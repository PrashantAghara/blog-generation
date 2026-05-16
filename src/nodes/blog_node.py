from src.states.blog_state import BlogState


class BlogNode:
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            prompt = """
                You are an expert blog content writer. Use markdown formatting.
                Generate a blog title for the {topic}. This title should be creative and SEO Friendly. 
                Don't give suggestions or summary, just give a good and creative title.
            """
            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            return {"blog": {"title": response.content}}

    def content_generation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            prompt = """You are an expert blog content writer. Use markdown formatting.
                Generate a detailed blog content with detailed breakdown for the {topic}"""
            sys_prompt = prompt.format(topic=state["topic"])
            response = self.llm.invoke(sys_prompt)
            return {
                "blog": {"title": state["blog"]["title"], "content": response.content}
            }
