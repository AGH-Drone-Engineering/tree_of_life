import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
#import NavSatFix
from sensor_msgs.msg import NavSatFix
import serial
from threading import Thread
import csv
# from config import *
import math
from doggy import Walk, Doggy, DoggyAction, walk_forward
from geoToLocal import geo_to_vector
from firebase_fun import *
import numpy as np

class Dog_data:
    def __init__(self) -> None:
        rospy.init_node('dog_control')
        self.rate = rospy.Rate(30)

        self.bridge = CvBridge()
        self.bridge_cam360 = CvBridge()
        # self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        self.gps_msg = NavSatFix()
        """
        PUBLISHERS
        """
        self.image_pub = rospy.Publisher('camera/image', Image, queue_size=10)
        self.image_pub_360 = rospy.Publisher('camera360/image', Image, queue_size=10)
        self.gps_pub = rospy.Publisher('gps/fix', NavSatFix, queue_size=10)
        # self.finished_mission_pub = rospy.Publisher('finished_drone_mission', Bool, queue_size=10)


        """
        SUBSRIBERS
        """
        self.sub_gps = rospy.Subscriber('gps/fix', NavSatFix, self.gps_callback)
        
        """
        INIT
        """

        self.inter_finished = 0
        self.last_latitude = None
        self.last_longitude = None
        self.last_timestamp = None

        self.finished_drone_mission = False

        """
        THREADS
        """
        # self.gps_data_thread = Thread(target=self.publisher_nav, args=())
        # self.gps_data_thread.daemon = True
        # self.gps_data_thread.start()

        self.camera_360 = Thread(target=self.publish_camera_video_360, args=())
        self.camera_360.daemon = True
        self.camera_360.start()

        self.mission_control = Thread(target=self.mission, args=())
        self.mission_control.daemon = True
        self.mission_control.start()


        #inicjalizacja psa i połączenia z nim
        self.doggy = Doggy()
        self.doggy.wait_connected()
        self.doggy.send_action(DoggyAction.WALK)

        self.start_mission = False

    def gps_callback(self, data):
        lat = data.latitude
        lon = data.longitude
        alt = data.altitude
        timestamp = data.header.stamp

        # Obliczanie prędkości
        speed = self.calculate_speed(lat, lon, timestamp)

        if speed is not None and speed != 0:
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
        if lat != 0 or lon != 0:
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
            self.rate.sleep()     
        camera.release()

    def publish_camera_video_360(self):
        rate = rospy.Rate(30)
        camera = cv2.VideoCapture(2) 
        while not rospy.is_shutdown():
            ret, frame = camera.read()

            if ret:
                # Konwersja ramki do formatu ROS
                image_msg = self.bridge_cam360.cv2_to_imgmsg(frame, encoding="bgr8")
                self.image_pub_360.publish(image_msg)
            rate.sleep()     
        camera.release()

    def publisher_nav(self):
        # def publish_gps_data():
        gps_msg = NavSatFix()
        # Inicjalizacja polaczenia z portem szeregowym
        ser = serial.Serial('/dev/ttyUSB0', 9600)  # Zmien '/dev/ttyUSB0' na odpowiedni port szeregowy i predkosc transmisji (baud rate) 
        #                                                                               I PO PODPIECIU DAC: sudo chmod 666 ${WSTAW NAZWE NASZEGO URZADZENIA}, bo inaczej sie pulta ze nie ma uprawnien

        rate = rospy.Rate(1)  # Czestotliwosc publikacji (10 Hz)

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
                        
                        gps_msg.header.stamp = rospy.Time.now()
                        gps_msg.latitude = lat
                        gps_msg.longitude = lon
                        gps_msg.altitude = alt
                        # Publikowanie danych GPS
                        
                    except ValueError:
                        pass
            self.gps_pub.publish(gps_msg)
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
        if d_time != 0:
            speed = distance / d_time
        else:
            speed = 0

        return speed

    def move_dog(self, x_target, y_target):
        #obliczenie pozycji celu względem psa (pies zawsze ma pozycję 0, 0)

        velocity, yaw_velocity = walk_forward(self.theta, [x_target, y_target], [0, 0])
        try:
            self.doggy.send_stick(0, velocity, yaw_velocity, 0)
            rospy.sleep(0.1)
            #obliczenie dystansu pomiędzy punktami
        except KeyboardInterrupt:
            for _ in range(10):
                rospy.sleep(0.1)
                self.doggy.send_stick(0, 0, 0, 0)

    def mission(self):
        while not rospy.is_shutdown() and self.start_mission == False:
            if is_drone_on_ground():
                self.start_mission = True
            else:
                if self.start_mission:
                    rospy.loginfo("DOG CAN START HIS MISSION")
                else:
                    rospy.logerror("ROSPY HAS PROBLEMS WITH COMMUNICATION")

        i = 0
        while not rospy.is_shutdown() and self.start_mission:
            # tutaj dać algorytm do optymalizacji punktow i jak ma ona przebiegac 
            points_to_walk = emum()
            #TODO dokonczyc to 
            target_i = points_to_walk[i]
            position_target_lat, position_target_lon = target_i
            x, y = geo_to_vector(self.position_dog_lat, self.position_dog_lon, position_target_lat, position_target_lon)
            if np.sqrt((x) ** 2 + (y) ** 2) < 1:
                i += 1
            else:
                self.move_dog(x, y)


if __name__ == '__main__':

    dog_control = Dog_data()

    dog_control.publish_camera_video()

