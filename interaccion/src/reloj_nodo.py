#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool
import time

PREFIX = "[CLOCK] "
LOCAL_TIME = "01:00"
LAP = 60

class Clock():
    """Nodo Reloj"""
    def __init__(self):
        rospy.init_node("reloj_nodo")
        rospy.loginfo(PREFIX + "Nodo iniciado")

        self.start_flag = False

        # Se crea un contador que llama a la funcion still_alive cada LAP segundos
        timer_alive = rospy.Timer(rospy.Duration(LAP), self.still_alive)

        self.pub = rospy.Publisher("still_alive", Bool, queue_size=10)  # topic pub

        # Recibir topic start_topic de dialogo_nodo para activar el timer
        rospy.Subscriber("/start_topic", String, self.start_callback)
        # Recibir topic reset_topic de dialogo_nodo para resetear el timer
        rospy.Subscriber("/reset_topic", String, self.reset_callback)

        rate = rospy.Rate(3) # 3Hz

        while not rospy.is_shutdown():
            if self.start_flag:
                self.hora()
            rate.sleep()

    def still_alive(self, event):
        """Envia un heartbeat a traves del topic still_alive"""
        self.pub.publish(True)

    def hora(self):
        """Muestra por pantalla cada 1/3 de segundo la hora local y en UTC
        junto a los segundos transcurridos desde el ultimo topic recibido de
        dialogo_nodo"""
        current = rospy.Time.now()  # hora actual
        seconds = current.secs - self.last.secs

        # Se da formato a los segundos transcurridos desde Epoch
        ttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current.secs))
        rospy.loginfo(PREFIX + ttime + " Z \n" + ttime + "+" + LOCAL_TIME + " (local)")
        rospy.loginfo(PREFIX + 'It has been ' + str(seconds) + ' seconds since the last message was received')

    def start_callback(self, msg):
        """Callback que recibe los mensajes del start_topic"""
        self.start_msg = msg
        rospy.loginfo(PREFIX + str(msg))
        self.start_flag = True  # Flag activado
        self.last = rospy.Time.now()

    def reset_callback(self, msg):
        """Callback que recibe los mensajes del reset_topic"""
        self.reset_msg = msg
        rospy.loginfo(PREFIX + str(msg))
        self.last = rospy.Time.now()


if __name__ == '__main__':
    try:
        Clock()
    except rospy.ROSInterruptException:
        pass
