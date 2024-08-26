FROM python:3.12.4

RUN apt-get -y update && apt-get -y upgrade

RUN apt-get install -y ffmpeg

ENV HOME="/app"
WORKDIR ${HOME}

COPY . $HOME

RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "src/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]



