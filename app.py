@app.route('/equipos-todos')
def get_equipos_todos():
    if not supabase:
        return jsonify({"error": "Backend no configurado"}), 500
    try:
        # Ajusta este valor al que uses en tu BD
        response = supabase.table('equipos').select('*').eq('estado_eq', 'A').execute()
        data = response.data if response.data else []
        # Depuración: imprime en los logs de Render
        print("Equipos devueltos:", len(data))
        return jsonify(data)
    except Exception as e:
        print("Error al listar equipos:", e)
        return jsonify({"error": "Error interno"}), 500