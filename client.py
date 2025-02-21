import requests
import streamlit as st

def get_groq_response(input_text):
    json_body = {
        "input": {
            "language": "French",
            "text": input_text
        }
    }

    response = requests.post("http://127.0.0.1:5000/chain/invoke", json=json_body)

    if response.status_code == 200:
        data = response.json()
        return data.get("output", "No translation found.")  # Extract only 'output' field
    else:
        return "Error: Unable to process the request."

# Streamlit app
st.title("LLM Application Using LCEL")
input_text = st.text_input("Enter the text you want to translate to French")

if input_text:
    translated_text = get_groq_response(input_text)
    st.subheader("Translated Text:")
    st.write(translated_text)  # Display the translated text only
