import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Directly input your API key here
groq_api_key = "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"  # Replace with your actual Groq API key

# Streamlit UI
st.title("LLM Translation App")

# Language Options
languages = ["French", "Spanish", "German", "Italian"]
selected_language = st.selectbox("Select Language", languages)

# LLM Models
llm_models = ["mixtral-8x7b-32768", "Gemma2-9b-It"]
selected_model = st.selectbox("Select LLM Model", llm_models)

# Initialize the model with the selected LLM model and API key
model = ChatGroq(model=selected_model, groq_api_key=groq_api_key)

# Define the prompt template dynamically based on selected language
system_template = f"Translate the following into {selected_language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# Initialize the output parser
parser = StrOutputParser()

# Create the chain (model -> prompt -> parser)
chain = prompt_template | model | parser

# User input for translation
input_text = st.text_input(f"Enter the text you want to translate to {selected_language}")

# Function to process input text and get translation
def get_translation(input_text):
    try:
        # Prepare the input text for the chain, directly as a dict with the necessary keys
        result = chain.invoke({"text": input_text})  # Ensure the input matches the prompt
        st.write(f"Chain result: {result}")  # Debugging line to print the result
        
        if result:
            # Return the output from the chain or fallback message if no output
            return result.get('output', "Translation failed.")
        else:
            return "Error: No valid result returned from the model."
    except Exception as e:
        st.write(f"Error encountered: {e}")  # Display the error message
        return "Error processing the translation."

# Trigger translation when input is provided
if input_text:
    translated_text = get_translation(input_text)
    st.subheader(f"Translated Text ({selected_language}):")
    st.write(translated_text)
