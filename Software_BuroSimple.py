import os.path
import json

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core.settings import Settings
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.indices import VectorStoreIndex, load_index_from_storage
from llama_index.core.storage import StorageContext

from llama_index.core import PromptTemplate

import configparser

# Creamos el configurador
config = configparser.ConfigParser()
config.read('./Config/config.ini')

# Leemos los datos del archivo de configuración
llm = config['Modelos']['llm']
embed_model = config['Modelos']['embedding']
PERSIST_DIR = config['Rutas']['almacenamiento_embedding'] # En este directorio se guarda el embedding de la colección (si ya existe se carga y, si no, se crea)
DATA_DIR = config['Rutas']['directorio_corpus'] # De este directorio se cargan los documentos para crear el índice a partir de ellos
DICT_ENLACES_DIR = config['Rutas']['diccionario_enlaces']
clave_openai = config['Keys']['clave_openai']
K = int(config['Parametros']['k_mas_similares'])

# Establecemos una variable de entorno (solo para esta sesión, no a nivel de sistema operativo) para la clave de la API de OpenAI
os.environ['OPENAI_API_KEY'] = clave_openai

# Definimos el LLM y el modelo de embedding que va a utilizarse
Settings.llm = OpenAI(model=llm)
Settings.embed_model = OpenAIEmbedding(model=embed_model)


# Comprobamos si ya existe un índice almacenado

# Si no existe, debe crearse
if not os.path.exists(PERSIST_DIR):
    # carga los documentos y crea el índice
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # almacena el índice
    index.storage_context.persist(persist_dir=PERSIST_DIR)

# Si existe, lo cargamos
else:
    # carga el índice
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Crea el motor de consultas
query_engine = index.as_query_engine(similarity_top_k=K)

# Creamos la descripción del prompt de acuerdo a la plantilla que propone LlamaIndex: https://docs.llamaindex.ai/en/stable/module_guides/models/prompts/usage_pattern/
descripcion_prompt = (

    "La información de contexto está debajo.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Responde la consulta como si fueras el asistente de la sede electrónica del ayuntamiento de Jaén.\n"
    "Consulta: {query_str}\n"
    'Si no puedes dar una respuesta útil, tu respuesta debe ser: "Lo siento, no tengo información suficiente para responder esa pregunta".'
)

# Instanciamos la plantilla
nuevo_prompt = PromptTemplate(descripcion_prompt)

# Actualizamos el prompt del motor de consulta
query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": nuevo_prompt}
)

# Ejecución de consulta
response = query_engine.query("hola")
print(response)

# Sacamos la similitud de los nodos recuperados
for nodo in response.source_nodes:
    print(nodo.get_score())

# Metadatos/enlaces
print("\n-------------- Enlaces de interés --------------\n")

# Obtenemos los documentos que han intervenido en la respuesta
claves = list(response.metadata.keys())
documentos_fuente = []
for key in claves:
    fichero = response.metadata[key]['file_name']
    if fichero not in documentos_fuente:
        documentos_fuente.append(fichero)

# Cargamos el diccionario {documento: enlace}
diccionario_enlaces = {}
with open(DICT_ENLACES_DIR, 'r') as f:
    diccionario_enlaces = json.load(f)

# Mostramos enlaces de las fuentes
for fichero in documentos_fuente:
    print(f"{fichero}   ->   {diccionario_enlaces[fichero]}")