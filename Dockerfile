FROM ubuntu:20.04

ADD helper.py .
ADD ui.py . 
ADD depth_map_to_point_cloud.py .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libqt5gui5 qt5-default python3.8-minimal python3-pip -y
RUN rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
ENV QT_DEBUG_PLUGINS=1

CMD ["python", "./ui.py"]