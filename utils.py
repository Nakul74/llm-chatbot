from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader,YoutubeLoader,ArxivLoader,WikipediaLoader,NewsURLLoader
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS 
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks import get_openai_callback
import os

def load_memory(llm_model):
    memory = ConversationBufferMemory(llm=llm_model,memory_key="chat_history",return_messages=True)
    return memory

def load_retriever(docs,embedding_model):
    vectorstore = FAISS.from_documents(documents=docs, embedding=embedding_model)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    return retriever

def load_conversation_bot(llm_model,retriever,memory):
    chatbot = ConversationalRetrievalChain.from_llm(llm_model, retriever=retriever, memory=memory, verbose=True)
    return chatbot
    
def get_chatbot_response(chatbot,user_input):
    with get_openai_callback() as cb:
        output = chatbot({"question": user_input})["answer"]
        tokens_used = cb.total_tokens
    return output,tokens_used
    
def extract_arxiv_content(id_list):
    d = {}
    for arxiv_id in id_list:
        loader = ArxivLoader(query=arxiv_id)
        docs = loader.load()
        content = [i.page_content for i in docs]
        d[arxiv_id] = ' '.join(content)
    return d

def extract_wikipedia_content(title_list):
    d = {}
    for title in title_list:
        loader = WikipediaLoader(query=title)
        docs = loader.load()
        content = [i.page_content for i in docs]
        d[title] = ' '.join(content)
    return d

def extract_youtube_transcript(id_list):
    d = {}
    for video_id in id_list:
        loader = YoutubeLoader(video_id)
        docs = loader.load()
        transcript = [i.page_content for i in docs]
        d[video_id] = ' '.join(transcript)
    return d

def extract_news_from_url(url_list):
    d = {}
    for idx,url in enumerate(url_list):
        loader = NewsURLLoader(urls=[url])
        docs = loader.load()
        transcript = [i.page_content for i in docs]
        d[str(idx+1)] = ' '.join(transcript)
    return d
    
def create_dir(path):
    os.makedirs(path,exist_ok=True)
    file_list = os.listdir(path)
    for file in file_list:
        os.remove(os.path.join(path,file))
        
def load_docs(directory):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents

def split_docs(documents,chunk_size=1000,chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs