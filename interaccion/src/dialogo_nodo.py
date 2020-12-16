#!/usr/bin/env python

import rospy
from interaccion.msg import usuario
from std_msgs.msg import String
from interaccion.srv import multiplicador


class Dialogo():
    def __init__(self):
        self.usuario_msg = usuario()

        rospy.Subscriber("/user_topic", usuario, self.usuario_cb)

        self.multiplicador = rospy.ServiceProxy("multiplicador", multiplicador)

        rospy.init_node("dialogo_node")
        rospy.spin()

    def usuaro_cb(self, msg):
        self.usuario_msg = msg
        rospy.loginfo(msg)


if __name__ == '__main__':
    try:
        Dialogo()
    except rospy.ROSInterruptException:
        pass
