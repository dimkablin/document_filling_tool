FROM python:3.10.9

WORKDIR /document_filling_tool
COPY . /document_filling_tool

RUN apt-get update && apt-get upgrade -y
RUN apt-get install build-essential git python3 python3-pip wget --no-install-recommends -y

RUN apt-get update && apt-get install -y uvicorn && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
