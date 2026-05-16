from src.states.blog_state import BlogState, Blog
from langchain.messages import HumanMessage


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

    def translation(self, state: BlogState):
        """
        Translate the content to the specified language.
        """
        translation_prompt = """
        Translate the following content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}

        """
        print(state["language"])
        blog_content = state["blog"]["content"]
        messages = [
            HumanMessage(
                translation_prompt.format(
                    current_language=state["language"], blog_content=blog_content
                )
            )
        ]
        transaltion_content = self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog": {"content": transaltion_content}}

    def route(self, state: BlogState):
        return {"language": state["language"]}

    def route_decision(self, state: BlogState):
        if state["language"] == "hindi":
            return "hindi"
        elif state["language"] == "french":
            return "french"
        else:
            return state["language"]
