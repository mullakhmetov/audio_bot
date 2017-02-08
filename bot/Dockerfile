FROM python:3.5-onbuild

ADD deb.multimedia.org.list /etc/apt/sources.list.d/deb.multimedia.org.list
RUN apt-get update && apt-get install -y --force-yes libimage-exiftool-perl ffmpeg

ENTRYPOINT ["python", "-u", "app.py"]
