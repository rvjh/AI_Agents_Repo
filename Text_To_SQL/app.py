# import os
# import streamlit as st
# from dotenv import load_dotenv
# import sqlite3
# from google import genai

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# client = genai.Client(api_key=GEMINI_API_KEY)


# ## getting the model
# def get_gemini_response(question, prompt, client):
#      response = client.models.generate_content(
#           model="gemini-2.0-flash",
#           contents=[prompt[0],question])
#      return response.text

# ## retrieve records for sqlite3
# def read_sql_query(sql, db):
#      conn = sqlite3.connect(db)
#      cur = conn.cursor()
#      cur.execute(sql)
#      rows = cur.fetchall()
#      conn.commit()
#      conn.close()
#      for r in rows:
#           print(r)
#      return rows

# prompt = [
#      """
#      You are an expert in converting English questions to SQL query!
     
#      The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION 
     
#      For example,
     
#      Example 1 - How many entries of records are present?
#           the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
     
#      Example 2 - Tell me all the students studying in Data Science class?
#           the SQL command will be something like this SELECT * FROM STUDENT where CLASS="Data Science";
     
#      also the sql code should not have ``` in beginning or end and sql word in. """
# ]


# st.set_page_config(page_title="Text to SQL")
# st.header("Using Gemini to retrieve data")

# q = st.text_input("Input: ", key="input")

# submit = st.button("Ask the question")
# if submit:
#      response = get_gemini_response(q, prompt, client)
#      print(response)
#      data = read_sql_query(response, "student.db")
#      st.subheader("Response is : ")
#      for r in response:
#           print(r)
#           st.header(r)


import os
import streamlit as st
from dotenv import load_dotenv
import sqlite3
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# Getting the model response
def get_gemini_response(question, prompt, client):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt[0], question]
    )
    return response.text

# Retrieve records from sqlite3
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

prompt = [
    """
    You are an expert in converting English questions to SQL query!
    
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION 
    
    For example,
    
    Example 1 - How many entries of records are present?
        the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    
    Example 2 - Tell me all the students studying in Data Science class?
        the SQL command will be something like this SELECT * FROM STUDENT where CLASS="Data Science";
    
    also the sql code should not have ``` in beginning or end and sql word in.
    """
]

st.set_page_config(page_title="Text to SQL")
st.header("Using Gemini to retrieve data")

q = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")
if submit:
    # Get the generated SQL query from Gemini
    response = get_gemini_response(q, prompt, client)
    
    # Retrieve the data using the generated SQL query
    data = read_sql_query(response, "student.db")
    
    # Display the result from the SQL query
    st.subheader("Response is:")
    if data:
        for r in data:
            st.write(r)  # Display each record in a new line
    else:
        st.write("No records found.")
