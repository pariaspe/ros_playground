#!/usr/bin/env python

import rospy
from interaccion.msg import inf_personal_usuario, pos_usuario, usuario
from std_msgs.msg import String


class Empaquetador():
    """Nodo Empaquetador"""
    def __init__(self):
        """Inicializacion del nodo"""
        # Mensajes a None
        self.inf_pers = None
        self.emocion = None
        self.posicion = None

        self.usuario_msg = usuario()  # msg vacio

        rospy.Subscriber("/inf_pers_topic", inf_personal_usuario, self.inf_pers_cb)  # sub a nodo inf_personal
        rospy.Subscriber("/emocion_topic", String, self.emocion_usr_cb)  # sub a nodo emocion
        rospy.Subscriber("/pos_usuario_topic", pos_usuario, self.posicion_cb)  # sub a nodo posicion

        self.pub = rospy.Publisher("user_topic", usuario, queue_size=10)  # topic pub

        rospy.init_node("empaquetador_node")  # se inicia el nodo
        rospy.spin()

    def inf_pers_cb(self, msg):
        """Callback que recibe los mensajes del inf_pers_topic"""
        self.inf_pers = msg  # se guarda el msg
        rospy.loginfo("Inf pers received: ({0} {1} {2})".format(msg.nombre, msg.edad, msg.idiomas))
        # Si se han recibido los tres msgs, se envia paquete
        if self.inf_pers is not None and self.emocion is not None and self.posicion is not None:
            self.send_package()

    def emocion_usr_cb(self, msg):
        """Callback que recibe los mensajes del emocion_topic"""
        self.emocion = str(msg.data)  # se guarda el msg
        rospy.loginfo("Emotion received: " + str(msg.data))
        # Si se han recibido los tres msgs, se envia el paquete
        if self.inf_pers is not None and self.emocion is not None and self.posicion is not None:
            self.send_package()

    def posicion_cb(self, msg):
        """Callback que recibe los mensajes del pos_usuario_topic"""
        self.posicion = msg  # se guarda el msg
        rospy.loginfo("Position received: ({0} {1} {2})".format(str(msg.x), str(msg.y), str(msg.z)))
        # Si se han recibido los tres msgs, se envia el paquete
        if self.inf_pers is not None and self.emocion is not None and self.posicion is not None:
            self.send_package()

    def send_package(self):
        """Envia un msg a traves del user_topic"""
        # Se construye el msgs
        self.usuario_msg.infPersonal = self.inf_pers
        self.usuario_msg.emocion = self.emocion
        self.usuario_msg.posicion = self.posicion
        self.pub.publish(self.usuario_msg)  # se envia el mensaje
        # rospy.loginfo(self.usuario_msg)  # debbuging
        rospy.loginfo("Sending new package.")

        # Vuelta a None
        self.inf_pers = None
        self.emocion = None
        self.posicion = None


if __name__ == '__main__':
    try:
        Empaquetador()
    except rospy.ROSInterruptException:
        pass
