import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Función para verificar si un punto está dentro de un polígono
def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

# Definir los polígonos y sus etiquetas con colores diferentes
areas = [
    {"polygon": np.array([[100, 50], [400, 50], [400, 400], [100, 400]]), "label": "Area 1", "person_count": 0, "status": "Estado: No se ha detectado movimiento", "color": (255, 0, 0)},
    {"polygon": np.array([[700, 750], [1250, 750], [1250, 1070], [700, 1070]]), "label": "Area 2", "person_count": 0, "status": "Estado: No se ha detectado movimiento", "color": (0, 255, 0)},
    {"polygon": np.array([[1500, 300], [1900, 300], [1900, 650], [1500, 650]]), "label": "Area 3", "person_count": 0, "status": "Estado: No se ha detectado movimiento", "color": (0, 0, 255)}
]

# Inicializar el capturador de video
cap = cv2.VideoCapture('gente.mp4')

# Inicializar el extractor de fondo y el kernel
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

# Crear la ventana principal
root = tk.Tk()
root.title("Contador de Personas")

# Definir el tamaño de la ventana
window_width = 1000  # Puedes modificar el ancho de la ventana
window_height = 850  # Puedes modificar la altura de la ventana
root.geometry(f"{window_width}x{window_height}")

# Crear una etiqueta para mostrar el video
video_label = tk.Label(root)
video_label.place(x=10, y=10, width=window_width - 20, height=window_height - 200)  # Modifica el tamaño del video según sea necesario

# Colores de fondo para cada etiqueta
background_colors = ["lightblue", "lightgreen", "#FF9999"]

# Crear etiquetas para mostrar el conteo y el estado de cada área
label_area_info = []
max_label_width = 0
for i, area in enumerate(areas):
    label = tk.Label(root, text=f"{area['label']}: {area['person_count']} | {area['status']}", font=("Times New Roman", 12, "bold"), bg=background_colors[i])
    label.place(x=10, y=window_height - 180 + i * 30, width=window_width - 20, height=30)
    label_area_info.append(label)
    label_width = label.winfo_reqwidth()
    if label_width > max_label_width:
        max_label_width = label_width

# Función para actualizar la interfaz de usuario
def update_ui():
    ret, frame = cap.read()
    if not ret:
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Dibujar polígonos en el frame y reiniciar el estado y contador de personas
    for area in areas:
        cv2.drawContours(frame, [area["polygon"]], -1, area["color"], 2)
        cv2.putText(frame, area["label"], (area["polygon"][0][0], area["polygon"][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, area["color"], 1)

    # Aplicar la operación AND para el área de interés
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    for area in areas:
        imAux = cv2.drawContours(imAux, [area["polygon"]], -1, (255), -1)
    image_area = cv2.bitwise_and(gray, gray, mask=imAux)

    # Aplicar el extractor de fondo
    fgmask = fgbg.apply(image_area)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    # Encontrar contornos de personas y actualizar el estado y el contador de personas por área
    for area in areas:
        area["status"] = "Estado: No se ha detectado movimiento"
        area["person_count"] = 0

    cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    personas_detectadas = []

    for cnt in cnts:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            # Verificar si la persona está dentro de alguno de los polígonos definidos
            for area in areas:
                if point_inside_polygon(x + w//2, y + h//2, area["polygon"]):
                    cv2.rectangle(frame, (x, y), (x+w, y+h), area["color"], 2)
                    personas_detectadas.append((x, y, x+w, y+h))
                    area["status"] = "Estado: Alerta Movimiento Detectado!"
                    area["person_count"] += 1

    # Mostrar el conteo de personas y el estado de cada área en la pantalla
    for i, area in enumerate(areas):
        label_area_info[i].config(text=f"{area['label']}: {area['person_count']} | {area['status']}")

    # Convertir la imagen de OpenCV a un formato compatible con Tkinter
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)

    # Redimensionar el video para que se ajuste al tamaño del contenedor
    img = img.resize((window_width - 20, window_height - 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image=img)

    # Mostrar la imagen en la interfaz de usuario
    video_label.img = img
    video_label.config(image=img)
    video_label.after(7, update_ui)  # Ajustar el tiempo de espera para una actualización más rápida

# Actualizar la interfaz de usuario
update_ui()

# Función para salir de la aplicación
def salir():
    root.destroy()

# Calcular la posición del botón Salir
max_label_height = max(label.winfo_reqheight() for label in label_area_info)
button_width = 100
button_height = 30
button_x = max_label_width + 100
button_y = window_height - 150 + (len(areas) - 1) * 30 - (max_label_height - 30) / 2

# Agregar un botón de "Salir"
button_salir = tk.Button(root, text="Salir", command=salir, font=("Times New Roman", 12, "bold"))
button_salir.place(x=button_x, y=button_y, width=button_width, height=button_height)

root.mainloop()
cap.release()
cv2.destroyAllWindows()
