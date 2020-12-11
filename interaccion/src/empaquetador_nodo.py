#!/usr/bin/env python

import rospy
from interaccion.msg import inf_personal_usuario, usuario
from std_msgs.msg import String

### La idea es guardar el ultimo mensaje de cada tipo en un atributo de la
### clase Empaquetador y en cada callback (metodo que se activa al recibir un
### msg por un Subscriber) comprobar si ya tengo listo un msg de cada y llamar
### a otro metodo que publica por el nodo salida.

### Como vereis aun queda por declarar vuestros Subscribers, los callbacks
### asociados e integrarlo en el envio. Cualquier sugerencia es bien recibida :)

class Empaquetador():
    def __init__(self):
        self.inf_pers = None
        self.emocion = None
        self.posicion = None

        self.usuario_msg = usuario()

        rospy.Subscriber("/inf_pers_topic", inf_personal_usuario, self.inf_pers_cb)
        rospy.Subscriber("/emocion_topic", String, self.emocion_usr_cb)

        self.pub = rospy.Publisher("user_topic", usuario, queue_size=10)

        rospy.init_node("empaquetador_node")
        rospy.spin()

    def inf_pers_cb(self, msg):
        self.inf_pers = msg
        rospy.loginfo("Inf pers received: ({0} {1} {2})".format(msg.nombre, msg.edad, msg.idiomas) )
        # if self.inf_pers is not None and self.emocion is not None and self.posicion is not None:
        #   self.send_package()

    def emocion_usr_cb(self, msg):
        self.emocion_usr = msg
        rospy.loginfo("Emotion received: " + str(msg))

    def send_package(self):
        self.usuario_msg.infPersonal = self.inf_pers
        self.usuario_msg.emocion = self.emocion
        #self.usuario_msg.posicion = self.posicion
        self.pub.publish(self.usuario_msg)
        rospy.loginfo(self.usuario_msg)

        # Back to none
        self.inf_pers = None
        self.emocion = None
        self.posicion = None


if __name__ == '__main__':
    try:
        Empaquetador()
    except rospy.ROSInterruptException:
        pass
