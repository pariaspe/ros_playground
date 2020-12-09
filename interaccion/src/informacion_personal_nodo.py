#!/usr/bin/env python

import rospy
from std_msgs.msg import String
#from inf_personal_usuario.msg import inf_personal_usuario

def talker():
    pub = rospy.Publisher('inf_pers_topic', String, queue_size=10)  # topic
    rospy.init_node('informacion_usuario_node', anonymous=True)  # node
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        msg = input("> ")
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
