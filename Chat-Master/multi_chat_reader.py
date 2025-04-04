# Importing the required libraries
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import time
import base64
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import json

# Set page config at the very beginning
st.set_page_config(
    page_title="PDF Intellichat",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Loading the API dot_env 
load_dotenv()
os.getenv("GOOGLE_API_KEY")

# Configuring the Google API key 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# App config and session state initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    with st.status("🤖 Generating response...", expanded=True) as status:
        st.write("Retrieving relevant information...")
        time.sleep(0.5)
        st.write("Processing with Gemini...")
        response = chain(
            {"input_documents":docs, "question": user_question}
            , return_only_outputs=True)
        st.write("Finalizing answer...")
        time.sleep(0.5)
        status.update(label="✅ Response ready!", state="complete", expanded=False)
    
    return response["output_text"]

def display_chat_history():
    for i, chat in enumerate(st.session_state.chat_history):
        if chat["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(chat["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(chat["content"])

def get_file_stats(pdf_docs):
    stats = []
    total_pages = 0
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        num_pages = len(pdf_reader.pages)
        total_pages += num_pages
        stats.append({"filename": pdf.name, "pages": num_pages, "size": f"{round(pdf.size/1024, 2)} KB"})
    return stats, total_pages

def apply_custom_css():
    if st.session_state.dark_mode:
        theme = """
        <style>
        .main {background-color: #1E1E1E; color: #FFFFFF;}
        .sidebar .sidebar-content {background-color: #252526; color: #FFFFFF;}
        .stButton>button {background-color: #0078D7; color: white;}
        .stTextInput>div>div>input {background-color: #3C3C3C; color: white;}
        </style>
        """
    else:
        theme = """
        <style>
        .stButton>button {background-color: #0078D7; color: white;}
        .chat-message {padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex;}
        .chat-message.user {background-color: #f0f2f6;}
        .chat-message.bot {background-color: #e3f6f5;}
        </style>
        """
    st.markdown(theme, unsafe_allow_html=True)

def get_pdf_download_link(pdf):
    """Generate a link to download the uploaded PDF"""
    b64 = base64.b64encode(pdf.getvalue()).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{pdf.name}">Download {pdf.name}</a>'

def main():
    apply_custom_css()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📚 PDF Intellichat")
        st.caption("Powered by Gemini AI")
    with col2:
        lottie_url = "https://assets10.lottiefiles.com/packages/lf20_2tVCkS.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=120, key="pdf_animation")
    
    st.markdown("---")
    
    with st.sidebar:
        st.title("🛠️ Control Panel")
        
        with st.expander("📁 Upload & Process", expanded=True):
            pdf_docs = st.file_uploader("Upload your PDF Files", 
                                        accept_multiple_files=True,
                                        type=['pdf'])
            
            col1, col2 = st.columns(2)
            process_btn = col1.button("Process PDFs")
            clear_btn = col2.button("Clear All")
            
            if process_btn and pdf_docs:
                with st.spinner("Processing PDFs..."):
                    # Display progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Extract text
                    status_text.text("Extracting text from PDFs...")
                    progress_bar.progress(25)
                    time.sleep(0.5)
                    raw_text = get_pdf_text(pdf_docs)
                    
                    # Step 2: Chunk text
                    status_text.text("Chunking text...")
                    progress_bar.progress(50)
                    time.sleep(0.5)
                    text_chunks = get_text_chunks(raw_text)
                    
                    # Step 3: Create vector store
                    status_text.text("Creating vector embeddings...")
                    progress_bar.progress(75)
                    time.sleep(0.5)
                    get_vector_store(text_chunks)
                    
                    # Complete
                    progress_bar.progress(100)
                    status_text.text("Ready to chat!")
                    st.session_state.pdf_processed = True
                    time.sleep(0.5)
                    
                    # Show success message
                    st.success("✅ PDFs processed successfully!")
                    
                    # Display file stats
                    if pdf_docs:
                        stats, total_pages = get_file_stats(pdf_docs)
                        st.session_state.pdf_stats = stats
                        st.session_state.total_pages = total_pages
            
            if clear_btn:
                st.session_state.chat_history = []
                st.session_state.pdf_processed = False
                st.success("All data cleared!")
        
        with st.expander("📊 PDF Statistics", expanded=False):
            if st.session_state.get('pdf_processed', False) and st.session_state.get('pdf_stats'):
                st.write(f"Total PDFs: {len(st.session_state.pdf_stats)}")
                st.write(f"Total Pages: {st.session_state.total_pages}")
                
                # Create a DataFrame to display stats
                df = pd.DataFrame(st.session_state.pdf_stats)
                st.dataframe(df)
        
        with st.expander("⚙️ Settings", expanded=False):
            st.toggle("Dark Mode", key="dark_mode", on_change=apply_custom_css)
            model = st.selectbox(
                "AI Model",
                ["gemini-1.5-pro", "gemini-1.5-flash"],
                index=0
            )
            temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
            st.caption("Higher temperature = more creative responses")
            
            exp_mode = st.checkbox("Expert Mode")
            if exp_mode:
                chunk_size = st.number_input("Chunk Size", min_value=1000, max_value=30000, value=10000, step=1000)
                chunk_overlap = st.number_input("Chunk Overlap", min_value=0, max_value=5000, value=1000, step=100)
        
        st.markdown("---")
        st.caption("Made with ❤️ by AI Team")
        st.caption("Version 2.0.0")

    # Main chat interface
    if not st.session_state.pdf_processed:
        st.info("👈 Please upload and process PDF documents from the sidebar first.")
        st.image("https://www.shutterstock.com/image-vector/upload-icon-vector-illustration-260nw-1890516314.jpg", width=300)
    else:
        # Display chat interface
        display_chat_history()
        
        # Get user question
        user_question = st.chat_input("Ask a question about your PDFs...")
        
        if user_question:
            # Add user question to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            
            # Display updated chat
            with st.chat_message("user", avatar="👤"):
                st.write(user_question)
            
            # Get AI response
            with st.chat_message("assistant", avatar="🤖"):
                ai_response = user_input(user_question)
                st.write(ai_response)
            
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

if __name__ == "__main__":
    main()