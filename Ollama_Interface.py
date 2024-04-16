import os
from llama_index.core.base.llms.types import ChatMessage
from llama_index.llms import ollama as ol
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings import huggingface
from dotenv import load_dotenv

# load in model and embedding functions, and knowledgebase dir
load_dotenv('pyBot.env')
MODEL = os.getenv('LLM_MODEL')
EMBEDDING = os.getenv('EMBED_FUNC')
K_DIR = os.getenv('KNOWLEDGE_BASE')

# Establish llm model and embedding function
Settings.llm = ol.Ollama(model=MODEL, request_timeout=1000.0)
Settings.embed_model = huggingface.HuggingFaceEmbedding(model_name=EMBEDDING)

# Load documents and use embedding function to vectorize
documents = SimpleDirectoryReader(K_DIR).load_data()
index = VectorStoreIndex.from_documents(
  documents,
  embed_model=Settings.embed_model,
  llm=Settings.llm,
  show_progress=True
)

# ask bot a question with the knowledgebase
def ask(user_string):
  query_engine = index.as_query_engine(llm=Settings.llm)
  response = query_engine.query(user_string)
  return response

# Ask bot a question without utilizing the knowledgebase
def question(user_string):
  message = [ChatMessage(role = "user", content = f"{user_string}")]
  response = Settings.llm.chat(messages=message)
  # response = Settings.llm.chat(messages=message)
  return response
