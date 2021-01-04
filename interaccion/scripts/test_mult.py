#!/usr/bin/env python

from __future__ import print_function

import sys
import rospy
from interaccion.srv import *

def multiplicador_edad_cliente(edad):
    rospy.wait_for_service('multiplicador')
    try:
        multiplicar_edad = rospy.ServiceProxy('multiplicador', multiplicador)
        resp1 = multiplicar_edad(edad)
        return resp1.resultado
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s edad"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        edad = int(sys.argv[1])
    else:
        print(usage())
        sys.exit(1)
    print("Se multiplica la edad %s por 2"%(edad))
    print("Edad %s* 2 = %s"%(edad, multiplicador_edad_cliente(edad)))