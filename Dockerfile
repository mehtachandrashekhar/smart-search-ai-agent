# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies
RUN pip install streamlit python-dotenv tiktoken

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Set environment variables
ENV SERPAPI_KEY=${SERPAPI_KEY}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV GOOGLE_CREDENTIALS_PATH=${GOOGLE_CREDENTIALS_PATH}
ENV GROQ_API_KEY=${GROQ_API_KEY}
ENV GROQ_API_URL=${GROQ_API_URL}
ENV GROQ_MODEL=${GROQ_MODEL}
ENV GROQ_MAX_TOKENS=${GROQ_MAX_TOKENS}
ENV GROQ_CONTEXT_MAX_TOKENS=${GROQ_CONTEXT_MAX_TOKENS}

# Run the Streamlit app
CMD ["streamlit", "run", "app/main.py"]
