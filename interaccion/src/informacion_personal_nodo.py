#!/usr/bin/env python

import rospy
from interaccion.msg import inf_personal_usuario

RATE = 10

def shutdown():
    print(" ")
    rospy.loginfo("Bye!")


def talker():
    pub = rospy.Publisher('inf_pers_topic', inf_personal_usuario, queue_size=10)  # topic
    rospy.init_node('informacion_usuario_node', anonymous=True)  # node
    rospy.on_shutdown(shutdown)
    rate = rospy.Rate(RATE) # 10hz

    while not rospy.is_shutdown():
        try:
            name = str(raw_input("Nombre: "))
            age = int(raw_input("Edad: "))
            langs = raw_input("Idiomas: ")
        except EOFError:
            # shutdown
            break
        msg = inf_personal_usuario(nombre=name, edad=age, idiomas=langs.split(" "))
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
