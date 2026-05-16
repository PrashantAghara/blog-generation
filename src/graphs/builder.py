from langgraph.graph import StateGraph, START, END
from src.llms.groq_llm import GroqLLM
from src.states.blog_state import BlogState
from src.nodes.blog_node import BlogNode


class GraphBuilder:
    def __init__(self, llm):
        self.llm = llm
        self.graph = StateGraph(BlogState)

    def build_topic_graph(self):
        """
        Build a graph to generate a blog for a topic
        """
        self.node = BlogNode(llm=self.llm)

        self.graph.add_node("title_creation", self.node.title_creation)
        self.graph.add_node("content_generation", self.node.content_generation)

        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)

        return self.graph

    def setup_graph(self, topic, language):
        if topic and language:
            pass

        if topic:
            return self.build_topic_graph().compile()


## Below code is for Langsmith & Langgraph Studio
llm = GroqLLM().get_llm()
builder = GraphBuilder(llm)
graph = builder.build_topic_graph().compile()
