import streamlit as st
from streamlit_chat import message
import utils
import os    
    
if 'start_arxiv_chat_button' not in st.session_state:
    st.session_state.start_arxiv_chat_button = False

def click_button():
    st.session_state.start_arxiv_chat_button = True
    st.session_state['chatbot'] = {}
    st.session_state['generated'] = ["Hello ! Ask me anything about uploaded arxiv paper ids 🤗"]
    st.session_state['past'] = ["Hey ! 👋"]

st.title('Arxiv chatbot')
st.text('Chat with multiple arxiv paper by giving their ids.')

if st.session_state['model_params']:
    arxiv_id = st.sidebar.text_input(label = 'Enter arxiv paper id for multiple ids seperate it by comma(,)')
    st.sidebar.button('start chat', on_click=click_button)
    if st.session_state['start_arxiv_chat_button']:
        if arxiv_id:
            if not st.session_state['chatbot']:
                with st.spinner('Processing documents...'):
                    data_folder = 'user_data'
                    utils.create_dir(data_folder)
                    
                    id_list = arxiv_id.split(',')
                    id_list = list(set([i.strip() for i in id_list if i.strip()]))
                    arxiv_content = utils.extract_arxiv_content(id_list)
                    for idx,content in arxiv_content.items():
                        with open(os.path.join(data_folder, idx+'.txt'), "w") as f:
                            f.write(content)
                    
                    documents = utils.load_docs(data_folder)
                    docs = utils.split_docs(documents)
                    
                    embedding_model = st.session_state["model_params"]["embedding_model"]
                    retriever = utils.load_retriever(docs,embedding_model)
                    
                    llm_model = st.session_state["model_params"]["chat_model"]
                    memory = utils.load_memory(llm_model)
                    
                    st.session_state['chatbot'] = utils.load_conversation_bot(llm_model,retriever,memory)
            #         print('Not cached')
            # else:
            #     print('using cache bot')
            
            response_container = st.container()
            container = st.container()
            
            with container:
                with st.form(key='input_form', clear_on_submit=True):
                    
                    user_input = st.text_input("Query:", placeholder="Chat with your pdf,txt data here", key='input')
                    submit_button = st.form_submit_button(label='Send')
                    
                if submit_button and user_input:
                    output,tokens_used = utils.get_chatbot_response(st.session_state['chatbot'],user_input)
                    
                    st.session_state['past'].append(user_input)
                    st.session_state['generated'].append(output+ f'\nTokens used: {tokens_used}')

            if st.session_state['generated']:
                with response_container:
                    for i in range(len(st.session_state['generated'])):
                        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                        message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")
                        
        else:
            st.error('Input data missing')
else:
    st.error("No models added. Please visit homepage and add models")
