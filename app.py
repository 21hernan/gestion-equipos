import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Conexión a Supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
CLAVE_SECRETA = os.getenv("CLAVE_SECRETA")

@app.route('/')
def home():
    return jsonify({"mensaje": "Backend de gestión de equipos activo"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data.get('clave') == CLAVE_SECRETA:
        return jsonify({"token": "dispositivo_autorizado"})
    return jsonify({"error": "Clave incorrecta"}), 401

@app.route('/equipos/<codigo_qr>')
def get_equipo(codigo_qr):
    response = supabase.table('equipos').select('*').eq('codigo_qr_eq', codigo_qr).execute()
    if response.data and len(response.data) > 0:
        return jsonify(response.data[0])
    return jsonify({}), 404

@app.route('/movimientos/lote', methods=['POST'])
def mover_lote():
    data = request.json
    codigos_qr = data.get('equipos', [])
    destino = data.get('destino', '')
    
    if not codigos_qr or not destino:
        return jsonify({"error": "Faltan equipos o destino"}), 400

    for qr in codigos_qr:
        equipo_resp = supabase.table('equipos').select('*').eq('codigo_qr_eq', qr).execute()
        if not equipo_resp.data or len(equipo_resp.data) == 0:
            continue  # Equipo no encontrado, lo ignora

        equipo = equipo_resp.data[0]
        equipo_id = equipo['id_eq']
        ubicacion_actual = equipo['ubicacion_actual_eq']

        # Marcar todos los movimientos anteriores como 'B' (histórico)
        supabase.table('movimientos').update({'estado_mv': 'B'}).eq('equipo_id_mv', equipo_id).execute()

        # Insertar nuevo movimiento con estado 'A' (activo)
        nuevo_mov = {
            'equipo_id_mv': equipo_id,
            'ubicacion_origen_mv': ubicacion_actual,
            'ubicacion_destino_mv': destino,
            'fecha_mv': datetime.now().strftime('%Y-%m-%d'),
            'usuario_mv': 'operario',
            'estado_mv': 'A'
        }
        supabase.table('movimientos').insert(nuevo_mov).execute()

        # Actualizar ubicación actual del equipo
        supabase.table('equipos').update({'ubicacion_actual_eq': destino}).eq('id_eq', equipo_id).execute()

    return jsonify({"mensaje": f"{len(codigos_qr)} equipos movidos a {destino}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
