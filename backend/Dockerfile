FROM python:3.12.7

RUN mkdir /vex_service

WORKDIR /vex_service

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000"]
