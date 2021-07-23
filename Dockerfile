FROM python:3.8

# Set work directory for /app
WORKDIR /app

# Copy contents into container /app
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Port that container exposes to the world
EXPOSE 5000

# Run app.py
CMD ["python", "./app.py"]