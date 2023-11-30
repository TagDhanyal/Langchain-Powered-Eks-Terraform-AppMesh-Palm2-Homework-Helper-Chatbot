FROM python:3.11-slim

WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
