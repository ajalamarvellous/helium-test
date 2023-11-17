# use official python runtime as a parent image
FROM python:3.8

# set the working directory in the container to /app
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt ./ 
COPY /src ./src
COPY /models ./MODELS 

# install dependencies
RUN pip install -r requirements.txt

RUN apt-get update 

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


