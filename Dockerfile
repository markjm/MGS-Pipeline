FROM tensorflow/tensorflow:2.4.2

RUN pip --no-cache-dir install --upgrade "Pillow==8.2.0"

COPY label.py label.py
COPY assets assets

ENTRYPOINT python label.py