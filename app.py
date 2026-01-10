import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensaje": "Backend activo"})

@app.route('/equipos-todos')
def equipos():
    return jsonify([
        {"codigo_qr_eq": "QR001", "nombre_eq": "Teclado Mause", "ubicacion_actual_eq": "Almacén Central"}
    ])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)