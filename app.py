import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load Google API key
load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Few-shot examples used for better responses
example_qa_pairs = [
    {
        "question": "My husband is not providing financial support. What can I do?",
        "answer": "Under Section 125 of the CrPC, a wife can claim maintenance from her husband. You can file a maintenance petition in the family court."
    },
    {
        "question": "What is the process for mutual divorce?",
        "answer": "Under Section 13B of the Hindu Marriage Act, both spouses must live separately for at least one year and mutually agree to dissolve the marriage. File a joint petition in the family court."
    },
    {
        "question": "Someone posted my personal photos without consent. What can I do?",
        "answer": "This is a violation under the IT Act, Section 66E. You can file a cybercrime complaint at the local police station or through the National Cyber Crime Reporting Portal."
    },
    {
        "question": "I was tricked into sharing my bank OTP. What now?",
        "answer": "Report immediately to your bank and lodge a cybercrime FIR under Section 66D of the IT Act for online cheating."
    },
    {
        "question": "I received a defective product and the company is not responding. What are my rights?",
        "answer": "Under the Consumer Protection Act 2019, you have the right to a refund or replacement. You can file a complaint at the District Consumer Forum."
    },
    {
        "question": "Can I get compensation for poor services from a hotel?",
        "answer": "Yes, poor service falls under 'deficiency in service' as per Consumer Protection Act. You can claim compensation by filing a consumer complaint."
    }
]

def format_examples():
    """Join all few-shot examples into a formatted prompt."""
    example_text = ""
    for ex in example_qa_pairs:
        example_text += f"Q: {ex['question']}\nA: {ex['answer']}\n\n"
    return example_text.strip()

# Prompt for the legal assistant
prompt_template = """
You are an AI-powered legal assistant named Judico Bot. Your role is to provide clear, accurate, and helpful legal advice in the Indian context.

Below are a few example legal questions and answers:
{examples}

Instructions:
- Respond with relevant Indian law if possible.
- Be respectful and helpful.
- If the answer is not found in the documents, say: "The answer is not available in the context provided."

Context:
{context}

Question:
{question}
"""

def get_conversational_chain():
    examples = format_examples()
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5)
    return load_qa_chain(model, chain_type="stuff", prompt=prompt.partial(examples=examples))

def user_input(user_question, chat_history):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index_legal", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )

    chat_history.append({"user": user_question, "bot": response["output_text"]})
    return chat_history

def display_chat(chat_history):
    for chat in chat_history:
        st.markdown(
            f"""<div style='background-color:#e6f2ff;padding:10px;margin:10px 0;border-radius:5px;'>
            <b>You:</b> {chat['user']}</div>""",
            unsafe_allow_html=True
        )
        st.markdown(
            f"""<div style='background-color:#f9f9f9;padding:10px;margin:10px 0;border-radius:5px;'>
            <b>Judico Bot:</b> {chat['bot']}</div>""",
            unsafe_allow_html=True
        )

def main():
    st.set_page_config("Judico Bot: Your Legal Assistant")
    st.header("🧑‍⚖️ Judico Bot - Legal Chat Assistant")

    # No sidebar or scenario selection
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_question = st.text_input("Ask a legal question...")

    if user_question:
        with st.spinner("Getting legal advice..."):
            st.session_state["chat_history"] = user_input(
                user_question,
                st.session_state["chat_history"]
            )

    display_chat(st.session_state["chat_history"])

if __name__ == "__main__":
    main()
