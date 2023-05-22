#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from turtlesim.msg import Pose
from turtlesim.srv import Spawn, Kill, SetPen
from move_turtle.srv import moveTurtle, moveTurtleResponse
from math import atan2, pi, sqrt

class TurtleController():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_x = 0
        self.current_y = 0
        self.current_yaw = 0
        self.distance_threshold = 0.1
        self.angular_threshold = 0.1
        self.velocity = 1
        self.rate = rospy.Rate(10)

        self.pose_sub = rospy.Subscriber("/turtle1/pose", Pose, self.pose_callback)
        self.cmd_pub = rospy.Publisher("/turtle1/cmd_vel", Pose, queue_size=10)

        rospy.wait_for_service("/spawn")
        self.spawn_turtle = rospy.ServiceProxy("/spawn", Spawn)
        rospy.wait_for_service("/kill")
        self.kill_turtle = rospy.ServiceProxy("/kill", Kill)
        rospy.wait_for_service("/turtle1/set_pen")
        self.set_pen = rospy.ServiceProxy("/turtle1/set_pen", SetPen)

    def pose_callback(self, msg):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_yaw = msg.theta

    def move_to_point(self, x, y):
        dx = x - self.current_x
        dy = y - self.current_y
        target_yaw = atan2(dy, dx)
        dyaw = target_yaw - self.current_yaw
        while dyaw < -pi:
            dyaw += 2*pi
        while dyaw > pi:
            dyaw -= 2*pi
        while abs(dyaw) > self.angular_threshold:
            cmd = Pose()
            cmd.angular.z = self.velocity*dyaw
            self.cmd_pub.publish(cmd)
            dyaw = target_yaw - self.current_yaw
            while dyaw < -pi:
                dyaw += 2*pi
            while dyaw > pi:
                dyaw -= 2*pi
            self.rate.sleep()
        distance = sqrt(dx**2 + dy**2)
        while distance > self.distance_threshold:
            cmd = Pose()
            cmd.linear.x = self.velocity
            self.cmd_pub.publish(cmd)
            distance = sqrt((x-self.current_x)**2 + (y-self.current_y)**2)
            self.rate.sleep()

    def run(self):
        for i in range(len(self.x)):
            self.move_to_point(self.x[i], self.y[i])
        result = "Done moving turtle"
        return result

def handle_move_turtle(req):
    turtle_controller = TurtleController(req.x, req.y)
    result = turtle_controller.run()
    return moveTurtleResponse(result)

def move_turtle_server():
    rospy.init_node("move_turtle_server")
    rospy.Service("/move_turtle", moveTurtle, handle_move_turtle)
    rospy.spin()

if __name__ == "__main__":
    move_turtle_server()
