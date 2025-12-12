from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensaje": "Backend activo - prueba local"})

@app.route('/login', methods=['POST'])
def login():
    return jsonify({"token": "dispositivo_autorizado"})

@app.route('/equipos/<codigo_qr>')
def get_equipo(codigo_qr):
    # Simulamos un equipo (solo para prueba)
    return jsonify({
        "id": "123",
        "codigo_qr": codigo_qr,
        "nombre": "Equipo de prueba",
        "ubicacion_actual": "Almacén Central",
        "estado": "activo"
    })

@app.route('/movimientos/lote', methods=['POST'])
def mover_lote():
    return jsonify({"mensaje": "Movimiento simulado (sin guardar en DB)"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
