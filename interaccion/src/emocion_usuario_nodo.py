#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def emocion_usuario_nodo():
    
    prompt = "Enter a string: "

    pub = rospy.Publisher('emocion_topic', String, queue_size=10)
    rospy.init_node('emocion_usuario_nodo', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        #Take user input and transform ir to string
        user_str = raw_input(prompt)
        user_str = str(user_str)
        #print(user_str)

        rospy.loginfo(user_str)
        pub.publish(user_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        emocion_usuario_nodo()
    except rospy.ROSInterruptException:
        pass