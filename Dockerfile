FROM python:3.9
ADD recipe.py .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "./recipe.py"]