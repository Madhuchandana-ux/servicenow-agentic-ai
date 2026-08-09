# 🤖 AI Service Desk Agent

An intelligent AI-powered IT service desk application that automatically analyzes IT incidents, predicts their category and priority, retrieves relevant solutions from a knowledge base using vector search, and creates real incidents directly in ServiceNow.

---

## 🚀 Overview

Traditional IT service desks often require manual incident classification, prioritization, knowledge lookup, and ticket creation.

This project automates that workflow using a combination of:

- Machine Learning
- Natural Language Processing
- TF-IDF
- Sentence Transformers
- FAISS vector search
- Agent-based workflow orchestration
- LangGraph
- Streamlit
- ServiceNow REST API

The system takes a natural-language IT incident such as:

> "VPN is not connecting to the office network"

and automatically determines:

- Incident category
- Incident priority
- Relevant resolution
- Assignment group

The user can then create a **real ServiceNow incident** directly from the application.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    │  IT Incident Input  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Streamlit UI    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Incident Agent    │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┼─────────────┐
                 │             │             │
                 ▼             ▼             ▼
        ┌──────────────┐ ┌──────────────┐ ┌───────────────┐
        │  Category    │ │   Priority   │ │ Knowledge/RAG │
        │ ML Model     │ │   ML Model   │ │    Agent      │
        └──────┬───────┘ └──────┬───────┘ └───────┬───────┘
               │                │                  │
               └────────────────┼──────────────────┘
                                ▼
                    ┌─────────────────────┐
                    │   Decision Agent    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Category / Priority │
                    │ Resolution / Group  │
                    └──────────┬──────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │ Create ServiceNow Ticket │
                 └────────────┬─────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ ServiceNow REST API │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Real Incident     │
                    │     INCxxxxxxx      │
                    └─────────────────────┘
---
##🧠 Key Features
1. Incident Classification

The application analyzes the user's incident description and predicts the appropriate incident category using a trained machine learning model.

Example:

Input:
VPN is not connecting to the office network

Output:
Category → Network
2. Priority Prediction

A machine learning model predicts the incident priority based on incident-related features.

The system considers information such as:

Description
Impact
Urgency

Example:

Input:
VPN is not connecting to the office network

Output:
Priority → High
3. Knowledge Base Retrieval

The project contains an IT service desk knowledge base.

The system uses Sentence Transformers to convert the incident and knowledge-base content into vector embeddings.

The embedding model used is:

all-MiniLM-L6-v2

FAISS is then used to perform similarity search and retrieve relevant knowledge-base records.

User Incident
      ↓
Sentence Transformer
      ↓
Vector Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Knowledge
      ↓
Recommended Resolution

The retrieved knowledge-base record provides:

Resolution
Assignment Group
4. Agentic Workflow

The application uses multiple specialized agents.

Incident Agent
      ↓
Category Agent
      ↓
Priority Agent
      ↓
Knowledge Agent
      ↓
Decision Agent

Each agent performs a specific task instead of putting the entire workflow into one function.

5. LangGraph Workflow

LangGraph is used to orchestrate the agent workflow.

The workflow follows:

Incident
   ↓
Category
   ↓
Priority
   ↓
Knowledge
   ↓
Decision

The agents share a common state containing:

Incident
Category
Priority
Resolution
Assignment Group

This provides a structured state-based workflow for processing incidents.

6. ServiceNow Integration

The application integrates with a real ServiceNow Personal Developer Instance (PDI) through the ServiceNow REST API.

After the AI analyzes an incident, the user can click:

🚀 Create ServiceNow Ticket

The application sends the incident information to ServiceNow and receives the generated incident number.

Example:

INC0010XXX

This demonstrates an end-to-end integration between an AI application and an enterprise IT service management platform.

🖥️ Application Workflow
Step 1 — Enter Incident

The user enters an IT issue into the Streamlit interface.

Example:

VPN is not connecting to the office network
Step 2 — Analyze Incident

The AI agents process the incident.

Step 3 — View AI Results

The application displays:

Category
Priority
Assignment Group
Recommended Resolution
Step 4 — Create Ticket

The user clicks:

🚀 Create ServiceNow Ticket
Step 5 — ServiceNow Incident

The application sends the incident to ServiceNow through the REST API.

A real ServiceNow incident is created and an incident number is returned.

Example:

INC0010XXX
📁 Project Structure
servicenow-agentic-ai/
│
├── app.py
├── README.md
├── .gitignore
│
├── data/
│   ├── incidents_cleaned.csv
│   └── knowledge_base.csv
│
├── models/
│   ├── category_model.pkl
│   ├── priority_model.pkl
│   └── tfidf.pkl
│
├── src/
│   ├── agents.py
│   ├── build_vector_db.py
│   ├── feature_engineering.py
│   ├── preprocessing.py
│   ├── rag.py
│   ├── search_vector_db.py
│   ├── servicenow.py
│   ├── test_category_model.py
│   ├── train_category_model.py
│   └── train_priority_model.py
│
├── test_servicenow.py
│
└── vector_db/
    ├── knowledge.index
    └── knowledge.pkl
🛠️ Tech Stack
Technology	Purpose
Python	Core programming language
Pandas	Data processing
NumPy	Numerical operations
Scikit-learn	Machine learning and TF-IDF
Joblib	Model serialization and loading
Sentence Transformers	Text embeddings
FAISS	Vector similarity search
LangGraph	Agent workflow orchestration
Streamlit	Web application
Requests	REST API communication
Python-dotenv	Environment variable management
ServiceNow REST API	Incident management
Git & GitHub	Version control
🔍 Knowledge Retrieval Pipeline

The knowledge base is indexed before the application performs searches.

Knowledge Base CSV
       ↓
Text Processing
       ↓
Sentence Transformer
       ↓
Embeddings
       ↓
FAISS Index
       ↓
Vector Database

During an incident:

Incident
   ↓
Embedding
   ↓
FAISS Similarity Search
   ↓
Top Relevant Knowledge Records
   ↓
Resolution + Assignment Group
🤖 Agent Responsibilities
Agent	Responsibility
Incident Agent	Initializes and receives the incident
Category Agent	Predicts the incident category
Priority Agent	Predicts incident priority
Knowledge Agent	Retrieves relevant knowledge using vector search
Decision Agent	Produces the final incident summary
⚙️ Installation
1. Clone the repository
git clone https://github.com/Madhuchandana-ux/servicenow-agentic-ai.git
2. Navigate to the project
cd servicenow-agentic-ai
3. Create a virtual environment
python -m venv .venv
4. Activate the environment

For Windows PowerShell:

.venv\Scripts\Activate.ps1
5. Install dependencies
pip install pandas numpy scikit-learn sentence-transformers faiss-cpu streamlit langgraph requests python-dotenv joblib
🔐 Environment Variables

Create a .env file in the project root:

SERVICENOW_INSTANCE=https://your-instance.service-now.com
SERVICENOW_USERNAME=admin
SERVICENOW_PASSWORD=your-password
⚠️ Security

Never commit .env to GitHub.

The .gitignore file includes:

.env

so your ServiceNow credentials remain outside version control.

▶️ Running the Application

From the project root:

streamlit run app.py

The application will open in your browser.

🧪 Testing the ServiceNow API

The ServiceNow integration can be tested independently using:

python test_servicenow.py

A successful ServiceNow incident creation request returns:

201 Created

The response contains the newly created incident information, including the incident number.

Example:

Incident Number: INC0010XXX
📊 Example
Input
VPN is not connecting to the office network
AI Analysis
Category:
Network

Priority:
High

Assignment Group:
Network Support

Resolution:
Check VPN connectivity, credentials, network configuration,
and VPN client status.
ServiceNow
Incident created successfully

INC0010XXX
🎯 Project Objectives

The main objectives of this project are:

Automate IT incident classification
Automatically prioritize incidents
Retrieve relevant solutions from a knowledge base
Reduce manual service desk effort
Automate ServiceNow ticket creation
Demonstrate an agent-based AI workflow
Integrate AI capabilities with an enterprise ITSM platform
🔮 Future Improvements

Potential improvements include:

Human-in-the-loop approval before ticket creation
Automated incident summarization
Duplicate incident detection
SLA breach prediction
Sentiment analysis
Automatic reassignment based on agent availability
Resolution feedback loop
Incident analytics dashboard
Monitoring and observability
OAuth-based ServiceNow authentication
LLM-powered reasoning and tool selection
Automated testing and CI/CD
Improved model evaluation and monitoring
👩‍💻 Author

Madhuchandana Sunkara

Artificial Intelligence & Data Science
Chaitanya Bharathi Institute of Technology, Hyderabad

⭐ Project Highlights

This project demonstrates an end-to-end AI-powered enterprise workflow combining:

Machine Learning
      +
Natural Language Processing
      +
Vector Search
      +
Knowledge Retrieval
      +
Agentic Workflow
      +
LangGraph
      +
Streamlit
      +
ServiceNow REST API

The result is an AI service desk system capable of transforming a natural-language IT issue into:

Natural Language Incident
        ↓
AI Analysis
        ↓
Category + Priority
        ↓
Knowledge Retrieval
        ↓
Resolution + Assignment Group
        ↓
ServiceNow REST API
        ↓
Real ServiceNow Incident
