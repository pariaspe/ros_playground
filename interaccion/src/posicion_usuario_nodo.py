#!/usr/bin/env python
# license removed for brevity
import rospy
import sys
from interaccion.msg import pos_usuario

RATE = 10

is_remote = False  # Flag para lanzar nodo en remoto sobre RaspberryPi

def shutdown():
    """Funcion salida"""
    print(" ")
    rospy.loginfo("Bye!")

def posicion_usuario():
    """Nodo Posicion Usuario"""
    rospy.init_node('posicion_usuario_nodo')  # se inicia el nodo
    rospy.on_shutdown(shutdown)  # funcion a ejecutar al salir

    pub = rospy.Publisher('pos_usuario_topic', pos_usuario, queue_size=10)  # topic pub

    rate = rospy.Rate(RATE)  # Frecuencia a 10hz

    rospy.loginfo("Remote is: " + str(is_remote))

    if is_remote:
        while not rospy.is_shutdown():
            try:
                x_pos = 1
                y_pos = 1
                z_pos = 1
            except EOFError:
            # shutdown
                break
            msg = pos_usuario(x = x_pos, y = y_pos, z = z_pos)
            # rospy.loginfo(msg)  # debbuging
            pub.publish(msg)
            rospy.loginfo("Sending new package.")
            rate.sleep()

    else:
        while not rospy.is_shutdown():
            try:
                x_pos = int(raw_input("X position: "))
                y_pos = int(raw_input("Y position: "))
                z_pos = int(raw_input("z position: "))
            except EOFError:
            # shutdown
                break
            msg = pos_usuario(x = x_pos, y = y_pos, z = z_pos)
            # rospy.loginfo(msg)  # debbuging
            pub.publish(msg)
            rospy.loginfo("Sending new package.")
            rate.sleep()

if __name__ == '__main__':

    ##if(len(sys.argv) == 2): # Not very sophisticated arg checking, assumes good usage
    if sys.argv[-1] == "remote":
        remote = True
    try:
        posicion_usuario()
    except rospy.ROSInterruptException:
        pass
