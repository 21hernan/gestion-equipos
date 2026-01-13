import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client

app = Flask(__name__)
# Permitir solo tu frontend de Vercel
CORS(app, origins=["https://gestion-equipos-alpha.vercel.app"])

# Leer variables de entorno desde Render
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
CLAVE_SECRETA = os.environ.get("CLAVE_SECRETA", "camioneta42")

# Conectar a Supabase
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("❌ Error al crear cliente de Supabase:", e)

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
        # Usar from_() → método correcto para tablas en Supabase
        response = supabase.from_('equipos').select('*').eq('estado_eq', 'A').execute()
        return jsonify(response.data or [])
    except Exception as e:
        print("❌ Error en /equipos-todos:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)