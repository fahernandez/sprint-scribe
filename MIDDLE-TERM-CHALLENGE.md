# Certification Challenge – Deliverable Checklist  
**Due August 5, 2025 at 4 PM PT**
# SprintScribe
## Task 1 — Define Problem & Audience  
**Role:** *AI Solutions Engineer*
1. **One-sentence problem statement**  
Tech leads lack a fast, reliable way to turn a statement of work and past Jira knowledge into a repeatable, high-quality implementation plan—especially when unfamiliar technologies are involved.
2. **1–2 paragraphs** explaining why this is a problem for your specific user (describe their job role, pain points, and example questions)
As a Tech lead, you are judged on how quickly you can decompose a statement of work (SOW) into a concrete, step-by-step roadmap that your team and stakeholders trust. Today that means trawling through hundreds of Jira tickets from prior projects, company best practices and copying snippets into spreadsheets, and stitching everything together by hand. Each hour spent hunting for similar user stories, sprint burndowns, or acceptance-criteria patterns is an hour not spent guiding engineers or advising executives.
The pain deepens when a new framework or cloud service appears in the SOW. You must pause the planning exercise, research best practices on the web, then mentally map those findings onto a delivery model you’ve never tried in-house. The result is an uneven plan that may overlook hidden dependencies (“Did we remember security baselines for this unfamiliar PaaS?”) or ignore proven team velocities (“What did it really take our data-platform squad to integrate Snowflake last year?”). Clients feel the uncertainty, and your margin for error—and profit—shrinks.
## Task 2 — Propose Solution  
**Role:** *AI Solutions Engineer*
1. **1–2 paragraphs** describing the user experience and “better world”
In the better world, you paste or upload a task list from the SOW, tag it with a few project attributes (team size, domain, critical dates), and click Generate Plan. Behind the scenes, an engine mines your organization’s Jira history, surfaces analogous tickets, and auto-drafts a phased implementation plan—complete with sprint breakdowns, story point estimates derived from historical velocity, risk registers, and links back to the exact tickets that inspired each section. If the system detects an uncharted technology, it automatically pulls authoritative guidance from trusted web sources, cross-references similar tech you have used, and weaves those insights into the plan so nothing feels experimental or under-researched.
For this iteration, I’ll build an interface that takes a single task from the SOW and automatically produces a detailed set of subtasks with acceptance criteria. It will first mine the company’s Jira history for relevant patterns; if the technology is new to us, the system will enrich the plan by pulling trusted information from the web and by mapping lessons learned from comparable technologies in past projects.
2. **Tool-stack choices** (one sentence each)  
   - LLM -  
   - Embedding model  
   - Orchestration layer  
   - Vector database  
   - Monitoring  
   - Evaluation  
   - User interface  
   - *(Optional)* Serving & inference  
3. **Agentic reasoning:** where and why you will use agents in the app
## Task 3 — Data & APIs  
**Role:** *AI Systems Engineer*

1. **List all data sources and external APIs** with their purpose  
2. **Default chunking strategy** and rationale  
3. *(Optional)* Additional data needed for other app components
## Task 4 — End-to-End Prototype  
**Role:** *AI Systems Engineer*

- Build and **deploy locally** an **Agentic RAG** prototype using a production-grade stack

## Task 5 — Golden Test Set & Baseline  
**Role:** *AI Evaluation & Performance Engineer*

1. Generate a **synthetic “golden” test set** and evaluate with **RAGAS** (faithfulness, response relevance, context precision, context recall)  
2. Provide a **results table** and brief conclusions on baseline performance

## Task 6 — Advanced Retrieval Upgrade  
**Role:** *AI Systems Engineer*

1. **List advanced retrieval techniques** you’ll test (one-sentence justification each)  
2. Implement and test them in your application

## Task 7 — Performance Comparison  
**Role:** *AI Evaluation & Performance Engineer*

1. Re-evaluate improved system vs. original with **RAGAS**; present a **comparison table**  
2. Summarize insights and planned next steps for the second half of the course

## Final Submission Package  

Submit a public (or shared) **GitHub repository** containing:  

1. A **≤ 5-minute Loom video** demonstrating the app and describing the use case  
2. A **written document** answering every deliverable above  
3. **All source code**


> **Tip:** Use this checklist to track progress and ensure every deliverable is ready by the deadline. Good luck!






I am a consultant and I need to create an implementation plan for a project following the companies best practices and prior projects.


