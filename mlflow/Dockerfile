FROM python:3.9.5-slim
RUN python -m pip install --upgrade pip && \
    pip install mlflow[extras] && \
    pip install psycopg2-binary
EXPOSE 5000
ENTRYPOINT ["mlflow"]