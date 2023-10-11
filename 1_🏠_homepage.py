import streamlit as st 
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

st.set_page_config(
    page_title="Chatbot",
    page_icon="👋",
)

st.title("Langchain Streamlit Multifunctional Chatbot")
# st.sidebar.markdown('**Features:**')

if "model_params" not in st.session_state:
    st.session_state["model_params"] = {} 
 
st.write('Enter below details to start using chatbot')
chat_model = st.selectbox(label = 'Select Chat Model', options = ['gpt-3.5-turbo','gpt-4'], index=0)
embedding_model = st.selectbox(label = 'Select embeddings Model', options = ['text-embedding-ada-002'], index=0)
openai_key = st.text_input(label = 'Enter openai key (only required if openai models selected)', value="", type="password")
if st.button("save details"):
    if (chat_model in ['gpt-3.5-turbo','gpt-4']) or (embedding_model in ['text-embedding-ada-002']):
        if not openai_key:
            st.error('Please enter valid openai key')
        else:
            if embedding_model in ['text-embedding-ada-002']:
                embeddings = OpenAIEmbeddings(model=embedding_model,openai_api_key=openai_key)
                st.session_state["model_params"]["embedding_model"] = embeddings
            else:
                pass
            if chat_model in ['gpt-3.5-turbo','gpt-4']: 
                llm = ChatOpenAI(model_name=chat_model,temperature=0.0, openai_api_key=openai_key)
                st.session_state["model_params"]["chat_model"] = llm
            else:
                pass
            st.success('Success. Now can start using all chat functions.')