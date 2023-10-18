FROM python:3.9

COPY ./app /app
COPY ./requirements.txt /requirements.txt

RUN apt-get update \
    && apt-get install -y \
    libgl1 \
    ffmpeg

RUN pip install -r requirements.txt

EXPOSE 5000

ENV PYTHONPATH $PWD

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]