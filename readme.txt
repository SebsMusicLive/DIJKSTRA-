========================================================================
SIMULADOR DE ENRUTAMIENTO - ALGORITMO DE DIJKSTRA
Materia: Redes 2
Estudiante: Johan Sebastián López Ortega
Código: 1152196
========================================================================

Profesor, adjunto el simulador visual del algoritmo de Dijkstra. 
Para este proyecto decidí construir el motor gráfico y la interfaz 
desde cero usando únicamente 'tkinter' y 'heapq', que ya vienen nativas 
en Python. No usé dependencias externas como networkx o matplotlib para 
evitar problemas de compatibilidad o necesidad de entornos virtuales al 
revisarlo.

El diseño tiene un enfoque de dashboard moderno e integra un sistema 
de interacción por modos para facilitar la edición de la topología.

------------------------------------------------------------------------
1. REQUISITOS Y EJECUCIÓN
------------------------------------------------------------------------
- Python 3.x instalado.
- Ninguna instalación por PIP requerida.

Para abrir el simulador, navegue hasta esta carpeta desde su terminal 
(CMD o PowerShell) y ejecute:

python algoritmo.py

------------------------------------------------------------------------
2. CÓMO USAR LAS HERRAMIENTAS
------------------------------------------------------------------------
La interfaz cuenta con 4 modos de operación ubicados en el panel derecho 
para evitar que se creen nodos por accidente al hacer clic:

1. [↖ Seleccionar]
   - Permite arrastrar y organizar los routers por la pantalla.
   - Si hace DOBLE CLIC sobre el número de un enlace (el peso), se 
     abrirá una ventana para editar ese valor sin tener que borrarlo.

2. [⨁ Añadir Router]
   - Haga clic en cualquier zona libre del área oscura. 
   - El sistema asignará las letras del abecedario automáticamente en orden.

3. [🔗 Conectar]
   - Haga clic en el Router de origen y luego en el de destino.
   - Aparecerá una ventana centrada pidiendo la métrica (latencia en ms).
   - Presione Enter para confirmar.

4. [✖ Eliminar]
   - En este modo, al hacer clic sobre un router se borra toda su info.
   - Al hacer clic sobre la métrica de un enlace, se corta esa conexión.

------------------------------------------------------------------------
3. ENRUTAMIENTO Y RUTAS ALTERNATIVAS (ECMP)
------------------------------------------------------------------------
Digite la letra de ORIGEN y la de DESTINO en los cuadros de texto y 
presione "Ejecutar Dijkstra". 

Modifiqué el comportamiento del algoritmo clásico para que soporte 
ECMP (Equal-Cost Multi-Path). Si en la red existen dos o más caminos 
diferentes que den exactamente la misma latencia mínima, el programa 
trazará la ruta principal en color verde esmeralda y las rutas 
alternativas en color violeta. 

Los resultados, saltos y comandos se registrarán en la terminal integrada 
en la parte inferior derecha.
========================================================================