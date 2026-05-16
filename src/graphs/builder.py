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

    def build_language_graph(self):
        """
        Build a graph to generate a blog for topic and language
        """
        self.node = BlogNode(llm=self.llm)

        # Nodes
        self.graph.add_node("title_creation", self.node.title_creation)
        self.graph.add_node("content_generation", self.node.content_generation)
        self.graph.add_node("route", self.node.route)
        self.graph.add_node(
            "hind_translation",
            lambda state: self.node.translation({**state, "language": "hindi"}),
        )
        self.graph.add_node(
            "french_translation",
            lambda state: self.node.translation({**state, "language": "french"}),
        )

        # Edge
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "route")
        self.graph.add_conditional_edges(
            "route",
            self.node.route_decision,
            {"hindi": "hind_translation", "french": "french_translation"},
        )
        self.graph.add_edge("hind_translation", END)
        self.graph.add_edge("french_translation", END)
        return self.graph

    def setup_graph(self, topic, language):
        if topic:
            if language:
                return self.build_language_graph().compile()
            return self.build_topic_graph().compile()


## Below code is for Langsmith & Langgraph Studio
llm = GroqLLM().get_llm()
builder = GraphBuilder(llm)
graph = builder.build_language_graph().compile()
