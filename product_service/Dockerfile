FROM python:3.11-slim
WORKDIR /product_service
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "product_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
