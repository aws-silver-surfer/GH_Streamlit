
FROM python:3.7
#Set the working directory
WORKDIR /app

#Copy the requirements file to the working folder
COPY requirements.txt ./requirements.txt

#Install the dependencies
RUN pip install -r requiremts.txt

EXPOSE 8501

COPY . ./app

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]



