from langchain.prompts import PromptTemplate

summarization_prompt_template = PromptTemplate.from_template(
    """
You are responsible for summarizing the lecture materials of your major in a way that is easy for students to understand. Please organize and summarize the given sentences, and ignore external links and unnecessary words. script: {docs}
"""
)


generation_prompt_template = PromptTemplate.from_template(
    """
You are responsible for creating 10 questions to help students understand the summarized lecture materials of your major.
Avoid non-essential questions.
Questions should be short answer or essay format.
Technical terms and proper nouns related to major should be used in English. Generate answers to questions concisely, focusing on keywords.
The output format is as follows.

Output format:

Q1: Content of question 1
A1: Content of answer 1

Q2: Content of question 2
A2: Content of answer 2

Q3 Content of question 2
A3: Content of answer 2

script: {summary}"""
)

translation_prompt_template = PromptTemplate.from_template(
    """
Translate the given sentences into Korean in a natural way, following the format. Keep technical terms and proper nouns in English.
{script}
"""
)

prompt_templates: dict = {
    "summarization": summarization_prompt_template,
    "generation": generation_prompt_template,
    "translation": translation_prompt_template,
}
