#!/usr/bin/env python

import rospy
from interaccion.msg import usuario
from std_msgs.msg import String, Bool
from interaccion.srv import multiplicador

import subprocess

PREFIX = "[DIALOGO] "  #  por propositos de legibilidad


class Dialogo():
    """Nodo Dialogo"""
    def __init__(self):
        """Inicializacion del nodo"""
        rospy.init_node("dialogo_node")  # se inicia nodo
        rospy.loginfo(PREFIX + "Node started")

        self.started = False  # flag para el timer

        # Service call (Multiplicador)
        rospy.wait_for_service("multiplicador")  # se espera que el servicio este disponible
        try:
            self.multiplicador = rospy.ServiceProxy("multiplicador", multiplicador)  # cliente
        except rospy.ServiceProxy as e:
            rospy.logwarn(PREFIX + "Service failed: " + e)  # se captura excepcion en caso de error

        # Publishers
        self.start_pub = rospy.Publisher('start_topic', String, queue_size=10)  # se crea un topic pub
        self.reset_pub = rospy.Publisher('reset_topic', String, queue_size=10)  # se crea un topic pub

        # Subscriber (Timer)
        rospy.Subscriber("user_topic", usuario, self.usuario_cb)  # sub a nodo empaquetador
        rospy.Subscriber("still_alive", Bool, self.still_alive_cb)  # sub a nodo reloj

        rospy.spin()

    def usuario_cb(self, msg):
        """Callback que recibe los mensajes del user_topic"""
        self.usuario_msg = msg
        rospy.loginfo(PREFIX + self.process_usuario_msg(self.usuario_msg))

        resp = self.multiplicador(int(self.usuario_msg.infPersonal.edad))  # llamada al servidor multiplicador
        rospy.loginfo(PREFIX + "Result of multiplication: " + str(resp.resultado))

        if not self.started:
            self.start_pub.publish("start")  # se publica msg por topic start
            self.started = True  # flag activada
        else:
            self.reset_pub.publish("reset")  # se publica msg por topic reset

        sentence = self.usuario_msg.infPersonal.nombre + " esta " + str(self.usuario_msg.emocion)
        subprocess.Popen(["espeak", "-v", "es", sentence])  # se lanza espeak
        # subprocess.Popen(["espeak", "-v", "es", self.process_usuario_msg(self.usuario_msg)])  # se lanza espeak

    def still_alive_cb(self, msg):
        """Callback que recibe los mensajes del still_alive topic"""
        rospy.loginfo(PREFIX + "Heartbeat received with: " + str(msg.data))

    def process_usuario_msg(self, msg):
        """Procesa y da formato al mensaje"""
        info = "User (" + msg.infPersonal.nombre + ", " \
        + str(msg.infPersonal.edad) + ", " + str(msg.infPersonal.idiomas) \
        + ") at [" + str(msg.posicion.x) + ", " + str(msg.posicion.y) + ", " \
        + str(msg.posicion.z) + "] is " + msg.emocion
        return info

if __name__ == '__main__':
    try:
        Dialogo()
    except rospy.ROSInterruptException:
        pass
