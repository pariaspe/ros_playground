#!/bin/bash

# Launch roscore
(xterm -e roscore &)
# Launch nodo_empaquetador
(xterm -e rosrun interaccion empaquetador_nodo.py &)
# Launch nodos emisores
(xterm -e python src/informacion_personal_nodo.py &)
(xterm -e python src/emocion_usuario_nodo.py &)