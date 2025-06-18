from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

# Load Google API key
load_dotenv()

# 📁 Replace this with your IPC folder path
pdf_directory = r"C:\Users\megha\Desktop\judicio bot\IPC"

def get_all_pdf_files(directory):
    """Get all .pdf files in the directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(".pdf")]

def extract_text(pdf_paths):
    """Extract text from all pages in the PDFs."""
    full_text = ""
    for path in pdf_paths:
        try:
            reader = PdfReader(path)
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    full_text += content + "\n"
        except Exception as e:
            print(f"[⚠] Error reading {path}: {e}")
    return full_text

def main():
    pdf_files = get_all_pdf_files(pdf_directory)
    print(f"[📚] Found {len(pdf_files)} PDF files.")

    raw_text = extract_text(pdf_files)
    print(f"[📄] Total extracted text length: {len(raw_text)} characters")

    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = splitter.split_text(raw_text)

    print(f"[✂️] Total chunks created: {len(chunks)}")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    vectorstore.save_local("faiss_index_legal")

    print("[✅] Vector store saved as 'faiss_index_legal'")

if __name__ == "__main__":
    main()
