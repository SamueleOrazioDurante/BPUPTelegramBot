FROM python:3.10.12

WORKDIR /usr/src/app

RUN apt update && apt install -y \
        ffmpeg \
        flac \
        unzip \
        wget \
        espeak

COPY src/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src .

CMD ["python", "-u", "./main.py"]
