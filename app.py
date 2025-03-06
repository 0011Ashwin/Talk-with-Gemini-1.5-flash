# # Q&A Chatbot
# #from langchain.llms import OpenAI

# from dotenv import load_dotenv

# load_dotenv()  # take environment variables from .env.

# # importing libraries
# import streamlit as st
# import os
# import pathlib
# import textwrap
# from IPython.display import display
# from IPython.display import Markdown
# import google.generativeai as genai




# def to_markdown(text):
#   text = text.replace('•', '  *')
#   return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ## Function to load OpenAI model and get respones

# def get_gemini_response(question):
#     model = genai.GenerativeModel('gemini-1.5-pro')
#     response = model.generate_content(question)
#     return response.text

# ##initialize our streamlit app

# st.set_page_config(page_title="Q&A Demo")

# # streamlit header part 
# st.header("Gemini-flash-1.5🚨🔍")

# # streamlit sub-header part 
# st.subheader("Hey, there! I am Gemini-flash-1.5, a Q&A chatbot. Ask me anything!🤖🔮")

# input=st.text_input("Input: ",key="input")
# submit=st.button("Ask the question")

# ## If ask button is clicked

# if submit:
    
#     response=get_gemini_response(input)
#     st.subheader("The Response is")
#     st.write(response)

from flask import Flask, render_template, request
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(question)
    return response.text

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    response = ""
    if request.method == 'POST':
        question = request.form['question']
        response = get_gemini_response(question)
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)