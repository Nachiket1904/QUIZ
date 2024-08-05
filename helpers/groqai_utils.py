import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


def get_quiz_data(text, groq_api_key):
    template = """
    You are a helpful assistant programmed to generate questions based on any text provided. For every chunk of text you receive, you're tasked with designing 5 distinct questions. Each of these questions will be accompanied by 3 possible answers: one correct answer and two incorrect ones.

    For clarity and ease of processing, structure your response in a way that emulates a Python list of lists.

    Your output should be shaped as follows:

    1. An outer list that contains 5 inner lists.
    2. Each inner list represents a set of question and answers, and contains exactly 4 strings in this order:
    - The generated question.
    - The correct answer.
    - The first incorrect answer.
    - The second incorrect answer.

    Your output should mirror this structure:
    [
        ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2"],
        ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2"],
        ...
    ]

    It is crucial that you adhere to this format as it's optimized for further Python processing.
    """
    
    # Initialize ChatGroq with the desired model
    chat = ChatGroq(temperature=0.2, groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")

    try:
        # Define the prompt templates
        system_message_prompt = ChatPromptTemplate.from_messages([("system", template)])
        human_message_prompt = ChatPromptTemplate.from_messages([("human", "{text}")])

        # Combine the prompt templates into one
        chat_prompt = ChatPromptTemplate.from_messages([("system", template), ("human", "{text}")])

        # Define the chain using the chat instance and the combined prompt
        chain = chat_prompt | chat

        # Run the chain with the provided text
        quiz_data = chain.invoke({"text": text})

        # Extract the content as a string
        quiz_content = quiz_data.content

        return quiz_content
    
    except Exception as e:
        if "AuthenticationError" in str(e):
            st.error("Incorrect API key provided. Please check and update your API key.")
            st.stop()
        else:
            st.error(f"An error occurred: {str(e)}")
            st.stop()