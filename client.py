import os
import requests
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize model
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# Output parser
parser = StrOutputParser()

# Create the translation chain
chain = prompt_template | model | parser

# Streamlit app
st.title("LLM Application Using LCEL")
input_text = st.text_input("Enter the text you want to translate to French")

if input_text:
    try:
        # Run the translation directly in the chain
        translated_text = chain.invoke({"language": "French", "text": input_text})
        st.subheader("Translated Text:")
        st.write(translated_text)
    except Exception as e:
        st.error(f"Error: {str(e)}")
