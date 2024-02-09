 # Programa de Conteo de Personas
## 1. Importación de Bibliotecas
cv2: Biblioteca OpenCV para procesamiento de imágenes y video.
numpy as np: Utilizado para operaciones numéricas y manipulación de matrices.
tkinter as tk: Biblioteca de GUI para crear la interfaz de usuario.
PIL.Image, PIL.ImageTk: Utilizado para manipular imágenes en formato PIL (Python Imaging Library) y convertirlas para su visualización en Tkinter.
## 2. Función point_inside_polygon
Verifica si un punto dado (x, y) está dentro de un polígono dado utilizando el algoritmo del rayo.
Utiliza la intersección de líneas para determinar si el punto está dentro del polígono.
## 3. Definición de Áreas de Interés
Se definen áreas de interés con polígonos, cada uno con su etiqueta, conteo de personas y estado.
Cada área tiene un color asociado para identificar visualmente las detecciones.
## 4. Inicialización del Capturador de Video y Algoritmos de Detección de Movimiento
Utiliza cv2.VideoCapture para capturar el video de entrada.
Utiliza el extractor de fondo MOG (Modelo de mezcla de Gaussiano) para detectar movimiento.
Define un kernel para operaciones morfológicas de dilatación y apertura.
## 5. Creación de la Interfaz de Usuario con Tkinter
Se crea la ventana principal con un tamaño definido.
Se crea una etiqueta para mostrar el video y botones para salir.
## 6. Función update_ui
Se actualiza la interfaz de usuario con cada iteración del video.
Lee cada fotograma del video y realiza las siguientes acciones:
Dibuja los polígonos de las áreas de interés en el fotograma.
Aplica operaciones de procesamiento de imágenes para detectar movimiento.
Actualiza el conteo de personas y estado de cada área.
Muestra el fotograma actualizado en la interfaz de usuario.
## 7. Función para Salir de la Aplicación
Define una función para cerrar la ventana y liberar los recursos al salir de la aplicación.
## 8. Configuración de la Interfaz de Usuario y Ciclo Principal
Calcula la posición de los elementos de la interfaz y los coloca correctamente.
Inicia el bucle principal de la aplicación con root.mainloop().
## 9. Liberación de Recursos
Libera el capturador de video y destruye todas las ventanas de OpenCV al salir de la aplicación.
Este programa detecta personas dentro de áreas definidas en un video en tiempo real y muestra el conteo de personas y el estado de cada área en una interfaz de usuario interactiva.
