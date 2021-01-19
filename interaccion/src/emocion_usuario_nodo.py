#!/usr/bin/env python

import rospy
from std_msgs.msg import String

RATE  = 10

def shutdown():
    """Funcion salida"""
    print(" ")
    rospy.loginfo("Adios!")


def emocion_usuario_nodo():
    """Nodo Emocion Usuario"""
    prompt = "Emocion: "

    pub = rospy.Publisher('emocion_topic', String, queue_size=10)  # topic pub
    rospy.init_node('emocion_usuario_nodo', anonymous=True)  # se inica el nodo
    rospy.on_shutdown(shutdown)  # funcion a ejecutar al salir
    rate = rospy.Rate(RATE) # 10hz

    while not rospy.is_shutdown():
        try:
            user_str = raw_input(prompt)  # lectura por entrada
            user_str = str(user_str)
        except EOFError:
            # shutdown
            break
        rospy.loginfo(user_str)  # se muestra por pantalla el mensaje a enviar
        pub.publish(user_str)  # se envia msg
        rate.sleep()  # se duerme (10Hz)

if __name__ == '__main__':
    try:
        emocion_usuario_nodo()
    except rospy.ROSInterruptException:
        pass
