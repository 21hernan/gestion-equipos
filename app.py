import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client

app = Flask(__name__)
CORS(app, origins=["https://gestion-equipos-alpha.vercel.app"])

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("❌ Error al conectar con Supabase:", e)

@app.route('/equipos-todos')
def equipos_todos():
    if not supabase:
        return jsonify({"error": "No conectado a Supabase"}), 500
    try:
        response = supabase.from_('equipos').select('*').execute()
        return jsonify(response.data or [])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/movimientos/lote', methods=['POST'])
def registrar_movimiento_lote():
    if not supabase:
        return jsonify({"error": "No conectado a Supabase"}), 500
    data = request.get_json()
    if not data or not isinstance(data.get('equipos'), list) or not data.get('destino'):
        return jsonify({"error": "Faltan datos: 'equipos' (lista) y 'destino'"}), 400

    try:
        for item in data['equipos']:
            codigo = item if isinstance(item, str) else item.get('codigo_qr')
            if not codigo:
                continue
            equipo_db = supabase.from_('equipos').select('*').eq('codigo_qr_eq', codigo).execute()
            if not equipo_db.data:
                continue
            # Registrar movimiento
            supabase.from_('movimientos').insert({
                "equipo_id_mv": equipo_db.data[0]['id_eq'],
                "ubicacion_origen_mv": equipo_db.data[0]['ubicacion_actual_eq'],
                "ubicacion_destino_mv": data['destino'],
                "usuario_mv": data.get('usuario', 'operario'),
                "estado_mv": "A"
            }).execute()
            # Actualizar ubicación actual del equipo
            supabase.from_('equipos').update({
                "ubicacion_actual_eq": data['destino']
            }).eq('codigo_qr_eq', codigo).execute()
        return jsonify({"mensaje": "Movimientos registrados y ubicaciones actualizadas"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)