import os
import re
import tempfile

import openai
from langchain.document_loaders import PyPDFLoader
from moviepy.editor import VideoFileClip, vfx

from app.core.config import settings

URL_REGEX = (
    "(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?"
)

class PreProcessor:
    def __init__(self, mode):
        if mode not in ["pdf", "video"]:
            raise Exception("The mode must be one of pdf, video")
        self.mode = mode

    def run(self, source, is_ocr=False):
        if self.mode == "pdf":
            return self.get_pdf(source, is_ocr)
        #TODO: It should also correspond to formats other than mp4
        elif self.mode == "video":
            return self.get_mp4(source)

    def get_pdf(self, source, is_ocr=False):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(source)
        loader = PyPDFLoader(tmp_file.name, extract_images=is_ocr)
        pages = loader.load_and_split()
        os.remove(tmp_file.name)
        docs = self.concat_docs(pages)
        return docs

    def get_mp4(self, source):
        with tempfile.TemporaryDirectory() as td:
            tmp_video_path = os.path.join(td, "temp_video.mp4")
            tmp_audio_path = os.path.join(td, "temp_audio.mp3")

            with open(tmp_video_path, "wb") as tmp_video:
                tmp_video.write(source)
            video_clip = VideoFileClip(tmp_video_path)
            video_clip = video_clip.fx(vfx.speedx, 1.5)
            video_clip.audio.write_audiofile(tmp_audio_path)
            with open(tmp_audio_path, "rb") as tmp_audio:
                transcript = openai.Audio.transcribe("whisper-1", tmp_audio, api_key=settings.OPENAI_API_KEY)["text"]

        return transcript
    
    def concat_docs(self, pages):
        docs = ""
        for page in pages:
            content = page.page_content
            replace_content = re.sub(URL_REGEX, "", content)
            docs += replace_content
        return docs
    

def parsing_generation_output(source) -> list:
    problems= []
    items = [item for item in source.split('\n') if item]
    for i in range(0, len(items)//2):
        question = items[2*i].replace(f'Q{i+1}:', "").strip()
        answer =  items[2*i+1].replace(f'A{i+1}:', "").strip()
        problems.append({
            "problem_no": i+1,
            "question": question,
            "answer": answer})
    return problems