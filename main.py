"""
import uvicorn
from fastapi import FastAPI
from backedn.database import models, database
from backedn.routes import llms,agent,tools,workfows
from fastapi.middleware.cors import CORSMiddleware
#from src.openagi.actions.tools import youtubesearch
#from src.openagi.actions.tools.ddg_search import DuckDuckGoSearch
#from src.openagi.agent import Admin
#from src.openagi.llms.groq import GroqModel
#from src.openagi.memory import Memory
#from src.openagi.planner.task_decomposer import TaskPlanner

app = FastAPI(title="AI Agent API with OpenAGI")


origins=[
    "https://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





# Create database tables on startup
models.Base.metadata.create_all(bind=database.engine)

# Include API routes
app.include_router(llms.router, prefix="/llms", tags=["LLMs"])
#app.include_router(llms.router, prefix="/llms", tags=["LLMs"])
#app.include_router(tools.router, prefix="/tools", tags=["Tools"])
#app.include_router(workfows.router, prefix="/workfows", tags=["Workfows"])

#app.include_router(youtubesearch.router, prefix="/youtubesearch", tags=["YouTube Search"])


@app.get("/")
def root():
    return {"message": "AI Agent API is running with OpenAGI"}

@app.get("/hello")
def hello():
    return {"message:" "AI agent api is running with openaAGI"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
"""


from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

parser=StrOutputParser()

##create chain
chain=prompt_template|model|parser



## App definition
app=FastAPI(title="Langchain Server",
            version="1.0",
            description="A simple API server using Langchain runnable interfaces")

## Adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=5000)


