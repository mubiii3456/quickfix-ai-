🏗️ Full Technology Stack (Comprehensive)
This project integrates a sophisticated AI and Web stack to ensure high performance, security, and accuracy:

1. AI Orchestration & Logic
LangGraph: The core "brain" of the system. It manages the conversation as a Stateful Graph, allowing the agent to intelligently switch between answering questions and collecting lead data.

LangChain: The primary framework used to orchestrate LLM chains, document loaders, and memory management.

Groq LPU Engine: The high-speed inference engine that allows the AI to respond in milliseconds.

Llama 3.3 (70B): The powerful Large Language Model (LLM) that provides human-like reasoning and understanding.

2. Frontend & User Experience
Streamlit: The core web framework used to build the entire application. It handles the interactive chat interface, sidebar logic, and the real-time data rendering.

Custom CSS Styling: Advanced CSS injected into Streamlit to create a professional Glassmorphism Dark Theme and custom chat bubbles.

Responsive Design: Optimized for both mobile and desktop views to ensure plumbers can access leads on the go.

3. Knowledge Intelligence (RAG)
RAG Architecture: A custom pipeline that retrieves data from local business files so the AI provides factual, business-specific answers.

Vector Database (FAISS/Chroma): Stores plumbing data as mathematical embeddings for high-speed semantic search.

HuggingFace Embeddings: Used to transform raw text into vectors for the RAG engine.

4. Backend & Communication
SMTP Protocol: Integrated with Python’s smtplib to send automated, structured email alerts to the business owner whenever a new lead is captured.

NLP Lead Extraction: Custom Python logic and regex patterns used to identify phone numbers and "Booking Intent" from user messages.

Data Persistence: Uses a structured CSV-based logging system (leads.csv) to store customer data securely for the owner to review.

🔄 System Workflow: How It Works
Input: The user asks a question via the Streamlit chat interface.

Retrieval: The system searches the Vector Store for relevant plumbing facts.

Decision: LangGraph evaluates the conversation state. If a user wants to book, it triggers the Lead Capture Node.

Action: The system saves the lead to a CSV file and triggers an SMTP Email Alert to the owner.

Admin Review: The owner logs into the hidden Admin Dashboard to view all captured leads.

🔐 Admin Dashboard Access

The Admin Panel is hidden to ensure data privacy:

Access URL: https://quickfixais.streamlit.app/?view=admin

Authentication: Open the Sidebar and enter the Master Password.

Master Password: mubashir5007

🚀 Local Installation & Setup

Clone the Repository

Bash
git clone https://github.com/mubiii3456/quickfix-ai-

cd quickfix-ai-

Install Dependencies

Bash

pip install -r requirements.txt

Configure Environment (.env)

Create a .env file and add:


Code snippet 

GROQ_API_KEY=your_groq_key

EMAIL_PASS=your_gmail_app_password

ADMIN_PASSWORD=mubashir5007

SENDER_EMAIL=your_email@gmail.com

RECEIVER_EMAIL=owner_email@gmail.com

Launch the App

Bash

streamlit run app.py

👨‍💻 Developer Contact

Jam Mubashir Ahmed | AI Solutions & Full-Stack Developer

WhatsApp: +92 316 7042947

LinkedIn: Jam Mubashir Ahmed

GitHub: @mubiii3456
