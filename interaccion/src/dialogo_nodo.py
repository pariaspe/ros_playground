#!/usr/bin/env python

import rospy
from interaccion.msg import usuario
from std_msgs.msg import String, Bool
from interaccion.srv import multiplicador

import subprocess


class Dialogo():
    def __init__(self):
        self.usuario_msg = usuario()
        self.started = False

        # Subscriber
        rospy.Subscriber("user_topic", usuario, self.usuario_cb)

        # Service call (Multiplicador)
        rospy.wait_for_service("multiplicador")
        try:
            self.multiplicador = rospy.ServiceProxy("multiplicador", multiplicador)
        except rospy.ServiceProxy as e:
            rospy.loginfo("Service failed: ", e)

        # Publishers (Timer)
        self.start_pub = rospy.Publisher('start_topic', String, queue_size=10)
        self.reset_pub = rospy.Publisher('reset_topic', String, queue_size=10)

        # Subscriber (Timer)
        rospy.Subscriber("still_alive", Bool, self.still_alive_cb)

        rospy.init_node("dialogo_node")
        rospy.spin()

    def usuario_cb(self, msg):
        self.usuario_msg = msg
        rospy.loginfo(msg)

        sentence = self.usuario_msg.infPersonal.nombre + " esta " + str(self.usuario_msg.emocion)

        resp = self.multiplicador(int(self.usuario_msg.infPersonal.edad))
        rospy.loginfo("Multiplicador: " + str(resp.resultado))

        if not self.started:
            self.start_pub.publish("start")
            self.started = True
        else:
            self.reset_pub.publish("reset")

        subprocess.Popen(["espeak", "-v", "es", sentence])

    def still_alive_cb(self, msg):
        rospy.loginfo("Heartbeat received at:", msg)


if __name__ == '__main__':
    try:
        Dialogo()
    except rospy.ROSInterruptException:
        pass
