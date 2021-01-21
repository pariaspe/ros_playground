#!/usr/bin/env python

import rospy
from interaccion.msg import inf_personal_usuario

RATE = 10

def shutdown():
    """Funcion salida"""
    print(" ")
    rospy.loginfo("Bye!")


def talker():
    """Nodo Informacion Personal"""
    rospy.init_node('informacion_usuario_node')  # se inicia el nodo
    rospy.on_shutdown(shutdown)  # funcion a ejecutar al salir

    pub = rospy.Publisher('inf_pers_topic', inf_personal_usuario, queue_size=10)  # topic pub

    rate = rospy.Rate(RATE) # 10hz

    while not rospy.is_shutdown():
        try:
            name = str(raw_input("Name: "))  # lectura por entrada
            age = int(raw_input("Age: "))
            langs = raw_input("Languages: ")
        except EOFError:
            # shutdown
            break
        msg = inf_personal_usuario(nombre=name, edad=age, idiomas=langs.split(" "))  # se crea el msg
        # rospy.loginfo(msg)  # debbuging
        pub.publish(msg)  # se envia msg
        rospy.loginfo("Sending new package.")
        rate.sleep()  # se duerme (10Hz)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
