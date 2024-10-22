import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# Load environment variables
load_dotenv()

# Loading JSON file
try:
    with open('C:/Users/ACER/Gen1Project/response.json', 'r') as file:
        RESPONSE_JSON = json.load(file)

    # Further code using RESPONSE_JSON here
    #st.write(RESPONSE_JSON)

    st.title("MCQs Creator Application with LangChain ($8)")

    # Create a form using st.form
    with st.form("user_inputs"):
        # File Upload
        uploaded_file = st.file_uploader("Upload a PDF or txt file")
        
        # Input Fields
        mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)

        # Subject Input
        subject = st.text_input("Insert Subject", max_chars=20)
        
        # Quiz Tone (Complexity Level)
        tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")
        
        # Submit button for the form
        button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                # Read file content
                text = read_file(uploaded_file)
                
                # Count tokens and the cost of API call using LangChain callback
                with get_openai_callback() as cb:
                    # Call the function to generate MCQs
                    response = generate_evaluate_chain(
                        text=text,
                        number=mcq_count,
                        subject=subject,
                        tone=tone,
                        response_json=json.dumps(RESPONSE_JSON)
                    )
                
                # Display the response (MCQs generated)
                st.write(response)
            
            except Exception as e:
                # Handle exceptions and display the error
                st.error("An error occurred while generating MCQs.")
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            
            else:
                # Display token and cost details
                st.write(f"Total Tokens: {cb.total_tokens}")
                st.write(f"Prompt Tokens: {cb.prompt_tokens}")
                st.write(f"Completion Tokens: {cb.completion_tokens}")
                st.write(f"Total Cost: {cb.total_cost}")
                
                # Check if response is a dictionary and extract quiz data
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        
                        if table_data is not None:
                            # Convert table data to a DataFrame
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            # Display the table in Streamlit
                            st.table(df)
                            
                            # Display the review in a text area
                            st.text_area(label="Review", value=response.get("review", "No review available"))
                        else:
                            st.error("Error in the table data.")
                else:
                    st.write(response)
except Exception as e:
    st.error("An error occurred while loading the JSON file.")
    traceback.print_exception(type(e), e, e.__traceback__)                    