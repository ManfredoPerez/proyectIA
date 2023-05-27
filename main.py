import numpy as np
import cv2
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# ...
# Función para cargar una imagen desde el sistema de archivos
def load_image():
    file_path = filedialog.askopenfilename(initialdir="/", title="Seleccionar imagen",
                                             filetypes=(("Archivos de imagen", "*.jpg;*.jpeg;*.png"),
                                                        ("Todos los archivos", "*.*")))
    if file_path:
        image_path.set(file_path)
        show_original_image()
        # imagen = Image.open(file_path)
        # imagen.thumbnail((600, 900))  # Redimensiona la imagen para ajustarse al espacio disponible
        # imagen_mostrada = ImageTk.PhotoImage(imagen)
        # label_imagen.config(image=imagen_mostrada)
        # label_imagen.image = imagen_mostrada


    # ruta_imagen = filedialog.askopenfilename(initialdir="/", title="Seleccionar imagen",
    #                                          filetypes=(("Archivos de imagen", "*.jpg;*.jpeg;*.png"),
    #                                                     ("Todos los archivos", "*.*")))
    # if ruta_imagen:
    #     imagen = Image.open(ruta_imagen)
    #     imagen.thumbnail((600, 900))  # Redimensiona la imagen para ajustarse al espacio disponible
    #     imagen_mostrada = ImageTk.PhotoImage(imagen)
    #     label_imagen.config(image=imagen_mostrada)
    #     label_imagen.image = imagen_mostrada

# Función para mostrar la imagen original
def show_original_image():
    image_path_val = image_path.get()
    if image_path_val:
        image = cv2.imread(image_path_val)
        cv2.imshow("Original Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Función para procesar la imagen y realizar la detección de objetos
def process_image():
    image_path_val = image_path.get()
    if image_path_val:
        image = cv2.imread(image_path_val)
        height, width = image.shape[0], image.shape[1]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007, (300, 300), 130)

        net.setInput(blob)
        detected_objects = net.forward()

        for i in range(detected_objects.shape[2]):
            confidence = detected_objects[0][0][i][2]
            if confidence > min_confidence:
                class_index = int(detected_objects[0, 0, i, 1])
                upper_left_x = int(detected_objects[0, 0, i, 3] * width)
                upper_left_y = int(detected_objects[0, 0, i, 4] * height)
                lower_right_x = int(detected_objects[0, 0, i, 5] * width)
                lower_right_y = int(detected_objects[0, 0, i, 6] * height)

                prediction_text = f"{classes[class_index]}: {confidence:.2f}%"

                cv2.rectangle(image, (upper_left_x, upper_left_y), (lower_right_x, lower_right_y), colors[class_index], 3)
                cv2.putText(image, prediction_text, (upper_left_x, upper_left_y - 15 if upper_left_y > 30 else upper_left_y + 15), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)

        cv2.imshow("Detected Objects", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# Función para buscar un objeto específico en la imagen
def search_object():
    image_path_val = image_path.get()
    if image_path_val:
        image = cv2.imread(image_path_val)
        height, width = image.shape[0], image.shape[1]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007, (300, 300), 130)

        net.setInput(blob)
        detected_objects = net.forward()

        search_class = entry_search.get()
        found = False

        for i in range(detected_objects.shape[2]):
            confidence = detected_objects[0][0][i][2]
            if confidence > min_confidence:
                class_index = int(detected_objects[0, 0, i, 1])
                class_name = classes[class_index]
                if class_name == search_class:
                    found = True
                    upper_left_x = int(detected_objects[0, 0, i, 3] * width)
                    upper_left_y = int(detected_objects[0, 0, i, 4] * height)
                    lower_right_x = int(detected_objects[0, 0, i, 5] * width)
                    lower_right_y = int(detected_objects[0, 0, i, 6] * height)

                    prediction_text = f"{class_name}: {confidence:.2f}%"

                    cv2.rectangle(image, (upper_left_x, upper_left_y), (lower_right_x, lower_right_y), colors[class_index], 3)
                    cv2.putText(image, prediction_text, (upper_left_x, upper_left_y - 15 if upper_left_y > 30 else upper_left_y + 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)

        if found:
            cv2.imshow("Detected Objects", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            messagebox.showinfo("Object Not Found", f"The object '{search_class}' was not found in the image.")

# ...
# Crear la ventana de la interfaz gráfica
window = tk.Tk()
window.title("Object Detection")
window.geometry("500x600")
window.configure(bg="#E9E9E9")

# # Crear el marco derecho
# marco_derecho = tk.Frame(window, bg="#FFFFFF", bd=5, relief=tk.RAISED)
# marco_derecho.pack(side=tk.RIGHT, padx=30, pady=30)

# # Sección para mostrar la imagen
# label_imagen = tk.Label(bg="#FFFFFF")
# label_imagen.pack()

# Variables de control
image_path = tk.StringVar()

# Crear el marco izquierdo
marco_izquierdo = tk.Frame(window, bg="#E9E9E9")
marco_izquierdo.pack(side=tk.LEFT, padx=30, pady=30)

# Título
label_titulo = tk.Label(marco_izquierdo, text="Cargar y buscar imágenes", font=("Arial", 24, "bold"), bg="#E9E9E9")
label_titulo.pack(pady=10)

# Etiqueta y campo de entrada para la ruta de la imagen
label_image = tk.Label(marco_izquierdo, text="Ruta de la imagen:", font=("Arial", 14, "bold"), bg="#E9E9E9")
label_image.pack()

entry_image = tk.Entry(marco_izquierdo, textvariable=image_path, font=("Arial", 16), width=30)
entry_image.pack(pady=10)

# Botón para cargar la imagen
button_load = tk.Button(marco_izquierdo, text="Cargar imagen", command=load_image, font=("Arial", 16), bg="#FFCC00",
                         fg="#FFFFFF")
button_load.pack(pady=10)

# Botón para mostrar la imagen original
button_show_original = tk.Button(marco_izquierdo, text="Mostrar imagen original", command=show_original_image, font=("Arial", 16), bg="#FFCC00",
                         fg="#FFFFFF")
button_show_original.pack(pady=10)

# Botón para analizar la imagen
button_process = tk.Button(marco_izquierdo, text="Analizar", command=process_image, font=("Arial", 16), bg="#FFCC00",
                         fg="#FFFFFF")
button_process.pack(pady=20)



# Botón para buscar un objeto en la imagen
button_search = tk.Button(marco_izquierdo, text="Buscar Objetos", command=search_object, font=("Arial", 16), bg="#FFCC00",
                         fg="#FFFFFF")
button_search.pack()

# Etiqueta y campo de entrada para el objeto a buscar
label_search = tk.Label(marco_izquierdo, text="Objeto a buscar:", font=("Arial", 14, "bold"), bg="#E9E9E9")
label_search.pack()

entry_search = tk.Entry(marco_izquierdo, font=("Arial", 16), width=30)
entry_search.pack(pady=20)

# ...
# Inicializar la red neuronal y los colores aleatorios
prototxt_path = 'MobileNetSSD_deploy.prototxt.txt'
model_path = 'MobileNetSSD_deploy.caffemodel'
min_confidence = 0.1

classes = ["background", "avion", "bicicleta",
          "pajaro", "bote",
          "bottella", "autobus",
          "carro", "gato",
          "silla", "vaca",
          "comedor", "perro",
          "caballo", "moto",
          "persona", "planta",
          "oveja", "sofa",
          "tren", "tvmonitor"]

np.random.seed(543210)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

window.mainloop()
