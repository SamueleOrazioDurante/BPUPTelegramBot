FROM python:3.10.12

WORKDIR /usr/src/app

RUN apt update && apt install -y \
        ffmpeg \
        flac

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "./main.py"]
