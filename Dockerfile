FROM python:3.6
ADD game.py /
RUN pip install pygame==3.7
CMD [ "python", "./game.py" ]