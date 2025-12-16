@app.route('/movimientos/lote', methods=['POST'])
def mover_lote():
    if not supabase:
        return jsonify({"error": "Backend no configurado"}), 500

    data = request.json
    if not 
        return jsonify({"error": "Cuerpo de la solicitud vacío"}), 400

    codigos_qr = data.get('equipos', [])
    destino = data.get('destino', '')
    
    if not codigos_qr or not destino:
        return jsonify({"error": "Faltan equipos o destino"}), 400

    for qr in codigos_qr:
        try:
            equipo_resp = supabase.table('equipos').select('*').eq('codigo_qr_eq', qr).execute()
            if not equipo_resp.data or len(equipo_resp.data) == 0:
                print(f"Equipo no encontrado: {qr}")
                continue

            equipo = equipo_resp.data[0]
            equipo_id = equipo['id_eq']
            ubicacion_actual = equipo['ubicacion_actual_eq']

            # Marcar movimientos anteriores como 'B'
            supabase.table('movimientos').update({'estado_mv': 'B'}).eq('equipo_id_mv', equipo_id).execute()

            # Insertar nuevo movimiento
            nuevo_mov = {
                'equipo_id_mv': equipo_id,
                'ubicacion_origen_mv': ubicacion_actual,
                'ubicacion_destino_mv': destino,
                'fecha_mv': datetime.now().strftime('%Y-%m-%d'),
                'usuario_mv': 'operario',
                'estado_mv': 'A'
            }
            supabase.table('movimientos').insert(nuevo_mov).execute()

            # ACTUALIZAR UBICACIÓN DEL EQUIPO (¡clave!)
            supabase.table('equipos').update({'ubicacion_actual_eq': destino}).eq('id_eq', equipo_id).execute()
            print(f"✅ Equipo {qr} actualizado a {destino}")

        except Exception as e:
            print(f"❌ Error al mover {qr}: {e}")
            continue

    return jsonify({"mensaje": f"{len(codigos_qr)} equipos movidos a {destino}"})