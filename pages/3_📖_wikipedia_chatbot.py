import streamlit as st
from streamlit_chat import message
import utils
import os    
    
if 'start_wiki_chat_button' not in st.session_state:
    st.session_state.start_wiki_chat_button = False

def click_button():
    st.session_state.start_wiki_chat_button = True
    st.session_state['chatbot'] = {}
    st.session_state['generated'] = ["Hello ! Ask me anything about uploaded wikipedia articles 🤗"]
    st.session_state['past'] = ["Hey ! 👋"]

st.title('Wikipedia chatbot')
st.text('Chat with multiple wikipedia articles by giving their titles.')

if st.session_state['model_params']:
    wiki_title = st.sidebar.text_input(label = 'Enter wikipedia article title for multiple titles seperate it by comma(,)')
    st.sidebar.button('start chat', on_click=click_button)
    if st.session_state['start_wiki_chat_button']:
        if wiki_title:
            if not st.session_state['chatbot']:
                with st.spinner('Processing documents...'):
                    data_folder = 'user_data'
                    utils.create_dir(data_folder)
                    
                    title_list = wiki_title.split(',')
                    title_list = list(set([i.strip() for i in title_list if i.strip()]))
                    wiki_content = utils.extract_wikipedia_content(title_list)
                    for idx,content in wiki_content.items():
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
