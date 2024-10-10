FROM python:3.10.12

WORKDIR /usr/src/app

RUN apt update && apt install -y \
        ffmpeg \
        flac \
        unzip \
        wget

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN wget "https://alphacephei.com/vosk/models/vosk-model-it-0.22.zip"
RUN unzip vosk-model-it-0.22.zip
RUN rm vosk-model-it-0.22.zip

COPY . .

CMD ["python", "-u", "./main.py"]
