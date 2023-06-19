FROM python:3.11-slim
LABEL org.opencontainers.image.source https://github.com/ondrejsika/demo-cloud-provider
RUN pip install --upgrade pip && \
    pip install pipenv && \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install
COPY . .
CMD [ "./uwsgi.sh" ]
EXPOSE 8000
