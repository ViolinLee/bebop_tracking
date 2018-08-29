#!/usr/bin/env python
import rospy
import roslib
from geometry_msgs.msg import Twist
from bebop_tracker_control.msg import centroid


# v1 -> control yaw & alt:

class bebopPIDController:
    def __init__(self):
        self.yaw_p = 0.0
        self.alt_p = 0.0
        #self.yaw_i = ki
        #self.yaw_d = kd

        self.centroid_x = 0
        self.centroid_y = 0

        self.centroid_sub = rospy.Subscriber("/face_centroid", centroid, self.update)
        self.vel_cmd_pub = rospy.Publisher("/bebop/cmd_vel", Twist, queue_size=1)

    def yaw_controller(self):
        e = 0.0
        
        centroid_x = self.centroid_x
        

        difference_x = (center_x - centroid_x)  # in pixel with maximum==428
      
        if abs(difference_x) > 10: 
            e = difference_x/428.0 # maximum is 1.0     
        
        yaw_cmd = self.yaw_p * e # maximum is 1.0  -> max speed is 1.0 degree/s

        return yaw_cmd

    def alt_controller(self):
        e = 0.0
        
        centroid_y = self.centroid_y
        
        difference_y = (center_y - centroid_y)  # in pixel with maximum==240
      
        if abs(difference_y) > 20: 
            e = difference_y/240.0 # maximum is 1.0    

        alt_cmd = self.alt_p * e # maximum is 0.2  -> max speed is 0.2 m/s
        print(alt_cmd)

        return alt_cmd


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
        alt_cmd = self.alt_controller()
        
        cmd = Twist()
        cmd.angular.y = 0.0
        cmd.angular.x = 0.0
        cmd.angular.z = yaw_cmd
        cmd.linear.z = alt_cmd
        cmd.linear.x = 0.0
        cmd.linear.y = 0.0

        self.vel_cmd_pub.publish(cmd)

def main():
    rospy.init_node('bebop_controller')
    controller = bebopPIDController()
    controller.yaw_p = 1.0
    controller.alt_p = 0.3

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
        # print("Check callback function--update")
        
        # Duration time (0.1s) to execute velocity command
        r.sleep()

        # Prevent yawing when there is no new centroid 
        # controller.vel_cmd_pub.publish(cmd_hover)

if __name__ == '__main__':
    main()
    
    

