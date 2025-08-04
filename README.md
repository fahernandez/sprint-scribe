# SprintScribe

SprintScribe is an AI-powered application that helps tech leads convert statements of work (SOW) into detailed implementation plans using historical Jira data and web research.

## Features

- **Intelligent Plan Generation**: Converts SOW tasks into structured epics and tickets
- **Historical Knowledge**: Leverages past Jira tickets and epics for context
- **Web Research Integration**: Automatically researches new technologies and best practices
- **Agentic RAG Architecture**: Uses LangGraph for sophisticated reasoning and retrieval

## How It Works

1. **Input**: Enter a statement of work task or requirement
2. **Analysis**: The system checks if the task relates to existing company knowledge (Jira epics)
3. **Generation**: 
   - If related to existing work: Extracts relevant tickets from historical epics
   - If new technology: Searches web for best practices and generates new implementation plan
4. **Output**: Returns structured epics with detailed tickets and acceptance criteria

## Architecture

- **Backend**: FastAPI with LangGraph agent
- **Frontend**: Next.js with React components
- **AI Models**: OpenAI GPT-4 for generation, OpenAI embeddings for retrieval
- **Data Sources**: Jira tickets/epics, web search via Tavily
- **Vector Store**: Qdrant for semantic search

## Setup

1. Install Python dependencies:
   ```bash
   uv sync
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   ```
   Add your API keys:
   - `OPENAI_API_KEY`
   - `TAVILY_API_KEY`
   - `LANGCHAIN_API_KEY` (optional, for tracing)

4. Start the development servers:
   ```bash
   # Backend (FastAPI)
   uvicorn api.index:app --reload --port 8000

   # Frontend (Next.js)
   npm run dev
   ```

## Usage

1. Navigate to `http://localhost:3000`
2. Enter a statement of work task in the text area
3. Click "Generate Implementation Plan"
4. Review the generated epics and tickets

## Example Queries

- "Set up Azure Data Factory for data pipeline processing"
- "Implement user authentication with OAuth 2.0"
- "Create REST API endpoints for data access"
- "Deploy infrastructure using Terraform"

## Sample Data

The application includes sample Jira data in the `data/` directory:
- `TF-Task.csv`: Sample tickets with descriptions and epic relationships
- `TF-EPIC.csv`: Sample epics with summaries

## Development

### Backend Structure
- `api/index.py`: FastAPI server with endpoints
- `api/utils/agent.py`: SprintScribe agent implementation
- `api/utils/prompt.py`: Prompt utilities
- `api/utils/tools.py`: Tool functions

### Frontend Structure
- `components/sprint-scribe.tsx`: Main SprintScribe interface
- `app/(chat)/page.tsx`: Main application page

## API Endpoints

- `POST /api/sprint-scribe`: Generate implementation plan
- `GET /api/health`: Health check
- `POST /api/chat`: Chat interface (existing)

## License

MIT License - see LICENSE file for details.
