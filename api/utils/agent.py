from operator import itemgetter
from typing import TypedDict, Any
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Qdrant
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers import EnsembleRetriever
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv


# 1. Define the state
class EpicGraphState(TypedDict):
    """State for the Epic Graph"""
    query: str
    epic_key: str
    epic_summary: str
    epic_tickets: list[Any]
    is_related: bool
    online_results: list[Any]


class SprintScribeAgent:
    """Sprint Scribe Agent"""
    def __init__(self):
        load_dotenv(".env.local")
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.tavily = TavilySearchResults()

        # Load tickets
        loader = CSVLoader(
            file_path="./data/TF-Task.csv",
            metadata_columns=["Issue key", "Parent key", "Parent summary", "Summary"],
        )
        self.jira_tickets = loader.load()

        # Load epics
        loader = CSVLoader(
            file_path="./data/TF-EPIC.csv",
            metadata_columns=["Issue key", "Summary"],
        )

        self.jira_epics = loader.load()

        # Create retriever
        # 1. Naive retriever
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        vectorstore = Qdrant.from_documents(
            self.jira_tickets,
            embeddings,
            location=":memory:",
            collection_name="LoanComplaints",
        )
        naive_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

        # 2. Multi-query retriever
        multi_query_retriever = MultiQueryRetriever.from_llm(
            retriever=naive_retriever, llm=self.llm
        )

        # 3. Ensemble retriever
        retriever_list = [
            naive_retriever,
            multi_query_retriever,
        ]
        equal_weighting = [1 / len(retriever_list)] * len(retriever_list)

        ensemble_retriever = EnsembleRetriever(
            retrievers=retriever_list, weights=equal_weighting
        )

        self.ensemble_retrieval_chain = (
            {
                "context": itemgetter("question") | ensemble_retriever,
                "question": itemgetter("question"),
            }
            | RunnablePassthrough.assign(context=itemgetter("context"))
        )

        self.setup_graph()

    def setup_graph(self):
        """Initialize the LangGraph workflow"""
        graph = StateGraph(EpicGraphState)

        # Add nodes
        graph.add_node("RetrieveTickets", self._retrieve_tickets_node)
        graph.add_node("GetEpicSummary", self._get_epic_summary_node)
        graph.add_node("ValidateQueryEpic", self._validate_query_epic_node)
        graph.add_node("ExtractTasksFromEpic", self._extract_tasks_from_epic_node)
        graph.add_node("SearchOnline", self._search_online_node)
        graph.add_node("GenerateEpicsAndTickets", self._generate_epics_and_tickets_node)

        # Set up edges
        graph.set_entry_point("RetrieveTickets")
        graph.add_edge("RetrieveTickets", "GetEpicSummary")
        graph.add_edge("GetEpicSummary", "ValidateQueryEpic")
        graph.add_conditional_edges(
            "ValidateQueryEpic",
            self._is_related_to_epic_condition,
            {
                True: "ExtractTasksFromEpic",
                False: "SearchOnline",
            },
        )
        graph.add_edge("ExtractTasksFromEpic", END)
        graph.add_edge("SearchOnline", "GenerateEpicsAndTickets")
        graph.add_edge("GenerateEpicsAndTickets", END)

        # Compile graph
        self.epic_graph = graph.compile()

    def _retrieve_tickets_node(self, state: EpicGraphState):
        """Node: Retrieve tickets related to the query"""
        query = state["query"]
        results = self.ensemble_retrieval_chain.invoke({"question": query})
        return {
            "epic_key": results['context'][0].metadata.get("Parent key") if "context" in results and len(results['context']) > 0 else None
        }

    def _get_epic_summary_node(self, state: EpicGraphState):
        """Node: Get Epic summary for the parent key"""
        epic_key = state["epic_key"]
        if not epic_key:
            return {"epic_summary": None}

        # Find the epic in jira_epics matching the epic_key
        epic_summary = None
        for epic in self.jira_epics:
            if epic.metadata.get("Issue key") == epic_key:
                epic_summary = epic.metadata.get("Summary")
                break

        return {"epic_summary": epic_summary}

    def _validate_query_epic_node(self, state: EpicGraphState):
        """Node: Validate if query is related to the epic summary"""
        query = state["query"]
        epic_summary = state["epic_summary"]
        if not epic_summary:
            return {"is_related": False}

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert project manager. Given a user query and an epic summary, determine if the query is about the epic. Respond with 'yes' or 'no'."),
            ("human", "Query: {query}\n\nEpic Summary: {epic_summary}\n\nIs the query about this epic?"),
        ])

        llm_input = prompt.format_messages(query=query, epic_summary=epic_summary)
        result = self.llm(llm_input)
        answer = result.content.strip().lower()

        return {"is_related": answer.startswith("yes")}

    def _is_related_to_epic_condition(self, state: EpicGraphState):
        """Condition: Check if related to epic"""
        return state["is_related"]

    def _extract_tasks_from_epic_node(self, state: EpicGraphState):
        """Node: Extract all tickets for the epic"""
        epic_key = state["epic_key"]
        if not epic_key:
            return {"epic_tickets": []}

        # Get tickets for this epic
        epic_tickets = []
        for ticket in self.jira_tickets:
            if ticket.metadata.get("Parent key") == epic_key:
                epic_tickets.append(ticket)

        # Build output JSON
        epic_name = epic_key
        if epic_tickets:
            epic_name = epic_tickets[0].metadata.get("Parent summary") or epic_key

        tickets_json = []
        for ticket in epic_tickets:
            name = ticket.metadata.get("Summary", "")
            description = ticket.page_content
            tickets_json.append({"name": name, "description": description})

        output_json = [{
            "epic_name": epic_name,
            "tickets": tickets_json
        }]

        return {"epic_tickets": output_json}

    def _search_online_node(self, state: EpicGraphState):
        """Node: Search online for technologies mentioned in the query"""
        query = state["query"]
        try:
            search_results = self.tavily.invoke({"query": query})
            return {"online_results": search_results}
        except Exception as e:
            print(f"Search error: {e}")
            return {"online_results": []}

    def _generate_epics_and_tickets_node(self, state: EpicGraphState):
        """Node: Generate epics and tickets from online info"""
        query = state["query"]
        online_results = state.get("online_results", [])
        context = "\n".join([r["content"] for r in online_results if "content" in r])

        prompt_template = """
You are a project analyst. Given a user query and online information about technologies, generate a list of relevant EPICs and tickets that might be needed for a project.

Format the output as a JSON list in the following structure:

[
  {{
    "epic_name": "<Epic Title>",
    "tickets": [
      {{
        "name": "<Task Title>", 
        "description": "<Task Description>"
      }}
    ]
  }}
]

Only output the JSON list, nothing else.

Query: {query}
Online Information: {context}
"""

        gen_chain = PromptTemplate.from_template(prompt_template) | self.llm | StrOutputParser()
        try:
            result = gen_chain.invoke({"query": query, "context": context})
            return {"epic_tickets": result}
        except Exception as e:
            raise e

# Global agent instance
agent = SprintScribeAgent()
