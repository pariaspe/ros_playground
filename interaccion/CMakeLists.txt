cmake_minimum_required(VERSION 2.8.3)
project(interaccion)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

## Mensajes propios
add_message_files(
  FILES
  inf_personal_usuario.msg
  usuario.msg
  pos_usuario.msg
)

## Matematico_nodo servicio
add_service_files(
  FILES
  multiplicador.srv
)

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package()

###########
## Build ##
###########

include_directories(
  ${catkin_INCLUDE_DIRS}
)

#############
## Install ##
#############

## Nodos
install(PROGRAMS
  src/informacion_personal_nodo.py
  src/empaquetador_nodo.py
  src/posicion_usuario_nodo.py
  src/emocion_usuario_nodo.py
  src/dialogo_nodo.py
  src/matematico_nodo.py
  src/reloj_nodo.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
