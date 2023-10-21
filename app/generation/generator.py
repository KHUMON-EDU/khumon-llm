import os

from langchain.chat_models import ChatOpenAI

from app.core.config import settings
from app.generation.prompts import prompt_templates


class Generator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo-16k",
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY,
        )

    def run(self, docs: str) -> dict:
        summarization_prompt = prompt_templates["summarization"].format(
            docs=docs[:10000]
        )
        summary = self.llm.predict(summarization_prompt)

        generation_prompt = prompt_templates["generation"].format(summary=summary)
        generation = self.llm.predict(generation_prompt)

        translation_prompt = prompt_templates["translation"].format(script=generation)
        translate_generation = self.llm.predict(translation_prompt)

        return {"summary": summary, "generation": translate_generation}
