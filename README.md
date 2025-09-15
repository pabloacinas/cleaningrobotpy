# CleaningRobotPY: Sistema de Control para un Robot de Limpieza Autónomo

`CleaningRobotPY` es el software de control para un robot de limpieza autónomo, diseñado para navegar y limpiar una habitación de forma eficiente. El sistema gestiona el movimiento, la detección de obstáculos y el estado de la batería del robot, permitiéndole operar de manera inteligente.



## Descripción del Proyecto

Este proyecto simula el cerebro de un robot de limpieza encargado de mantener los suelos libres de polvo. El robot opera en un entorno representado como una cuadrícula de coordenadas `(x, y)`, donde `(0,0)` es la esquina inferior izquierda.

El control del robot se realiza a través de un **Sistema de Gestión de Rutas (RMS)**, que envía comandos simples para dirigir sus movimientos y acciones.

---

## Características Principales

### **Sistema de Movimiento y Navegación**
El robot está equipado con dos motores de corriente continua (DC) que le confieren una gran movilidad:
* Un **motor para las ruedas** que le permite avanzar.
* Un **motor de rotación** para girar su cuerpo a la izquierda o a la derecha, cambiando su orientación (Norte, Sur, Este, Oeste).

### **Detección de Obstáculos**
Para evitar colisiones, el robot utiliza un **sensor de distancia por infrarrojos** situado en su parte frontal. Si detecta un obstáculo, se detiene y reporta su posición, esperando un nuevo comando del RMS.

### **Sistema de Limpieza**
Debajo del chasis se encuentra un sistema de limpieza compuesto por **dos cepillos giratorios**. Este sistema se activa automáticamente cuando el robot se enciende y tiene suficiente batería, garantizando que el suelo quede limpio a su paso.

### **Gestión Inteligente de Batería**
El robot monitoriza constantemente su nivel de energía gracias a un **Sensor de Batería Inteligente (IBS)**.
* Si la carga de la batería **desciende por debajo del 10%**, el sistema de limpieza se apaga para ahorrar energía y se enciende un **LED de recarga** en la parte superior del robot para indicar que necesita volver a su base.
* Mientras la batería esté por encima de este umbral, el sistema de limpieza permanecerá activo y el LED de recarga apagado.

---

## Arquitectura del Software

El código está estructurado en la clase `CleaningRobot`, que encapsula toda la lógica de control. La comunicación con los componentes de hardware (motores, sensores, LED) se simula a través de **pines GPIO** en modo `BOARD`.

El proyecto fue desarrollado siguiendo una metodología de **Desarrollo Guiado por Pruebas (TDD)**, asegurando que cada funcionalidad sea robusta y fiable. Para ello, se utilizan librerías de `mocking` que permiten simular el comportamiento del hardware en un entorno de desarrollo sin necesidad de tener el robot físico conectado.
