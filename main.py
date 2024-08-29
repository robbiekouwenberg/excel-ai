from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, Settings, download_loader
from pathlib import Path
import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO
)  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

api_key = os.getenv('AZ_OPENAI_API_KEY')
azure_endpoint = os.getenv('AZ_OPENAI_API')
api_version = os.getenv('AZ_OPENAI_API_VERSION')

llm = AzureOpenAI(
    model=os.getenv('AZ_OPENAI_MODEL'),
    deployment_name=os.getenv('AZ_OPENAI_MODEL_DEPLOYMENT'),
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

# You need to deploy your own embedding model as well as your own chat completion model
embed_model = AzureOpenAIEmbedding(
    model=os.getenv('AZ_OPENAI_EMBEDDING_MODEL'),
    deployment_name=os.getenv('AZ_OPENAI_EMBEDDING_MODEL_DEPLOYMENT'),
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_version,
)

Settings.llm = llm
Settings.embed_model = embed_model

PandasExcelReader = download_loader("PandasExcelReader")
loader = PandasExcelReader(pandas_config={ "header": None})
documents = loader.load_data(file=Path("path to\excel.xlsx"))

index = VectorStoreIndex.from_documents(documents)

query = "query."

query_engine = index.as_query_engine()
answer = query_engine.query(query)

print("--------------------")
print("query was:", query)
print("answer was:", answer)
print("--------------------")