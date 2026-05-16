import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from src.graphs.builder import GraphBuilder
from src.llms.groq_llm import GroqLLM

load_dotenv()

app = FastAPI()

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


## API
@app.post("/blogs")
async def create_blogs(request: Request):
    data = await request.json()
    topic = data.get("topic", "")
    language = data.get("language", None)

    llm = GroqLLM().get_llm()

    graph_builder = GraphBuilder(llm=llm)

    if topic:
        graph = graph_builder.setup_graph(topic, language)
        state = graph.invoke({"topic": topic})

    return {"data": state}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
