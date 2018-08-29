#!/usr/bin/env python
import rospy
import roslib
from geometry_msgs.msg import Twist
from bebop_tracker_control.msg import centroid


# v1 -> control yaw:

class bebopPIDController:
    def __init__(self):
        self.yaw_p = 0.0
        #self.yaw_i = ki
        self.yaw_d = 0.0

        self.centroid_x = 0
        self.centroid_y = 0
        
        self.last_difference_x = 0.0

        self.centroid_sub = rospy.Subscriber("/face_centroid", centroid, self.update)
        self.vel_cmd_pub = rospy.Publisher("/bebop/cmd_vel", Twist, queue_size=1)

    def yaw_controller(self):
        #e = 0.0
        
        centroid_x = self.centroid_x
        
        
        difference_x = (center_x - centroid_x)  # maximum==428 pixel
        difference_x_dot = difference_x - self.last_difference_x  # maximum=0.1s*1.0degree/s*428/40=-1pixel/1T
      
        e = difference_x/428.0 # maximum is 1.0
        e_dot = difference_x_dot/0.1 # minimum is -10.0
        
        if not self.last_difference_x == 0.0:
            yaw_cmd = self.yaw_p * e + self.yaw_d * e_dot
        # p item: maximum is 1.0  -> max speed is 1.0 degree/s
        # d item: 
        else:
            yaw_cmd = self.yaw_p * e

        self.last_difference_x = difference_x

        return yaw_cmd


    def update(self, centroid):
        
        #print("Execute callback function--update")
        self.centroid_x = centroid.x
        self.centroid_y = centroid.y
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
        cmd.angular.y = 0.0  # no works
        cmd.angular.x = 0.0  # no works
        cmd.angular.z = yaw_cmd
        cmd.linear.z = 0.0
        cmd.linear.x = 0.0
        cmd.linear.y = 0.0

        self.vel_cmd_pub.publish(cmd)

def main():
    rospy.init_node('bebop_controller')
    controller = bebopPIDController()
    controller.yaw_p = 0.5
    controller.yaw_d = 0.05
    
    global center_x
    global center_y

    center_x = 428
    center_y = 240

    '''
    cmd_hover = Twist()
    cmd_hover.angular.y = 0.0
    cmd_hover.angular.x = 0.0
    cmd_hover.angular.z = 0.0
    cmd_hover.linear.z = 0.0
    cmd_hover.linear.x = 0.0
    cmd_hover.linear.y = 0.0
    '''

    r = rospy.Rate(100)

    while not rospy.is_shutdown():
        #print("Check callback function--update")
        
        # Duration time (0.1s) to execute velocity command
        r.sleep()

        # Prevent yawing when there is no new centroid 
        #controller.vel_cmd_pub.publish(cmd_hover)

if __name__ == '__main__':
    main()
    
    

