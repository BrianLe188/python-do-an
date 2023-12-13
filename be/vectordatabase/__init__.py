import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain.agents import Tool
from langchain.agents import initialize_agent

TEXT_FIELD = "text"
OPENAI_API_KEY = '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'
YOUR_API_KEY = '5cf20be0-6e9f-47ef-bef3-ffcd57011ab0'
YOUR_ENV = 'asia-southeast1-gcp-free'
INDEX_NAME = 'admission'

embed = OpenAIEmbeddings(
    # model=MODEL_NAME,
    openai_api_key=OPENAI_API_KEY
)
pinecone.init(
    api_key=YOUR_API_KEY,
    environment=YOUR_ENV
)

index = pinecone.Index(INDEX_NAME)
vectorstore = Pinecone(
    index, embed.embed_query, TEXT_FIELD
)

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model='gpt-3.5-turbo',
    temperature=0.0,
)
conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# tools = [
#     Tool(
#         name='Knowledge Base',
#         func=qa.run,
#         description=(
#             'use this tool when answering general knowledge queries to get '
#             'more information about the topic'
#         )
#     )
# ]
# agent = initialize_agent(
#     agent='chat-conversational-react-description',
#     tools=tools,
#     llm=llm,
#     verbose=True,
#     max_iterations=3,
#     early_stopping_method='generate',
#     memory=conversational_memory
# )