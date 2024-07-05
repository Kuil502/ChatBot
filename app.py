from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Carga del catálogo de productos
def cargar_catalogo():
    with open('catalogo.json') as f:
        return json.load(f)

catalogo = cargar_catalogo()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    user_message = data['message']
    response = generar_respuesta(user_message)
    emit('response', {'message': response})

def generar_respuesta(mensaje):
    mensaje = mensaje.lower()
    
    if "recomendar" in mensaje or "sugerir" in mensaje:
        return recomendar_producto()
    elif "comprar" in mensaje:
        return "Puedes realizar tu compra visitando nuestra tienda en línea. ¿Necesitas ayuda con algo más?"
    elif "precio" in mensaje or "costo" in mensaje:
        return obtener_precio_producto(mensaje)
    else:
        return "Lo siento, no entiendo tu solicitud. Por favor, pregúntame sobre recomendaciones de productos o precios."

def recomendar_producto():
    producto = random.choice(catalogo["productos"])
    return f"Te recomiendo el {producto['nombre']} por {producto['precio']} USD. {producto['descripcion']}"

def obtener_precio_producto(mensaje):
    for producto in catalogo["productos"]:
        if producto["nombre"].lower() in mensaje:
            return f"El {producto['nombre']} cuesta {producto['precio']} USD."
    return "Lo siento, no encontré el producto que mencionas."

if __name__ == '__main__':
    socketio.run(app, debug=True)
