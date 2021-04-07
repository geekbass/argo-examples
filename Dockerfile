FROM python:slim
ENV WORK_DIR /opt/code
RUN python -m pip install --upgrade pip && \
    pip install Flask && \
    pip install requests
EXPOSE 5000
RUN mkdir -pv ${WORK_DIR}/tests
COPY ./app.py ${WORK_DIR}
COPY ./tests/ ${WORK_DIR}/tests
WORKDIR ${WORK_DIR}
