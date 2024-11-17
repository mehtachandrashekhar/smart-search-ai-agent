# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port that Streamlit runs on
EXPOSE 8501

# Define environment variables
ENV STREAMLIT_SERVER_PORT=8501

# Run the Streamlit application
CMD ["streamlit", "run", "app/main.py"]
