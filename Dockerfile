FROM python:3.6

EXPOSE 5000

WORKDIR /code

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /code

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]