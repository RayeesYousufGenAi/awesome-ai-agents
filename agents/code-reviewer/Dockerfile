FROM python:3.11-slim

WORKDIR /app

COPY app.py requirements.txt README.md ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
