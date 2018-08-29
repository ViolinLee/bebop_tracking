#!/usr/bin/env python
import rospy
import roslib
from geometry_msgs.msg import Twist
#from ardrone_autonomy.msg import Navdata
from bebop_tracker_control.msg import centroid

class bebopPIDController:
    def __init__(self, kp=0.0, ki=0.0, kd=0.0):
        self.yaw_p = kp
        #self.yaw_i = ki
        #self.yaw_d = kd

        self.goal_vel = 0.0
        self.centroid_x = 0
        self.centroid_y = 0

        self.centroid_sub = rospy.Subscriber("/face_centroid", centroid, self.goal_cb)
        self.vel_cmd_pub = rospy.Publisher("/bebop/cmd_vel", Twist, queue_size=1)
        

    def goal_cb(self, centroid):
        self.centroid_x = centroid.x
        self.centroid_y = centroid.y

    def yaw_controller():
        e = 0.0
        centroid_y = self.centroid_y
        center_y = 856/2

        difference_y = (centroid_y - center_y)  # in pixel with maximum==856
        
        if abs(difference_y) > 50: 
            e = difference_y/856 # maximum is 1.0
            

        yaw_cmd = self.yaw_p * e # maximum is 0.05

        return yaw_cmd

    def update(self):
        '''
        if self.last_time is None:
            self.last_time = rospy.Time.now()
            dt = 0.0
        else:
            time = rospy.Time.now()
            dt = (time - self.last_time).to_sec()
            self.last_time = time
       '''

        yaw_cmd = self.yaw_controller()
        
        cmd = Twist()
        cmd.angular.y = 0.0
        cmd.angular.x = 0.0
        cmd.angular.z = yaw_cmd
        cmd.linear.z = 0.0
        cmd.linear.x = 0.0
        cmd.linear.y = 0.0

        self.vel_cmd_pub.publish(cmd)


if __name__ == '__main__':
    rospy.init_node('bebop_controller')
    controller = bebopPIDController(kp=0.05)
    r = rospy.Rate(100)
    
    try:
        while not rospy.is_shutdown():
            #controller.update()
            r.sleep()
    except KeyboardInterrupt:
        print("Node Has Been Shut Down")


