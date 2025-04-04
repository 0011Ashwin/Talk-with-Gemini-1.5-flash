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

from flask import Flask, render_template, request, jsonify, session
import os
import google.generativeai as genai
from dotenv import load_dotenv
import traceback

load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=GOOGLE_API_KEY)

def get_gemini_response(question):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(question)
        if response.text:
            return response.text
        else:
            return "I apologize, but I couldn't generate a response. Please try again."
    except Exception as e:
        print(f"Error in get_gemini_response: {str(e)}")
        print(traceback.format_exc())
        return "I apologize, but there was an error processing your request. Please try again."

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    if request.method == 'POST':
        try:
            question = request.form.get('question', '').strip()
            if not question:
                return jsonify({
                    'error': 'Please enter a question'
                }), 400

            response = get_gemini_response(question)
            
            # Add the conversation to chat history
            session['chat_history'].append({
                'question': question,
                'response': response
            })
            
            return jsonify({
                'question': question,
                'response': response
            })
        except Exception as e:
            print(f"Error in index route: {str(e)}")
            print(traceback.format_exc())
            return jsonify({
                'error': 'An error occurred while processing your request'
            }), 500
    
    return render_template('index.html', chat_history=session['chat_history'])

@app.route('/new-chat', methods=['POST'])
def new_chat():
    try:
        session['chat_history'] = []
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error in new_chat route: {str(e)}")
        return jsonify({
            'error': 'An error occurred while clearing chat history'
        }), 500

if __name__ == '__main__':
    # Fix for "ValueError: signal only works in main thread of the main interpreter"
    # Disable the reloader and run in threaded mode
    app.run(debug=False, threaded=True)
    
    # Alternative approach if above doesn't work:
    # import werkzeug.serving
    # werkzeug.serving.run_simple('localhost', 5000, app, use_debugger=True, use_reloader=False)