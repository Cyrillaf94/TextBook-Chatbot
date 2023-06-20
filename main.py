from dotenv import load_dotenv
import pickle
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
import pdb
import re



def embed_pdf(pdf, start=None, end=None, name=None):
    if os.path.isfile(pdf):
        store_name = name if name else os.path.splitext(pdf)[0]

        if not os.path.exists(f"{store_name}.pkl"):
            pdf_reader = pdfplumber.open(pdf)
            pdb.set_trace()
            text = ""
            start = start if start else 0
            end = end +1 if end else len(pdf_reader.pages)
            for page in pdf_reader.pages[start:end]:
                text += page.extract_text()
            if len(text) < 1000:
                return 'Error processing text'
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
                )
            chunks = text_splitter.split_text(text=text)
            load_dotenv()
            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"data/processed/{store_name}.pkl", "wb") as f:
                    pickle.dump(VectorStore, f)
    else:
        return 'Error in processing request'



def ask_question_on_doc(query=None):
    with open(f"data/processed/Gastrointestinal.pkl", "rb") as f:
            VectorStore = pickle.load(f)
    if query:
        load_dotenv()
        llm = OpenAI()
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        docs = VectorStore.similarity_search(query=query, k=1)
        question = '''You are a professor creating a quizz,
        Please generate different blocks, each corresponding to a multiple choice question (5 choices, only one is correct).
        Each block includes: the question, the choices, the correct answer, and an explanation for the correct answer.
        Make sure to provide at least two disctinct and complete question blocks
        Each block will be returned as follows:
        Question 1:
        A)
        B)
        C)
        D)
        E)
        Answer: M)
        Explanation:'''
        for doc in docs:
            with get_openai_callback() as cb:
                response = chain.run(input_documents=[doc], question=question)
                print(cb)
                print(response)
        pattern = r"Question (\d+): (.*?)\n(A\)) (.*?)\n(B\)) (.*?)\n(C\)) (.*?)\n(D\)) (.*?)\n(E\)) (.*?)\nAnswer: (.*?)\nExplanation: (.*?)\n"

        matches = re.findall(pattern, response)
        if len(matches) > 0:
            questions = [
                {
                    "id": int(match[0]),
                    "question": match[1],
                    "choices": {
                        "A": match[3],
                        "B": match[5],
                        "C": match[7],
                        "D": match[9],
                        "E": match[11]
                    },
                    "answer": match[12],
                    "explanation": match[13]
                }
                for match in matches
            ]
            return questions
        else:
            "Regex error"
    else:
        return 'Error no query'



if __name__ == '__main__':
    #for book in book2_content.items():
    embed_pdf('data/raw/Gastrointestinal.pdf', name='Gastrointestinal')
    # ask_question_on_doc(query='gastrointestinal anatomy')
