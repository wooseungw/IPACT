import os
from glob import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

# Initialize variables
documents = []
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Define the directory containing the PDF files
pdf_directory = './data'

# Use glob to get all PDF files in the directory
pdf_files = glob(os.path.join(pdf_directory, '*.pdf'))

# Load all PDF files using PyPDFLoader
for pdf_file in pdf_files:
    loader = PyPDFLoader(pdf_file)
    pdf_documents = loader.load()
    documents.extend(pdf_documents)

# Split the documents into chunks
chunk_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = chunk_splitter.split_documents(documents)

# Create embeddings
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings)
retriever = vectordb.as_retriever()

# Create the QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-4", temperature=0),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# Define the chatbot response function
def get_chatbot_response(chatbot_response):
    print(chatbot_response['result'].strip())
    print('\n문서 출처:')
    for source in chatbot_response["source_documents"]:
        print(source.metadata['source'])