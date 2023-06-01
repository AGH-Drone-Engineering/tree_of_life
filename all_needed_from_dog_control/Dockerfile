FROM ros:noetic

RUN apt-get update && apt-get install -y python3-pip ros-noetic-cv-bridge

RUN pip3 install pyserial paho-mqtt firebase-admin pulp
RUN pip3 install pandas matplotlib scipy

COPY . .

CMD [ "/ros_entrypoint.sh", "python3", "gps_pos_publisher.py" ]
