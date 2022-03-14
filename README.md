# arXiv Intelligence NER Web Service

Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP).

# Install

## With Docker

    sudo docker build -t arxiv_intelligence_web_service .

## With Linux or Mac OS

### Dependencies: pdftotext

These instructions assume you're using Python 3 on a recent OS. Package names may differ for Python 2 or for an older OS.

#### Debian, Ubuntu, and friends

    sudo apt install build-essential libpoppler-cpp-dev pkg-config python3-dev

#### Fedora, Red Hat, and friends

    sudo yum install gcc-c++ pkgconfig poppler-cpp-devel python3-devel

#### macOS
    
    brew install pkg-config poppler python

### Web Service

#### Virtual environment

    python3 -m venv venv
    . venv/bin/activate

#### Spacy

    pip install --upgrade pip
    pip install -U pip setuptools wheel

With CPU:

    pip install -U spacy

If you prefer to use a GPU:

    pip install -U 'spacy[cuda114]'

Model:

    python3 -m spacy download en_core_web_sm

#### Web Service requirements:

    pip install -r requirements.txt

## With Windows OS

Sorry, this app is not currently compatible with Windows... Please use Docker instead.

## Credentials for AWS Comprehend setup

The current web service can use the AWS Comprehend.
If you would enable the AWS Comprehend, go in the 'config/config.ini' file 
and add the 'aws-comprehend' method to the parameter 'ner_methods'.
Example for AWS Comprehend + Spacy:

    ner_methods = aws-comprehend spacy

You will also need to connect to your AWS account (or AWS academy account).
For academy users, be sure to start the Lab.
Copy and past the content of the Cloud Access AWS CLI into ~/.aws/credentials
The file may look like:

    [default]
    aws_access_key_id=BLABLABLA
    aws_secret_access_key=BLABLABLA
    aws_session_token=BLABLABLA

# Run

## With Docker

    sudo docker run -d -p 5000:5000 arxiv_intelligence_web_service

## With Linux or Mac OS

### Production

    python3 main.py

### Development

    export FLASK_APP=web_service
    export FLASK_ENV=development
    flask run

# Usage

## Swagger

## curl

Ask the web service to process a PDF file from an URL:

    curl http://localhost:5000/?doc_url=https://arxiv.org/ftp/arxiv/papers/2201/2201.05599.pdf

Upload a PDF local file:

    curl -F 'file=@article.pdf' localhost:5000

Get PDF metadata:

    curl http://localhost:5000/document/metadata/1

Get PDF content:

    curl http://localhost:5000/document/content/1

# Test

## pylint

    apt install pylint
    export PYTHONPATH="venv/lib/python3.9/site-packages/"
    pylint --disable too-many-return-statements --disable too-many-instance-attributes --disable too-few-public-methods --disable too-many-locals --disable too-many-arguments --disable c-extension-no-member web_service/*

## pytest

    pip install '.[test]'
    pytest

Run with coverage report:

    export PYTHONPATH="venv/lib/python3.9/site-packages/"
    coverage run -m pytest
    coverage report
    coverage html  # open htmlcov/index.html in a browser
