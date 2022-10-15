FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY pyproject.toml /app 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]



