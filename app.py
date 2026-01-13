import os
from flask import Flask, jsonify
from flask_cors import CORS
from supabase import create_client

app = Flask(__name__)
CORS(app, origins=["https://gestion-equipos-alpha.vercel.app"])

# Credenciales desde Render
url = os.environ.get("https://dejsrxnqpgespknupkid.supabase.co")
key = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRlanNyeG5xcGdlc3BrbnVwa2lkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1MDQ0NjQsImV4cCI6MjA4MTA4MDQ2NH0.miCWSNoVy17oyYm6VjFbIPVCCgqunGxw6ne4f5m5_Uc")

# Crear cliente Supabase
supabase = create_client(url, key) if url and key else None

@app.route('/equipos-todos')
def equipos_todos():
    if not supabase:
        return jsonify({"error": "Faltan credenciales de Supabase"}), 500
    try:
        # Traer TODOS los equipos (sin filtro)
        data = supabase.table('equipos').select('*').execute().data
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)