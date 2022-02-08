# arXiv Intelligence NER Web Service

Web service specialized in Named Entity Recognition (NER), in Natural Language Processing (NLP).

# Install

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

Create a virtualenv and activate it:

    python3 -m venv venv
    python3 -m spacy download en_core_web_sm
    . venv/bin/activate

Install arXiv Intelligence NER Web Service:

    pip install -r requirements.txt

## With Windows OS

Sorry, this app is not currently compatible with Windows... Please use Docker instead.

## Credentials for AWS Comprehend setup

Connect to your AWS account (or AWS academy account).
For academy users, be sure to start the Lab.
Copy and past the content of the Cloud Access AWS CLI into ~/.aws/credentials
The file may look like:

    [default]
    aws_access_key_id=BLABLABLA
    aws_secret_access_key=BLABLABLA
    aws_session_token=BLABLABLA

# Run

## With Linux or Mac OS

    export FLASK_APP=web_service
    export FLASK_ENV=development
    flask run

# Usage

    curl http://localhost:5000/?doc_url=https://arxiv.org/ftp/arxiv/papers/2201/2201.05599.pdf
    curl http://localhost:5000/?doc_url=file:///home/myuser/arxiv_intelligence_ner_ws/tests/article.pdf
    curl -F 'file=@article.pdf' localhost:5000

# Test

## pylint

    apt install pylint
    export PYTHONPATH="venv/lib/python3.9/site-packages/"
    pylint --disable too-many-instance-attributes --disable too-few-public-methods --disable too-many-locals --disable too-many-arguments --disable c-extension-no-member web_service/*

## pytest

    pip install '.[test]'
    pytest

Run with coverage report:

    export PYTHONPATH="venv/lib/python3.9/site-packages/"
    coverage run -m pytest
    coverage report
    coverage html  # open htmlcov/index.html in a browser
