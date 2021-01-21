# TRABAJO FINAL - SIST OPERATIVOS DE ROBOTS

- Autor: Pedro Arias Pérez (NIA: 100421902)
- Grupo: Francisco Blanco, Iván Rodríguez y Pedro Arias.
- Github: [ros_playground](https://github.com/pariaspe/ros_playground)

Esta memoria contiene el diseño y el desarrollo del paquete ROS creado, **interaccion**. Todo el código está recogido el repositorio [ros_playground](https://github.com/pariaspe/ros_playground).


## Índice
- [1. Diseño](#diseño)
- [2. Desarrollo](#desarrollo)
- [3. Ejecución](#ejecución)

---

## DISEÑO

Esta sección recoge el diseño y estructura del paquete ROS desarrollado. Además, se explican las decisiones de diseño tomadas y se muestra el grafo de nodos y paso de mensajes.

Una de las principales decisiones de diseño ha sido utilizar Python como código de desarrollo. La principal ventaja de seleccionar Python frente a C++, es la no necesidad de compilar el paquete cada vez que se modifique el código fuente, lo cuál agiliza en gran medida el desarrollo.

Otra decisión tomada ha sido integrar el paquete ROS dentro de un repositorio Github. Utilizar un repositorio nos permite llevar un control de versiones actualizado y facilita el desarrollo de código en equipo.

Antes de mostrar la estructura de nodos ROS, se muestra la estructura de carpetas del paquete y el repositorio que lo contiene.

El repositorio tiene la siguiente estructura:

```txt
.
+-- interaccion (paquete ros)
+-- docs (bagfiles, imgs..)
+-- README.md
+-- memoria-pedro.md
```

Se destaca la estructura del repositorio ya que no se trata en sí de un paquete ROS, por lo que su ruta no se encuentra dentro del `catkin_ws`. En mi caso, se encuentra en la ruta `~/repos/ros_playground`.

El *binding* se consigue gracias a un enlace simbólico. Las instrucciones a seguir serían:

```bash
roscd && cd src
ln -s ~/repos/ros_playground/interaccion .
```

De esta forma, aunque el código fuente se encuentre fuera del `catkin workspace`, se puede compilar y trabajar con el paquete ROS.

La estructura del paquete es la siguiente:

```txt
.
+-- launch
    +-- interaccion-base.launch
    +-- interaccion.launch
    +-- remoto_interaccion.launch
+-- msg
    +-- inf_personal_usuario.msg
    +-- pos_usuario.msg
    +-- usuario.msg
+-- src
    +-- dialogo_nodo.py
    +-- emocion_usuario_nodo.py
    +-- empaquetador_nodo.py
    +-- informaion_personal_nodo.py
    +-- matematico_nodo.py
    +-- posicion_usuario_nodo.py
    +-- reloj_nodo.py
+-- srv
    +-- multiplicador.srv
+-- CMakeLists.txt
+-- package.xml
```

El paquete interacción contiene **7 nodos** escritos en python que hacen uso de **7 topics** (con **3 tipos de mensaje** propios) y **un servicio**. Además, también posee **un launch** que permite desplegar todos los nodos.

Al ejecutar el paquete (`roslaunch interaccion interaccion.launch`) se pueden comprobar los nodos, topics y servicios lanzados.

Con el comando `rosnode list` comprobamos los siete nodos, más un octavo "rosout" parte del roscore y usado para publicar mensajes:

```bash
parias@parias-msi:~$ rosnode list
/dialogo
/emocion_usuario_nodo
/empaquetador
/informacion_usuario_node
/matematico
/posicion_usuario_nodo
/reloj
/rosout
```

Para comprobar los topic se utiliza el comando `rostopic list`. La salida muestra los siete topics utilizados junto con "\\rosout" y "\\rosout_agg" usados para publicar mensajes durante la ejecución.

```bash
parias@parias-msi:~$ rostopic list
/emocion_topic
/inf_pers_topic
/pos_usuario_topic
/reset_topic
/rosout
/rosout_agg
/start_topic
/still_alive
/user_topic
```

Finalmente, para comprobar los servicios se utiliza el comando `rosservice list`. Además, si filtramos esta salida eliminando los servicio encargados de los logs (`grep -v logger`) observamos el servicio creado.

```bash
parias@parias-msi:~$ rosservice list
/dialogo/get_loggers
/dialogo/set_logger_level
/emocion_usuario_nodo/get_loggers
/emocion_usuario_nodo/set_logger_level
/empaquetador/get_loggers
/empaquetador/set_logger_level
/informacion_usuario_node/get_loggers
/informacion_usuario_node/set_logger_level
/matematico/get_loggers
/matematico/set_logger_level
/multiplicador
/posicion_usuario_nodo/get_loggers
/posicion_usuario_nodo/set_logger_level
/reloj/get_loggers
/reloj/set_logger_level
/rosout/get_loggers
/rosout/set_logger_level
parias@parias-msi:~$ rosservice list | grep -v logger
/multiplicador
```

La siguiente figura muestra la estructura de los nodos en ejecución, mediante la herramienta Node Graph de rqt.

![map](/docs/rqt-node-graph.png)

En la figura se puede observar como los nodos "informacion_usuario", "posicion_usuario" y "emocion_usuario" crean sendos topics a los que se conecta el nodo "empaquetador". A su vez, este crea el topic "user_topic" sobre el que publica mensajes que recibe el nodo "dialogo" al estar subscrito. El nodo dialogo publica sobre dos topics ("start" y "reset") sobre los que está subscrito un nuevo nodo "reloj". De forma inversa, el nodo "reloj" publica sobre el topic "still_alive" al cual está subscrito el nodo "dialogo".
Por último, el nodo "matematico" ofrece el servicio multiplicador a la infraestructura presente.

## DESARROLLO

Esta sección recoge las partes más relevantes del desarrollo del paquete.

### Mensajes y servicios
Para el correcto funcionamiento del paquete, se han creado tres tipos de mensaje (`inf_personal_usuario.msg`, `pos_usuario.msg` y `usuario.msg`) junto con un tipo de servicio (`multiplicador.srv`). Sobre los mensajes destacar el tipo "usuario", ya que utiliza a su vez otros tipos de mensajes tanto creados por nosotros como de la librería estándar de mensajes.

```txt
interaccion/inf_personal_usuario infPersonal
string emocion
interaccion/pos_usuario posicion
```

Además, destacar también el servicio creado. Los campos son dos de entrada y uno de salida. Las entradas son la edad y una constante de multiplicación, en este caso 2, aunque se podría modificar. Por otro lado, la salida es el resultado de la multiplicación la cual tiene un tamaño de entero superior para evitar un posible overflow, caso bastante improbable porque nadie debería tener una edad tan elevada.

```txt
#Constant
uint32 MULT=2
#Edad - posible cambio por la edad del mensaje
uint32 edad
---
int64 resultado # Evitar overflow de la multiplicacion
```

### CMakeLists
Estos tipos de mensajes y servicios se han declarado correctamente en el `CMakeLists.txt`, como se puede comprobar el el propio fichero. Junto a los mensajes y servicios se han declarado los nodos, los cuales pasamos a describir a continuación. Una vez definidos, compilamos el paquete `catkin build`. Mientras no modifiquemos el "CMakeLists" y no añadamos nuevos nodos, mensajes o servicios, no es necesario volver a compilar el paquete.

### Nodos
A la hora de analizar los nodos creados distinguimos los nodos que son meramente emisores o publicadores (*publishers*), los nodos que ofrecen servicios y los nodos emisores-receptores (*publisher-subscriber*).

Los nodos emisores son `emocion_usuario_node.py`, `informacion_personal_nodo.py` y `posicion_usuario_nodo.py`. Lo más interesante de estos nodos es el bucle de ejecución. A continuación, se muestra un ejemplo estándar de este bucle explicado:

```python
rospy.init_node('my_nodo')  # se inicia el nodo

pub = rospy.Publisher('my_topic', MsgTipo, queue_size=10)  # topic pub

rate = rospy.Rate(RATE) # 10hz

while not rospy.is_shutdown():
    # LECTURA DE ENTRADA POR PANTALLA

    pub.publish(msg)  # se envia msg
    rate.sleep()  # se duerme (10Hz)
```

La secuencia sería: iniciar el nodo, atarme al topic sobre el que voy a publicar, establecer el *rate* y publicar mensajes según voy recibiendo la entrada del usuario. Es importante entender que el *rate* me establece el ratio o velocidad de iteración del bucle.

En este paquete solo hay un paquete que ofrece un servicio (`matematico_nodo.py`). La secuencia seguida es iniciar el nodo, establecer el sercivio con la función handle y hacemos *spin*. EL método spin inicia un bucle infinito hasta que el nodo reciba una señal de apagado (shutdown).

```python
def handle(req):
    # REALIZAMOS TAREA
    return resp

def my_server():
    rospy.init_node('my_nodo')

    s = rospy.Service('my_servicio', ServicioTipo, handle)  # Llamadas al servicio atadas al handle, donde se realizará la tarea requerida

    rospy.spin()  # A la espera de que se solicite el servicio
```

Por último, los nodos `dialogo_nodo.py`, `empaquetador_nodo.py` y `reloj_nodo.py` son emisores-receptores. Además el nodo dialogo utiliza un servicio, mientras que el nodo reloj utiliza un timer o contador.

Se muestra en primer lugar la estructura del código del nodo dialogo. Se inicia el nodo, se espera que el servicio este disponible y si es posible obtiene un proxy al servidor (el cual le permitirá hacer llamadas al servicio `resp = serv(ServicioTipo)`) y declara los publicadores y subscriptores antes de hacer *spin*.

```python
rospy.init_node("my_nodo")  # se inicia nodo

# Service call
rospy.wait_for_service("a_service")  # se espera que el servicio este disponible
try:
    serv = rospy.ServiceProxy("a_service", Servicio)  # cliente
except rospy.ServiceProxy as e:
    # Fallo en llamada a servicio

# Publishers
start_pub = rospy.Publisher('my_topic', MsgTipo, queue_size=10)  # pub a topic

# Subscriber
rospy.Subscriber("/a_topic", MsgTipo, my_callback)  # sub a topic

rospy.spin()
```

Por otro lado, el nodo reloj iniciaría el nodo, crea el Timer que llamará al método *my_callback* cada *LAP* segundos, establece los publicadores y a continuación los subscriptores y por último itera a 3Hz de forma similar a la ya explicada anteriormente.

```python
rospy.init_node("my_nodo")

timer_alive = rospy.Timer(rospy.Duration(LAP), my_callback)

pub = rospy.Publisher("my_topic", MsgTipo, queue_size=10)  # pub a topic

rospy.Subscriber("/a_topic", MsgTipo, other_callback)  # sub a topic

rate = rospy.Rate(3) # 3Hz

while not rospy.is_shutdown():
    # ENVIO MSGs A RATE 3Hz
    pub.publish(msg)

    rate.sleep()
```

Finalmente, destacar que para ejecutar `espeak` se hace uso del submodulo de python *subprocess*. Con él se abre un proceso que ejecuta el siguiente comando espeak:

```python
subprocess.Popen(["espeak", "-v", "es", sentence])  # se lanza espeak
```

### Launch
Se han creado varios archivos launch con diferentes propósitos. Se muestran a continuación:
- `interaccion-base.launch`: Lanza la parte básica del paquete.
- `interaccion.launch`: Lanza el paquete completo.
- `remoto_interaccion.launch`: Permite el lanzamiento del nodo posición en una raspberry pi remota.

Si analizamos el launch completo podemos comprobar como los nodos que reciben entrada por pantalla son lanzados en una terminal diferentes, mientras que el resto de nodos se lanzan en la misma terminal. Entre ellos, solo dos ("dialogo" y "reloj") muestran su salida por el terminal ya que la información que muestran se considera relevante.

```xml
<?xml version="1.0"?>
<launch>
    <arg name="cmd-bash" default="gnome-terminal --command"/>

    <node name="matematico" pkg="interaccion" type="matematico_nodo.py"/>
    <node name="informacion" pkg="interaccion" type="informacion_personal_nodo.py" launch-prefix="$(arg cmd-bash)"/>
    <node name="posicion" pkg="interaccion" type="posicion_usuario_nodo.py" launch-prefix="$(arg cmd-bash)"/>
    <node name="emocion" pkg="interaccion" type="emocion_usuario_nodo.py" launch-prefix="$(arg cmd-bash)"/>
    <node name="empaquetador" pkg="interaccion" type="empaquetador_nodo.py"/>
    <node name="dialogo" pkg="interaccion" type="dialogo_nodo.py" output="screen"/>
    <node name="reloj" pkg="interaccion" type="reloj_nodo.py" output="screen"/>
</launch>
```

Para lanzar un nodo remoto en una Raspberry Pi es necesario declarar la etiqueta "machine" en el nodo que quieras ejecutar.

```xml
<machine name="pi-zero" address="192.168.1.53" env-loader="/opt/ros/kinetic/env.sh" password="password" user="pi"/>

<node machine="pi-zero" name="posicion" pkg="interaccion" type="posicion_usuario_nodo.py" output="screen"/>
```

## Ejecución

En la primera sección ya se mostraron los nodos, topics y servicios en ejecución junto con el grafo con la estructura de los nodos. Así pues, en esta sección se muestra un vídeo con la ejecución en el que se explican los aspectos relevantes del diseño y se muestra el funcionamiento del paquete. Durante la ejecucicón se graba un bagfile, el cual también se adjunta en el directorio `/docs`.

[![Video Base](http://img.youtube.com/vi/xYU5fRBoH78/0.jpg)](http://www.youtube.com/watch?v=xYU5fRBoH78)

Tal como se muestra en el vídeo, el consumo de RAM y CPU en ejecución no es elevado.

![Process Monitor](/docs/rqt-process-monitor.png)

Por ultimo, se adjunta otro vídeo donde se realiza una ejecución del paquete en remoto. El vídeo tiene dos partes, en la primera se muestra la ejecución entre dos PCs mientras que en la segunda se muestra la ejecución entre un PC y una RAspberry Pi.

[![Video Remoto](http://img.youtube.com/vi/8Ytfg5aUvMw/0.jpg)](http://www.youtube.com/watch?v=8Ytfg5aUvMw)

Para poder ejecutar en diferentes máquinas, ha sido necesario utilizar dos variables de entorno de ROS. En el equipo donde se ejecuta el roscore se han añadido `ROS_MASTER_URI` apuntando a la dirección IP de localhost y con el puerto por defecto (11311), junto con `ROS_IP` con la dirección IP de la propia máquina en la subred local.
Por otro lado, la máquina en remoto introduce en `ROS_MASTER_URI` la dirección IP de la máquina con el roscore y el mismo puerto (11311), junto con junto con `ROS_IP` con la dirección IP de la propia máquina en la subred local.

```bash
# Maquina con el roscore
export ROS_MASTER_URI=http://localhost:11311
export ROS_IP=my_ip  # ip correspondiente su propia dirección en la red local

------------------------------------

# Maquina remota
export ROS_MASTER_URI=http://my_ip:11311  # ip de la maquina con roscore
export ROS_IP=other_ip  # ip correspondiente su propia dirección en la red local
```
