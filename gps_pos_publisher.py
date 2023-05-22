import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
#import NavSatFix
from sensor_msgs.msg import NavSatFix
import serial
from threading import Thread
import csv
from config import *
from firebase_admin import credentials, firestore, initialize_app
from pobierz_punkty_z_bazy_do_listy import points_targets_finished_mission
import math

class Dog_data:
    def __init__(self) -> None:
        rospy.init_node('dog_control')
        self.rate = rospy.Rate(30)

        self.bridge = CvBridge()
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        self.gps_msg = NavSatFix()
        """
        PUBLISHERS
        """
        self.image_pub = rospy.Publisher('camera/image', Image, queue_size=10)
        self.gps_pub = rospy.Publisher('gps/fix', NavSatFix, queue_size=10)
        # self.finished_mission_pub = rospy.Publisher('finished_drone_mission', Bool, queue_size=10)


        """
        SUBSRIBERS
        """
        sub_gps = rospy.Subscriber('gps/fix', NavSatFix, self.gps_callback)
        self.inter_finished = 0

        self.last_latitude = None
        self.last_longitude = None
        self.last_timestamp = None

        self.finished_drone_mission = False
        self.gps_data_thread = Thread(target=self.publisher_nav, args=())
        self.gps_data_thread.daemon = True
        self.gps_data_thread.start()

    def gps_callback(self, data):
        lat = data.latitude
        lon = data.longitude
        alt = data.altitude
        timestamp = data.header.stamp

        # Obliczanie prędkości
        speed = self.calculate_speed(lat, lon, timestamp)

        if speed is not None:
            # Przetwarzanie prędkości
            # Tutaj można umieścić dowolny kod przetwarzania prędkości
            # Na przykład, wyświetlanie prędkości
            rospy.loginfo(f"Speed: {speed} m/s")

        # Aktualizacja poprzednich danych
        self.last_latitude = lat
        self.last_longitude = lon
        self.last_timestamp = timestamp
        # Przetwarzanie danych GPS
        # Tutaj mozna umiescic dowolny kod przetwarzania danych

        # Przykladowe dzialanie - wyswietlanie danych
        rospy.loginfo(f"Received GPS data: Latitude: {lat}, Longitude: {lon}, Altitude: {alt}")



    def publish_camera_video(self):
        camera = cv2.VideoCapture(0)  # Ustawienie parametru na 0 oznacza użycie domyślnej kamery

        while not rospy.is_shutdown():
        # Odczytanie ramki z kamery
            ret, frame = camera.read()

            if ret:
                # Konwersja ramki do formatu ROS
                image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
                self.image_pub.publish(image_msg)
                # Publikowanie obrazu            

            if self.finished_drone_mission == True and self.inter_finished == 0 :
                #pobierz dane z punktami z aplikacji oraz je wczytaj
                points_targets_and_finished_drone_mission = points_targets_finished_mission()
                if points_targets_and_finished_drone_mission[-1] == 1:
                    points_targets_and_finished_drone_mission.pop()
                    self.inter_finished += 1
                    rospy.loginfo("Mission accepted")

                    #tutaj dać algorytm do opymalizacji ścieżki
                else:
                    rospy.loginfo("WAIT FOR END OF DRONE MISSION")

                



            self.rate.sleep()

        
    
        
        camera.release()

    def publisher_nav(self):
        # def publish_gps_data():
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


    def calculate_speed(self, latitude, longitude, timestamp):
        if self.last_latitude is None or self.last_longitude is None or self.last_timestamp is None:
            # Brak poprzednich danych, nie można obliczyć prędkości
            return None

        # Obliczanie różnicy położeń
        d_latitude = latitude - self.last_latitude
        d_longitude = longitude - self.last_longitude

        # Obliczanie różnicy czasu w sekundach
        d_time = (timestamp - self.last_timestamp).to_sec()

        # Obliczanie odległości w metrach
        # Za pomocą wzoru haversine dla odległości na sferze
        earth_radius = 6371000  # Promień Ziemi w metrach
        a = math.sin(d_latitude / 2) ** 2 + math.cos(self.last_latitude) * math.cos(latitude) * math.sin(d_longitude / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c

        # Obliczanie prędkości w metrach na sekundę
        speed = distance / d_time

        return speed

if __name__ == '__main__':

    dog_control = Dog_data()

    dog_control.publish_camera_video()

