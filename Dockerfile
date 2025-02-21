# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports (FastAPI on 5000, Streamlit on 8501)
EXPOSE 5000 8501

# Run both FastAPI and Streamlit using supervisord
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 5000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
