FROM python:3.10

WORKDIR /code

COPY ./pyproject.toml ./poetry.lock /code/

RUN pip install --no-cache-dir poetry && poetry config virtualenvs.in-project true && poetry install

COPY ./ /code/

CMD ["python", "run.py"]