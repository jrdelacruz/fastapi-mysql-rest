FROM python:3.12.2
WORKDIR /project
RUN git clone https://github.com/jrdelacruz/fastapi-mysql-rest.git .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"] 