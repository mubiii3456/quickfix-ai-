import os
import csv
from langchain_groq import ChatGroq
from .state import AgentState
from vectorstore.db_manager import get_retriever
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
email_password = os.getenv("EMAIL_PASS")

llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)

def save_lead(text):
    with open('leads.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([text])

def retrieve_node(state: AgentState):
    question = state["messages"][-1].content
    retriever = get_retriever()
    docs = retriever.invoke(question) 
    context = "\n".join([d.page_content for d in docs])
    return {"context": context}

def send_email_alert(lead_details):
    sender_email = "jammubashir368@gmail.com" 
    receiver_email = "zartashahmed450@gmail.com" 
    app_password = os.getenv("EMAIL_PASS")

    msg = MIMEText(f"A new lead has been captured:\n\n{lead_details}")
    msg['Subject'] = '🚨 NEW LEAD: QuickFix Plumbing'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("📧 SUCCESS: Email notification sent!")
    except Exception as e:
        print(f"❌ ERROR: Email not send. Reason: {e}")
def generate_node(state: AgentState):
    user_msg = state["messages"][-1].content
    context = state.get("context", "")
    
    has_number = any(char.isdigit() for char in user_msg) and len(user_msg) > 7
    is_booking_intent = any(word in user_msg.lower() for word in ["book", "appointment", "schedule", "hire", "service"])

    if has_number:
    
        save_lead(f"CONTACT: {user_msg}")
        send_email_alert(f"Customer Number: {user_msg}")
        print("✅ Lead Saved & Email Sent!")


        friendly_response = (
            "Thank you so much! I've noted your phone number. 📝 "
            "A member of the QuickFix team will reach out to you shortly to discuss the details and confirm your appointment. "
            "Is there anything else I can help you with in the meantime?"
        )
        

        return {
            "answer": friendly_response, 
            "messages": [AIMessage(content=friendly_response)]
        }

    prompt = f"""You are the friendly QuickFix Plumbing Assistant.
    Context: {context}
    User Message: {user_msg}

    How to respond:
    1. If the user is asking questions about services or rates, answer them warmly using the context.
    2. If they just said 'Hi' or 'Hello', give them a warm welcome and ask how you can assist with their plumbing today.
    3. If they want to book but haven't given a number, politely ask for their phone number.
    
    Make sure your tone is professional yet helpful, like a real person at a front desk.
    """
    
    response = llm.invoke(prompt)
    
    if is_booking_intent:
        save_lead(f"INTENT: User wants to book - {user_msg}")
        print("📈 Booking interest captured.")

    return {"answer": response.content, "messages": [response]}