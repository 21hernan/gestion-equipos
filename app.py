import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://gestion-equipos-alpha.vercel.app"])

# Datos simulados (equivalentes a tu tabla 'equipos')
EQUIPOS = [
    {"id_eq": "1", "codigo_qr_eq": "QR001", "nombre_eq": "Teclado Mause", "ubicacion_actual_eq": "Almacén Central", "estado_eq": "A"},
    {"id_eq": "2", "codigo_qr_eq": "QR002", "nombre_eq": "Monitor HP", "ubicacion_actual_eq": "Almacén Central", "estado_eq": "A"},
    {"id_eq": "3", "codigo_qr_eq": "QR003", "nombre_eq": "CPU Dell", "ubicacion_actual_eq": "Almacén Central", "estado_eq": "A"},
    {"id_eq": "4", "codigo_qr_eq": "QR004", "nombre_eq": "Impresora Epson", "ubicacion_actual_eq": "Almacén Central", "estado_eq": "A"}
]

@app.route('/')
def home():
    return jsonify({"mensaje": "Backend activo"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data and data.get('clave') == "camioneta42":
        return jsonify({"token": "ok"})
    return jsonify({"error": "Clave incorrecta"}), 401

@app.route('/equipos-todos')
def equipos_todos():
    return jsonify(EQUIPOS)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)