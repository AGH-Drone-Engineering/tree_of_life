#!/usr/bin/env python

# TRZEBA PAMIETAC O 

import rospy
from sensor_msgs.msg import NavSatFix
import serial

def publish_gps_data():
    # Inicjalizacja wezla ROS
    rospy.init_node('gps_publisher', anonymous=True)

    # Utworzenie publikera dla danych GPS
    gps_pub = rospy.Publisher('gps/fix', NavSatFix, queue_size=10)

    # Inicjalizacja polaczenia z portem szeregowym
    ser = serial.Serial('/dev/ttyUSB0', 9600)  # Zmien '/dev/ttyUSB0' na odpowiedni port szeregowy i predkosc transmisji (baud rate) 
    #                                                                               I PO PODPIECIU DAC: sudo chmod 666 ${WSTAW NAZWE NASZEGO URZADZENIA}, bo inaczej sie pulta ze nie ma uprawnien

    rate = rospy.Rate(10)  # Czestotliwosc publikacji (10 Hz)

    while not rospy.is_shutdown():
        # Odczytanie danych z GPS-a przez port szeregowy
        line = ""
        try:
            line = ser.readline().decode('ascii').strip()
        except UnicodeDecodeError:
            rospy.loginfo("Error when trying to decode, after another try it will be OK")
        # Przetwarzanie i publikowanie danych
        # zmienilem na GNGGA, bo to nasz typ
        if line.startswith('$GNGGA'):
            data = line.split(',')
            if len(data) >= 10:
                try:
                    lat = float(data[2]) / 100
                    lon = float(data[4]) / 100
                    alt = float(data[9])

                    # Tworzenie wiadomosci NavSatFix
                    gps_msg = NavSatFix()
                    gps_msg.header.stamp = rospy.Time.now()
                    gps_msg.latitude = lat
                    gps_msg.longitude = lon
                    gps_msg.altitude = alt
                    # Publikowanie danych GPS
                    gps_pub.publish(gps_msg)
                except ValueError:
                    rospy.loginfo("Error when converting, next time it will be OK")

        rate.sleep()

    # Zamykanie polaczenia z portem szeregowym
    ser.close()

if _name_ == '_main_':
    try:
        publish_gps_data()
    except rospy.ROSInterruptException:
        pass
