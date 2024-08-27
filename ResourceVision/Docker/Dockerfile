FROM python:3.9.19-slim-bookworm

COPY . /app

WORKDIR /app

RUN pip install -r requirement.txt

CMD ["python", "manage.py", "runserver"]
