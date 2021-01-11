#!/usr/bin/env python

from __future__ import print_function

from interaccion.srv import multiplicador
import rospy

def multiplicar_edad(req):
    resultado = req.MULT * req.edad
    #Sustituir por ROS_INFO?
    rospy.loginfo("La edad %s multiplicada por %s es %s"%(req.edad, req.MULT, resultado))
    return resultado

def matematico_nodo():
    rospy.init_node('matematico_nodo')

    s = rospy.Service('multiplicador', multiplicador, multiplicar_edad)
    rospy.loginfo("Listo para multiplicar la edad")

    #A la espera de que se solicite el servicio
    rospy.spin()

if __name__ == "__main__":
    matematico_nodo()
