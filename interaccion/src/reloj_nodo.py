#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool
import time

LOCAL_TIME = "01:00"

class Clock():
    def __init__(self):
        rospy.init_node("reloj_nodo")

        self.start_flag = False
        # Recibir topic start_topic de dialogo_nodo para activar el timer
        rospy.Subscriber("/start_topic", String, self.start_callback)
        # Recibir topic reset_topic de dialogo_nodo para resetear el timer
        rospy.Subscriber("/reset_topic", String, self.reset_callback)

        timer_alive  = rospy.Timer(rospy.Duration(60), self.still_alive)

        self.pub = rospy.Publisher("still_alive", Bool, queue_size=10)

        rate = rospy.Rate(3) # 3Hz

        while not rospy.is_shutdown():
            if self.start_flag:
                self.hora()
            rate.sleep()
            #rospy.spin()

    # Enviar cada 60 segundos un topic still_alive a dialogo_nodo
    def still_alive(self, event):
        self.pub.publish(True)

    # Mostrar por pantalla cada 1/3 de segundo la hora local y en UTC
    # junto a los segundos transcurridos desde el ultimo topic recibido
    # de dialogo_nodo
    def hora(self):
        current = rospy.Time.now()
        seconds = current.secs - self.last.secs

        ttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current.secs))
        rospy.loginfo(ttime + " Z \n" + ttime + "+" + LOCAL_TIME + " (local)")
        rospy.loginfo('It has been ' + str(seconds) + ' seconds since the last message was received')

    def start_callback(self, msg):
        self.start_msg = msg
        rospy.loginfo(msg)
        self.start_flag = True
        self.last = rospy.Time.now()

    def reset_callback(self, msg):
        self.reset_msg = msg
        rospy.loginfo(msg)
        self.last = rospy.Time.now()


if __name__ == '__main__':
    try:
        Clock()
    except rospy.ROSInterruptException:
        pass
