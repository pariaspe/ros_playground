#!/usr/bin/env python

from __future__ import print_function

from interaccion.srv import multiplicador
import rospy

PREFIX = "[MATEMATICO] "  # por propositos de legibilidad


def multiplicar_edad(req):
    """Multiplica edad por MULT"""
    resultado = req.MULT * req.edad
    rospy.loginfo("The age %s multiplied by %s is %s"%(req.edad, req.MULT, resultado))
    return resultado

def matematico_nodo():
    """Nodo matematico"""
    rospy.init_node('matematico_nodo')
    rospy.loginfo(PREFIX + "Node started")

    s = rospy.Service('multiplicador', multiplicador, multiplicar_edad)  # respuesta al cliente
    rospy.loginfo(PREFIX + "Server ready to operate")

    #A la espera de que se solicite el servicio
    rospy.spin()

if __name__ == "__main__":
    matematico_nodo()
