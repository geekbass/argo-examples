FROM python:slim
ENV WORK_DIR /opt/code
RUN python -m pip install --upgrade pip && \
    pip install Flask
EXPOSE 5000
RUN mkdir -pv ${WORK_DIR}/
COPY ./app.py ${WORK_DIR}
WORKDIR ${WORK_DIR}
