# 🧠 CogniFlow-RAG
An Enterprise-Grade Agentic RAG system that self-corrects, verifies facts, and uses web search tools. Built with LangGraph &amp; Next.js.

CogniFlow-RAG: Autonomous Self-Correcting Knowledge Engine
CogniFlow-RAG is an enterprise-grade "Agentic" Retrieval-Augmented Generation (RAG) platform designed to solve the biggest problem in GenAI: Hallucination.

Unlike traditional RAG systems that blindly trust retrieved documents, CogniFlow uses a Graph-Based Architecture (LangGraph) to "reason" about the data. It evaluates the quality of retrieved information, automatically rewrites poor queries, and falls back to web search if its internal database is insufficient.

🚀 Key Features
Self-Reflective Retrieval: The system grades its own retrieved documents for relevance before answering. If the documents are irrelevant, it discards them.

Active Web Fallback: If internal documents don't answer the question, the agent autonomously triggers a web search (via Tavily API) to find real-time information.

Hallucination Guardrails: A final "Grader Agent" checks if the generated answer is factually supported by the documents. If not, it forces a re-generation.

"Thinking" UI: A real-time dashboard (Next.js) that visualizes the agent's decision-making process (e.g., Thinking... -> Bad Data Found -> Searching Web -> Generating Answer).

🛠️ Tech Stack
Orchestration: LangGraph (State Machine & Logic Loops)

LLM Integration: OpenAI GPT-4o / Llama 3 (via Groq)

Vector Database: Pinecone (Hybrid Search: Sparse + Dense Embeddings)

Backend: FastAPI (Async Python)

Frontend: Next.js & Tailwind CSS

Tools: Tavily Search API, LangSmith (Tracing/Debugging)

🏗️ Architecture
The system follows a Corrective RAG (CRAG) pattern:

Retrieve: Fetch documents based on user query.

Grade: AI evaluates if documents are relevant.

Correct:

If Relevant: Proceed to generation.

If Irrelevant: Rewrite query → Search Web.

Generate: Create the final answer.
