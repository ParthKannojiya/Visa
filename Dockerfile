FROM python:3.10
# Set working directory inside container
WORKDIR /app
# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the entire app source code
COPY . .
# Run the FastAPI app using uvicorn (pointing to app.py)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
