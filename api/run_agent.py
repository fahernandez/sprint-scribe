#!/usr/bin/env python3
"""
Sprint Scribe Agent CLI Runner

This script allows you to run the Sprint Scribe Agent from the terminal.
You can provide a query as a command line argument or run it interactively.

Usage:
    python run_agent.py "Your query here"
    python run_agent.py  # Interactive mode
"""

import json
import argparse
from typing import Dict, Any
from utils.agent import agent
from dotenv import load_dotenv


def print_results(results: Dict[str, Any]) -> None:
    """Pretty print the agent results"""
    print("\n" + "="*50)
    print("SPRINT SCRIBE AGENT RESULTS")
    print("="*50)
    
    # Print query
    if "query" in results:
        print(f"\n🔍 Query: {results['query']}")
    
    # Print epic information if available
    if results.get("epic_key"):
        print(f"\n📋 Found Epic: {results['epic_key']}")
        if results.get("epic_summary"):
            print(f"📝 Epic Summary: {results['epic_summary']}")
    
    # Print whether query is related to epic
    if "is_related" in results:
        status = "✅ Yes" if results["is_related"] else "❌ No"
        print(f"\n🔗 Related to Epic: {status}")
    
    # Print epic tickets if available
    if results.get("epic_tickets"):
        print("\n🎫 Epic Tickets:")
        try:
            # Try to parse as JSON if it's a string
            tickets = results["epic_tickets"]
            if isinstance(tickets, str):
                tickets = json.loads(tickets)
                
            if isinstance(tickets, list):
                for epic in tickets:
                    print(f"\n  📁 Epic: {epic.get('epic_name', 'Unknown')}")
                    for i, ticket in enumerate(epic.get('tickets', []), 1):
                        print(f"    {i}. {ticket.get('name', 'Unknown')}")
                        if ticket.get('description'):
                            # Truncate long descriptions
                            desc = ticket['description']
                            if len(desc) > 100:
                                desc = desc[:100] + "..."
                            print(f"       📄 {desc}")
            else:
                print(f"    {tickets}")
        except (json.JSONDecodeError, TypeError):
            print(f"    {results['epic_tickets']}")
    
    # Print online search results if available
    if results.get("online_results"):
        count = len(results['online_results'])
        print(f"\n🌐 Online Search Results: {count} results found")
        # Show first 3 results
        for i, result in enumerate(results["online_results"][:3], 1):
            if isinstance(result, dict):
                title = result.get("title", "No title")
                url = result.get("url", "No URL")
                print(f"    {i}. {title}")
                print(f"       🔗 {url}")
    
    print("\n" + "="*50)


def run_agent_with_query(query: str) -> Dict[str, Any]:
    """Run the agent with the given query"""
    print(f"🚀 Running Sprint Scribe Agent with query: '{query}'")
    print("⏳ Processing...")
    
    try:
        # Initialize the state with the query
        initial_state = {"query": query}
        
        # Run the agent graph
        result = agent.epic_graph.invoke(initial_state)
        
        return result
        
    except Exception as e:
        print(f"❌ Error running agent: {str(e)}")
        return {"error": str(e)}


def interactive_mode():
    """Run the agent in interactive mode"""
    print("🎯 Sprint Scribe Agent - Interactive Mode")
    print("Type 'quit' or 'exit' to stop")
    print("-" * 40)
    
    while True:
        try:
            query = input("\n💭 Enter your query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not query:
                print("⚠️  Please enter a valid query")
                continue
                
            results = run_agent_with_query(query)
            print_results(results)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Run the Sprint Scribe Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_agent.py "I need help with React hooks"
    python run_agent.py "Show me tasks for authentication epic"
    python run_agent.py  # Interactive mode
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Query to process (if not provided, runs in interactive mode)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    args = parser.parse_args()
    
    if args.query:
        # Single query mode
        results = run_agent_with_query(args.query)
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    print("Loading environment variables...")
    load_dotenv(".env.local")
    main() 
