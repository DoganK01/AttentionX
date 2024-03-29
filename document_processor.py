import argparse
import os
import uuid
from typing import List
import glob
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_nomic import NomicEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.storage import InMemoryByteStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document

load_dotenv() # Load environment variables from .env file

class DocumentProcessor:
    def __init__(self, vector_store_path: str, collection_name: str, llm_model: str):
        self.embeddings = NomicEmbeddings(model='nomic-embed-text-v1.5')
        self.vectorstore = Chroma(embedding_function=self.embeddings, persist_directory=vector_store_path, collection_name=collection_name)
        self.store = InMemoryByteStore()
        self.retriever = MultiVectorRetriever(vectorstore=self.vectorstore, byte_store=self.store, id_key="doc_id")
        self.llm = self.initialize_llm(llm_model)

    def initialize_llm(self, llm_model: str):
        if llm_model == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="text-davinci-003", max_retries=0)
        elif llm_model == "mistral":
            from langchain_mistralai.chat_models import ChatMistralAI
            return ChatMistralAI(mistral_api_key=os.getenv("MISTRAL_API_KEY"), model="mistral-large-latest")
        else:
            raise ValueError(f"Unsupported LLM model: {llm_model}")

    def load_documents(self, doc_dir: str) -> List[Document]:

        documents = []
        for pdf_path in glob.glob(f"{doc_dir}/*.pdf"):
            print(f"Processing {pdf_path}...")
            loader = PyMuPDFLoader(pdf_path)
            docs = loader.load()  # Add a limiter if needed
            documents.extend(docs) 
        #docs = loader.load() #TODO: Ensure text sizes are smaller than 8,000 characters
        return docs

    def process_documents(self, documents: List[Document], n_batches: int):
        summaries = self.generate_summaries(documents, n_batches)
        doc_ids = [str(uuid.uuid4()) for _ in documents]
        summary_docs = [Document(page_content=s, metadata={"doc_id": doc_ids[i]}) for i, s in enumerate(summaries)]
        self.retriever.vectorstore.add_documents(summary_docs)
        self.retriever.docstore.mset(list(zip(doc_ids, documents)))
        for i, doc in enumerate(documents):
            doc.metadata["doc_id"] = doc_ids[i]
        self.retriever.vectorstore.add_documents(documents)

    def generate_summaries(self, documents: List[Document], n_batches: int) -> List[str]:
        chain = (
            {"doc": lambda x: x.page_content}
            | ChatPromptTemplate.from_template("Summarize the following document:\n\n{doc}") # TODO: Make modular templates for varying prompts
            | self.llm
            | StrOutputParser()
        )
        summaries = chain.batch(documents, {"max_concurrency": n_batches})
        return summaries

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process and summarize documents.")
    # parser.add_argument("--doc_path", type=str, required=True, help="Path to the document to be processed.")
    parser.add_argument("--doc_dir", type=str, required=True, help="Directory containing PDF documents to be processed.")
    parser.add_argument("--vector_store_path", type=str, default="./chroma_db", help="Path for storing vector data.")
    parser.add_argument("--collection_name", type=str, default="regulations", help="Collection name for the vector store.")
    parser.add_argument("--n_batches", type=int, default=1, help="Number of batches for processing summaries.")
    parser.add_argument("--llm_model", type=str, choices=["openai", "mistral"], default="openai", help="LLM for summaries.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    processor = DocumentProcessor(
        vector_store_path=args.vector_store_path, 
        collection_name=args.collection_name, 
        llm_model=args.llm_model
        )
    #documents = processor.load_documents(doc_path=args.doc_path)
    documents = processor.load_documents(doc_dir=args.doc_dir)
    processor.process_documents(documents=documents, n_batches=args.n_batches)

if __name__ == "__main__":
    main()
