import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client

app = Flask(__name__)
CORS(app, origins=["https://gestion-equipos-alpha.vercel.app"])

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

@app.route('/equipos-todos')
def equipos_todos():
    if not supabase:
        return jsonify({"error": "Backend no configurado"}), 500
    try:
        data = supabase.from_('equipos').select('*').execute().data
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/movimientos/lote', methods=['POST'])
def registrar_movimiento_lote():
    if not supabase:
        return jsonify({"error": "Backend no configurado"}), 500
    
    data = request.get_json()
    if not data or not isinstance(data.get('equipos'), list) or not data.get('destino'):
        return jsonify({"error": "Faltan datos: 'equipos' (lista) y 'destino'"}), 400

    try:
        for item in data['equipos']:
            # Aceptar tanto "QR001" como {"codigo_qr": "QR001"}
            codigo = item if isinstance(item, str) else item.get('codigo_qr')
            if not codigo:
                continue

            # Buscar equipo
            equipo = supabase.from_('equipos').select('*').eq('codigo_qr_eq', codigo).execute().data
            if not equipo:
                continue

            # Registrar movimiento
            supabase.from_('movimientos').insert({
                "equipo_id_mv": equipo[0]['id_eq'],
                "ubicacion_origen_mv": equipo[0]['ubicacion_actual_eq'],
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