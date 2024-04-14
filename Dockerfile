FROM python:3.12.2
ARG CACHEBUST=$(date +%s)
WORKDIR /project
RUN git clone https://github.com/jrdelacruz/fastapi-mysql-rest.git .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","run.py"] 