#!/usr/bin/env python
# license removed for brevity
import rospy
from interaccion.msg import pos_usuario

RATE = 10

def shutdown():
    print(" ")
    rospy.loginfo("Bye!")

def posicion_usuario():

    pub = rospy.Publisher('pos_usuario_topic', pos_usuario, queue_size=10) # topic
    rospy.init_node('posicion_usuario_nodo', anonymous=True) # nodo
    rospy.on_shutdown(shutdown)
    rate = rospy.Rate(RATE) # Frecuencia a 10hz

    while not rospy.is_shutdown():
    	try:
    		x_pos = int(raw_input("Posicion en x: "))
    		y_pos = int(raw_input("Posicion en y: "))
    		z_pos = int(raw_input("Posicion en z: "))
    	except EOFError:
    	# shutdown
    		break
    	msg = pos_usuario(x = x_pos, y = y_pos, z = z_pos)
    	rospy.loginfo(msg)
    	pub.publish(msg)
    	rate.sleep()

if __name__ == '__main__':
    try:
        posicion_usuario()
    except rospy.ROSInterruptException:
        pass