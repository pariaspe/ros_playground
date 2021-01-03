#!/usr/bin/env python

import rospy
from interaccion.msg import usuario
from std_msgs.msg import String, Bool
#serv#from interaccion.srv import multiplicador

import subprocess

## Cuidado al descomentar, hay parte del codigo que sirve para el servicio "multiplicador" y parte del "reloj".
##    Multiplicador: los comentarios empiezan por #serv#
##    Reloj: los comentarios empiezan por #timer#


class Dialogo():
    def __init__(self):
        self.usuario_msg = usuario()
        self.started = False

        # Subscriber
        rospy.Subscriber("user_topic", usuario, self.usuario_cb)

        # Client Service (Multiplicador)
        #serv#self.multiplicador = rospy.ServiceProxy("multiplicador", multiplicador)

        # Publishers (Timer)
        #timer#self.start_pub = rospy.Publisher('start_topic', String, queue_size=10)
        #timer#self.reset_pub = rospy.Publisher('reset_topic', String, queue_size=10)

        # Subscriber (Timer)
        #timer#rospy.Subscriber("still_alive", Bool, self.still_alive_cb)

        rospy.init_node("dialogo_node")
        rospy.spin()

    def usuario_cb(self, msg):
        self.usuario_msg = msg
        rospy.loginfo(msg)

        sentence = self.usuario_msg.infPersonal.nombre + " esta " + str(self.usuario_msg.emocion)

        #serv#resp = self.multiplicador(self.usuario_msg.edad)
        #serv#rospy.loginfo("Multiplicador:", resp)

        #timer#if not self.started:
        #timer#    self.start_pub.publish("start")
        #timer#    self.started = True
        #timer#else:
        #timer#    self.reset_pub.publish("reset")

        subprocess.Popen(["espeak", "-v", "es", sentence])


    def still_alive_cb(self, msg):
        rospy.loginfo("Heartbeat received at:", msg)


if __name__ == '__main__':
    try:
        Dialogo()
    except rospy.ROSInterruptException:
        pass
