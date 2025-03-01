import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Directly input your API key here
groq_api_key = "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"  # Replace with your actual Groq API key

# Initialize the model with the provided API key
model = ChatGroq(model="mixtral-8x7b-32768", groq_api_key=groq_api_key)

# Define the prompt template for translation
system_template = "Translate the following into French:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# Initialize the output parser
parser = StrOutputParser()

# Create the chain (model -> prompt -> parser)
chain = prompt_template | model | parser

# Streamlit UI
st.title("LLM Translation App")
input_text = st.text_input("Enter the text you want to translate to French")

# Function to process input text and get translation
def get_translation(input_text):
    # Create a json_body that fits the model's input
    json_body = {
        "input": {
            "language": "French",
            "text": input_text
        }
    }

    # Run the chain to get the translation result
    result = chain.invoke({"input": json_body})

    # Return the translated text
    return result['output']

# Trigger translation when input is provided
if input_text:
    translated_text = get_translation(input_text)
    st.subheader("Translated Text:")
    st.write(translated_text)
