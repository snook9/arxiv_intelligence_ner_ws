FROM debian:11

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install dependencies and pip requirements
COPY requirements.txt .
RUN apt-get update -q -y
RUN apt-get install -yf \
    build-essential libpoppler-cpp-dev pkg-config python3-dev \
    python3 \
    python3-pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -U pip setuptools wheel
RUN python3 -m pip install -U spacy
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["python3", "main.py"]
