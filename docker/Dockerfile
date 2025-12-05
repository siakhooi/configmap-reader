FROM python:3.13-slim

RUN useradd -m  appuser

COPY *.whl /tmp/
RUN pip install --no-cache-dir /tmp/configmap_reader-*-py3-none-any.whl && rm /tmp/*.whl

EXPOSE 8000
ENV CONFIG_DIR=/config
USER appuser
CMD ["configmap-reader"]
