# Use the python image
FROM python:3.13

# Create the app directory to run our code
RUN mkdir /app

# Set the created directory as the working directory of our container
WORKDIR /app

# Set the env variables
# Prevents python from writing back to the hard disk
ENV PYTHONDONTWRITEBYTECODE=1

# Prevents python from buffering stdout and stderr
ENV PYTHONBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Copy the system requirements and install dependencies
COPY requirements.txt /app/

# Run a command to install the dependencies
RUN pip install -r --no-cache-dir requirements.txt

# Copy the django project to the container
COPY . /app/

# Expose the django port
EXPOSE 8000

# Run django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
