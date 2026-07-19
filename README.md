⚖️ Citation-Grounded Legal Information Chatbot for UAE/Dubai

An AI-powered Retrieval-Augmented Generation (RAG) chatbot that delivers accurate, context-aware, and citation-grounded answers to UAE/Dubai legal queries using LangChain, ChromaDB, and Groq LLMs.

<p align="center">












</p>
🌐 Live Demo

🚀 Try the chatbot:
https://lexguardai.streamlit.app/


📖 Project Overview

Legal information systems demand accuracy, transparency, and trustworthy sources. Traditional AI chatbots often hallucinate or generate unsupported legal advice.

This project addresses that challenge by implementing a Retrieval-Augmented Generation (RAG) pipeline that retrieves relevant legal documents before generating an answer. Every response is grounded in retrieved legal content, significantly improving reliability.

 Disclaimer: This chatbot provides legal information for educational purposes only and should not be considered professional legal advice.

✨ Key Features

 Citation-Grounded Responses

 Retrieval-Augmented Generation (RAG)

 Semantic Search using ChromaDB

 LangChain Retrieval Pipeline

 Groq LLM Integration

 Interactive Gradio Chat Interface

 Fast Low-Latency Responses

 Modular & Scalable Architecture

🏗️ Architecture


User Query
     │
     ▼
Gradio Chat Interface
     │
     ▼
LangChain Retrieval Chain
     │
     ▼
Embedding Model
     │
     ▼
ChromaDB Vector Store
     │
Relevant Legal Context
     ▼
Groq LLM
     │
     ▼
Citation-Grounded Answer


🚀 Workflow
User submits a legal query.
The query is embedded into vector space.
ChromaDB retrieves the most relevant legal document chunks.
LangChain constructs the retrieval context.
Groq LLM generates a response using only retrieved evidence.
The chatbot returns a citation-grounded answer.


📂 Project Structure
citation-grounded-legal-chatbot/

├── app.py
├── requirements.txt
├── src/
├── data/
├── processed/
├── vectorstore/
└── README.md


💬 Example Questions
What are employee termination rights in the UAE?
How is annual leave calculated?
What are tenant rights in Dubai?
What are the penalties for cheque bounce cases?
What are the legal requirements for starting a company in Dubai?

📊 Why RAG Instead of a Normal LLM?
Standard LLM	RAG Chatbot
May hallucinate	Retrieves legal evidence
No citations	Citation-grounded responses
Generic knowledge	Domain-specific knowledge
Lower reliability	Higher trustworthiness



💬 Chat Interface

<img width="1920" height="1080" alt="Screenshot 2026-07-19 234651" src="https://github.com/user-attachments/assets/24179e39-454d-4c54-a4a6-913e501f09ad" />



📄 Citation Response

<img width="1920" height="1080" alt="Screenshot 2026-07-19 234808" src="https://github.com/user-attachments/assets/db4cb4b5-cfd8-444b-9a08-52faca9ef81b" />


🔮 Future Enhancements
Arabic Language Support
Voice-based Legal Assistant
Multi-turn Conversation Memory
PDF Upload & Legal Analysis
Advanced Citation Formatting
Docker Deployment
Authentication & User Profiles


📈 Project Highlights
Built a complete RAG pipeline for legal question answering.
Integrated semantic search using ChromaDB.
Used Groq LLMs for fast inference.
Designed a modular architecture for easy scalability.
Delivered citation-grounded legal responses to improve answer reliability.


👨‍💻 Author

Prajjval Pawar

GitHub: https://github.com/Prajjval02

LinkedIn: https://www.linkedin.com/in/prajjvalpawar/
