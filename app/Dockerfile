FROM python:3.12
WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt
ENV FASTAPI "/app/main.py"
COPY . .
CMD ["python", "-m" , "fastapi", "run", "--host=0.0.0.0", "--port=8080"]