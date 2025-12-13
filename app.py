kimport os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Obtener variables de entorno
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
clave_secreta = os.getenv("CLAVE_SECRETA", "camioneta42")

# Validar que las variables críticas existan
if not supabase_url or not supabase_key:
    print("⚠️ ADVERTENCIA: SUPABASE_URL o SUPABASE_KEY no están configuradas")
    print("SUPABASE_URL =", repr(supabase_url))
    print("SUPABASE_KEY =", repr(supabase_key))
    # Usa valores ficticios para evitar que la app se caiga
    supabase_url = "https://dummy.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy"

# Conexión a Supabase
try:
    supabase = create_client(supabase_url, supabase_key)
except Exception as e:
    print("❌ Error al conectar con Supabase:", e)
    supabase = None

@app.route('/')
def home():
    return jsonify({"mensaje": "Backend de gestión de equipos activo"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data and data.get('clave') == clave_secreta:
        return jsonify({"token": "dispositivo_autorizado"})
    return jsonify({"error": "Clave incorrecta"}), 401

@app.route('/equipos/<codigo_qr>')
def get_equipo(codigo_qr):
    if not supabase:
        return jsonify({"error": "Backend no configurado"}), 500
    try:
        response = supabase.table('equipos').select('*').eq('codigo_qr_eq', codigo_qr).execute()
        if response.data and len(response.data) > 0:
            return jsonify(response.data[0])
        return jsonify({}), 404
    except Exception as e:
        print("Error al obtener equipo:", e)
        return jsonify({"error": "Error interno"}), 500

@app.route('/movimientos/lote', methods=['POST'])
def mover_lote():
    if not supabase:
        return jsonify({"error": "Backend no configurado"}), 500

    data = request.json
    if not data:
        return jsonify({"error": "Cuerpo de la solicitud vacío"}), 400

    codigos_qr = data.get('equipos', [])
    destino = data.get('destino', '')
    
    if not codigos_qr or not destino:
        return jsonify({"error": "Faltan equipos o destino"}), 400

    for qr in codigos_qr:
        try:
            equipo_resp = supabase.table('equipos').select('*').eq('codigo_qr_eq', qr).execute()
            if not equipo_resp.data or len(equipo_resp.data) == 0:
                continue  # Ignora equipos no encontrados

            equipo = equipo_resp.data[0]
            equipo_id = equipo['id_eq']
            ubicacion_actual = equipo['ubicacion_actual_eq']

            # Marcar movimientos anteriores como 'B'
            supabase.table('movimientos').update({'estado_mv': 'B'}).eq('equipo_id_mv', equipo_id).execute()

            # Insertar nuevo movimiento con estado 'A'
            nuevo_mov = {
                'equipo_id_mv': equipo_id,
                'ubicacion_origen_mv': ubicacion_actual,
                'ubicacion_destino_mv': destino,
                'fecha_mv': datetime.now().strftime('%Y-%m-%d'),
                'usuario_mv': 'operario',
                'estado_mv': 'A'
            }
            supabase.table('movimientos').insert(nuevo_mov).execute()

            # Actualizar ubicación del equipo
            supabase.table('equipos').update({'ubicacion_actual_eq': destino}).eq('id_eq', equipo_id).execute()

        except Exception as e:
            print(f"Error al mover equipo {qr}:", e)
            continue

    return jsonify({"mensaje": f"{len(codigos_qr)} equipos movidos a {destino}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
