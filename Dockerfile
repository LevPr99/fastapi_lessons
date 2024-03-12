FROM python:3.12.2-bullseye

WORKDIR /code

COPY ./resources/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./resources /code/resources

CMD ["uvicorn", "app.fastapi_main:app", "--host", "0.0.0.0", "--port", "80"]
