#!/usr/bin/env python

import rospy
from interaccion.msg import usuario
from std_msgs.msg import String, Bool
from interaccion.srv import multiplicador

import subprocess

PREFIX = "[DIALOGO] "  # por propositos de legibilidad


class Dialogo():
    """Nodo Dialogo"""
    def __init__(self):
        """Inicializacion del nodo"""
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

        rospy.init_node("dialogo_node")  # se inicia nodo
        rospy.loginfo(PREFIX + "Nodo iniciado")
        rospy.spin()

    def usuario_cb(self, msg):
        """Callback que recibe los mensajes del user_topic"""
        self.usuario_msg = msg
        rospy.loginfo(PREFIX + str(msg))

        resp = self.multiplicador(int(self.usuario_msg.infPersonal.edad))  # llamada al servidor multiplicador
        rospy.loginfo(PREFIX + "Resultado de la multiplicacion: " + str(resp.resultado))

        if not self.started:
            self.start_pub.publish("start")  # se publica msg por topic start
            self.started = True  # flag activada
        else:
            self.reset_pub.publish("reset")  # se publica msg por topic reset

        sentence = self.usuario_msg.infPersonal.nombre + " esta " + str(self.usuario_msg.emocion)
        subprocess.Popen(["espeak", "-v", "es", sentence])  # se lanza espeak

    def still_alive_cb(self, msg):
        """Callback que recibe los mensajes del still_alive topic"""
        rospy.loginfo(PREFIX + "Heartbeat received at: " + str(msg.data))


if __name__ == '__main__':
    try:
        Dialogo()
    except rospy.ROSInterruptException:
        pass
