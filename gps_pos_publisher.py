import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import NavSatFix
import serial

class Dog_data:
    def __init__(self) -> None:
        self.bridge = CvBridge()
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        
        self.image_pub = rospy.Publisher('camera/image', Image, queue_size=10)
        self.gps_pub = rospy.Publisher('gps/fix', NavSatFix, queue_size=10)
        
    def publish_camera_video(self):
        camera = cv2.VideoCapture(0)  # Ustawienie parametru na 0 oznacza użycie domyślnej kamery

        while not rospy.is_shutdown():
        # Odczytanie ramki z kamery
            ret, frame = camera.read()

            if ret:
                # Konwersja ramki do formatu ROS
                image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")

                # Publikowanie obrazu
                self.image_pub.publish(image_msg)

            
            line = ""
            try:
                line = self.ser.readline().decode('ascii').strip()
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
                        self.gps_pub.publish(gps_msg)
                    except ValueError:
                        rospy.loginfo("Error when converting, next time it will be OK")

            rate.sleep()

        
        self.ser.close()
        camera.release()

# def publish_camera_video():
#     # Inicjalizacja węzła ROS
#     rospy.init_node('camera_publisher', anonymous=True)

#     # Utworzenie publikera dla obrazu
#     # image_pub = rospy.Publisher('camera/image', Image, queue_size=10)

#     # Inicjalizacja kamery
#     camera = cv2.VideoCapture(0)  # Ustawienie parametru na 0 oznacza użycie domyślnej kamery

#     # Inicjalizacja konwertera OpenCV do ROS
#     bridge = CvBridge()

#     rate = rospy.Rate(30)  # Częstotliwość publikacji (30 Hz)

#     while not rospy.is_shutdown():
#         # Odczytanie ramki z kamery
#         ret, frame = camera.read()

#         if ret:
#             # Konwersja ramki do formatu ROS
#             image_msg = bridgex.cv2_to_imgmsg(frame, encoding="bgr8")

#             # Publikowanie obrazu
#             image_pub.publish(image_msg)

#         rate.sleep()

#     # Zatrzymanie kamery po zakończeniu publikacji
#     camera.release()


# def publish_gps_data():
#     # Inicjalizacja wezla ROS
#     rospy.init_node('gps_publisher', anonymous=True)

#     # Utworzenie publikera dla danych GPS
#     gps_pub = rospy.Publisher('gps/fix', NavSatFix, queue_size=10)

#     # Inicjalizacja polaczenia z portem szeregowym
#     ser = serial.Serial('/dev/ttyUSB0', 9600)  # Zmien '/dev/ttyUSB0' na odpowiedni port szeregowy i predkosc transmisji (baud rate) 
#     #                                                                               I PO PODPIECIU DAC: sudo chmod 666 ${WSTAW NAZWE NASZEGO URZADZENIA}, bo inaczej sie pulta ze nie ma uprawnien

#     rate = rospy.Rate(10)  # Czestotliwosc publikacji (10 Hz)

#     while not rospy.is_shutdown():
#         # Odczytanie danych z GPS-a przez port szeregowy
#         line = ""
#         try:
#             line = ser.readline().decode('ascii').strip()
#         except UnicodeDecodeError:
#             rospy.loginfo("Error when trying to decode, after another try it will be OK")
#         # Przetwarzanie i publikowanie danych
#         # zmienilem na GNGGA, bo to nasz typ
#         if line.startswith('$GNGGA'):
#             data = line.split(',')
#             if len(data) >= 10:
#                 try:
#                     lat = float(data[2]) / 100
#                     lon = float(data[4]) / 100
#                     alt = float(data[9])

#                     # Tworzenie wiadomosci NavSatFix
#                     gps_msg = NavSatFix()
#                     gps_msg.header.stamp = rospy.Time.now()
#                     gps_msg.latitude = lat
#                     gps_msg.longitude = lon
#                     gps_msg.altitude = alt
#                     # Publikowanie danych GPS
#                     gps_pub.publish(gps_msg)
#                 except ValueError:
#                     rospy.loginfo("Error when converting, next time it will be OK")

#         rate.sleep()

#     # Zamykanie polaczenia z portem szeregowym
#     ser.close()
if __name__ == '__main__':
    # try:
    #     publish_camera_video()
    # except rospy.ROSInterruptException:
    #     pass
    dog_control = Dog_data()

    rate = rospy.rate(30)
    dog_control.publish_camera_video()

