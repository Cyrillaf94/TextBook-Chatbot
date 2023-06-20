import streamlit as st
import base64
from main import ask_question_on_doc


with st.sidebar:
    st.title('🤗💬 Amanda Medical Study')
    st.markdown('''
    ## About
    This app i an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model''')






def display_question(question, question_index):
    st.subheader(question["question"])
    user_answer = st.radio("Select an answer:", question["choices"].values(), key=f'answer{question_index}')
    #base64_pdf = display_pdf('data/raw/Gastrointestinal.pdf')
    if st.button('Submit', key=f'btn{question_index}_question'):
        #correct_answer = {"A":0, "B":1, "C":2, "D":3, "E":4}
        #print(correct_answer[question["answer"]{})
        if user_answer == question["choices"][question['answer'][0]]:
            st.write("Correct!")
            st.session_state.count_right += 1
            st.write(f"Explanation: {question['explanation']}")
        else:
            st.write(user_answer, question["choices"][question['answer'][0]])
            st.write("Incorrect.")
            st.session_state.count_wrong += 1
            st.write(f"The correct answer is: {question['answer']}")
            st.write(f"Explanation: {question['explanation']}")
        st.session_state.answered = True
    """ st.write(base64_pdf)
    pdf_display = f'<embed src=”data:application/pdf;base64,{base64_pdf}” width=”700″ height=”1000″ type=”application/pdf”>'
    st.markdown(pdf_display, unsafe_allow_html=True) """
    return


def display_mcq(questions):
    st.write(st.session_state)
    if st.button('Next Question'):
        if st.session_state.current_question < len(questions) - 1:
            st.session_state.current_question += 1
            st.session_state.answered = False
        else:
            st.write("No more questions.")
            st.write(f"Correct answers: {st.session_state.count_right}. Incorrect Answers: {st.session_state.count_wrong}")
    display_question(questions[st.session_state.current_question], st.session_state.current_question)


def display_pdf(pdf_file):
    with open(pdf_file,"rb") as f:
      base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    return base64_pdf



if 'count_wrong' not in st.session_state:
    st.session_state.count_wrong = 0
if 'count_right' not in st.session_state:
    st.session_state.count_right = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'next' not in st.session_state:
    st.session_state.next = False
if 'data' not in st.session_state:
    st.session_state.data = ''

query = st.text_input('What subject do you want to generate an MCQ on?',
                      value='Gastrointestinal Pharmacology',
                      max_chars=1000, )


questions = []
if st.button('Generate Questions'):  # The button returns True when pressed
    questions = ask_question_on_doc(query)
display_mcq(questions)
