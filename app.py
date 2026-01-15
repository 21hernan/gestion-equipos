import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client

app = Flask(__name__)
CORS(app, origins=["https://gestion-equipos-alpha.vercel.app"])

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
CLAVE_SECRETA = os.environ.get("CLAVE_SECRETA", "camioneta42")

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("❌ Error al conectar con Supabase:", e)

@app.route('/')
def home():
    return jsonify({"mensaje": "Backend activo"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data and data.get('clave') == CLAVE_SECRETA:
        return jsonify({"token": "ok"})
    return jsonify({"error": "Clave incorrecta"}), 401

@app.route('/equipos-todos')
def equipos_todos():
    if not supabase:
        return jsonify({"error": "No conectado a Supabase"}), 500
    try:
        response = supabase.from_('equipos').select('*').execute()
        return jsonify(response.data or [])
    except Exception as e:
        print("❌ Error en /equipos-todos:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/escanear', methods=['POST'])
def escanear_qr():
    if not supabase:
        return jsonify({"error": "No conectado a Supabase"}), 500
    data = request.get_json()
    if not data or not data.get('codigo_qr'):
        return jsonify({"error": "Falta código QR"}), 400
    try:
        response = supabase.from_('equipos').select('*').eq('codigo_qr_eq', data['codigo_qr']).execute()
        if not response.data:
            return jsonify({"error": "Equipo no encontrado"}), 404
        return jsonify(response.data[0])
    except Exception as e:
        print("❌ Error en /escanear:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/movimientos/lote', methods=['POST'])
def registrar_movimiento_lote():
    if not supabase:
        return jsonify({"error": "No conectado a Supabase"}), 500
    data = request.get_json()
    if not data or not data.get('equipos') or not data.get('destino'):
        return jsonify({"error": "Datos inválidos"}), 400
    try:
        for equipo in data['equipos']:
            equipo_db = supabase.from_('equipos').select('*').eq('codigo_qr_eq', equipo['codigo_qr']).execute()
            if not equipo_db.data:
                continue
            movimiento = {
                "equipo_id_mv": equipo_db.data[0].get("id_eq"),
                "ubicacion_origen_mv": equipo_db.data[0].get("ubicacion_actual_eq"),
                "ubicacion_destino_mv": data.get("destino"),
                "usuario_mv": data.get("usuario", "operario"),
                "estado_mv": "A"
            }
            supabase.from_('movimientos').insert(movimiento).execute()
        return jsonify({"mensaje": "Movimientos registrados"})
    except Exception as e:
        print("❌ Error en /movimientos/lote:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)