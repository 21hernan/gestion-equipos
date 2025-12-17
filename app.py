import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://gestion-equipos-alpha.vercel.app"])

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
clave_secreta = os.getenv("CLAVE_SECRETA", "camioneta42")

if not supabase_url or not supabase_key:
    print("⚠️ Faltan variables de Supabase")
    supabase_url = "https://dummy.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy"

try:
    supabase = create_client(supabase_url, supabase_key)
except:
    supabase = None

@app.route('/')
def home():
    return jsonify({"mensaje": "Backend activo"})

@app.route('/equipos-todos')
def get_equipos_todos():
    if not supabase:
        return jsonify([])  # Devuelve lista vacía si no hay conexión
    try:
        response = supabase.table('equipos').select('*').eq('estado_eq', 'A').execute()
        return jsonify(response.data or [])
    except:
        return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)