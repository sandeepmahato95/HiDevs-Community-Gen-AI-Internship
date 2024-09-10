import streamlit as st
import sqlite3
from langchain import LLMChain, PromptTemplate
#from langchain.chains.qa import QA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
#from langchain.llms import Gemini
from speech_recognition import Recognizer, Microphone
import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Create a small employee database
conn = sqlite3.connect('employee.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS employees (
            name text,
            department text,
            salary real,
            age integer
            )""")

employees = [
    ('John Doe', 'Sales', 50000, 30),
    ('Jane Smith', 'Marketing', 60000, 28),
    ('Bob Johnson', 'IT', 70000, 35),
    ('Alice Brown', 'HR', 55000, 32),
    ('Mike Davis', 'Finance', 65000, 40)
]

## Disspaly ALl the records

print("Data inserted in the table:")
data=c.execute('''Select * from employees''')
for row in data:
    print(row)

c.executemany('INSERT INTO employees VALUES (?,?,?,?)', employees)
conn.commit()
conn.close()

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt): # def natural_language_to_sql(query):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

# Define a function to execute SQL queries and return results as rows
def execute_sql_query(sql,db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(sql)
    rows = c.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    \nThe SQL database named 'employee', has a table named 'employees' and has the following columns - name, department, salary, age in that table.
    \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this: SELECT COUNT(*) FROM employees;
    \nExample 2 - Tell me all the employees working in Marketing department?, 
    the SQL command will be something like this SELECT * FROM employees 
    where department="Marketing"; 
    also the sql code should not have ``` in beginning or end and sql word in output.

    """

]

## Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Joey Chatbot (Text to SQL)")

question = st.text_input("Text Input:", key="text_input")

# Add voice input for natural language queries
st.write("Or use voice input:")
if st.button("Start Voice Input"):
    r = Recognizer()
    with Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            voice_input = r.recognize_google(audio)
            st.write("You said:", voice_input)
            question = voice_input
            st.session_state.text_input = voice_input  # Update the text input with voice input
        except:
            st.write("Sorry, I didn't catch that.")

submit = st.button("Submit")

# if submit is clicked or voice input is recognized
if submit or ('voice_input' in locals() and voice_input):
    if question:
        response = get_gemini_response(question, prompt)
        print(response)
        response = execute_sql_query(response, "employee.db")
        st.subheader("The response is")
        for row in response:
            print(row)
            st.write(row) 
    else:
        st.write("Please provide a question using text or voice input.")



