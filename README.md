# Langchain openai chatbot web app using streamlit

This is a web application for a language model chatbot using Streamlit.

## Overview

🤖 This web application features a chatbot utilizing Streamlit, Langchain, FAISS, and OpenAI.

## Highlights

1. Multi doc upload and chat support. 📂💬
2. Chat with YouTube video scripts 🎥📝
3. Chat with Arxiv papers 📚📑
4. Chat with Wikipedia articles 📖📑
5. Chat history memory support. 📚🧠

## Coming Soon

1. Support for csv and more. 📺📖
2. Integration with llama2 llm. 🦙

## Prerequisites

1. Python 3.10
2. Streamlit
3. Langchain
4. OpenAI key

## Setup
1. Clone the repository:

    ```bash
    git clone https://github.com/Nakul74/llm-chatbot.git
    ```

2. Create a Conda environment with the specified version of Python from the `runtime.txt` file:

    ```bash
    conda create -p ./envs $(cat runtime.txt) -y
    ```

3. Activate the environment:

    ```bash
    conda activate envs/
    ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Use the following command to run the application:

```bash
streamlit run app.py
```
