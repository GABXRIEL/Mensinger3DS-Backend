from flask import Flask, request, jsonify

app = Flask(__name__)

# Límite de memoria: guardaremos máximo 50 mensajes en el servidor
MAX_MENSAJES = 50
mensajes_db = []

@app.route('/')
def home():
    return "Servidor Mensinger3DS funcionando", 200

# Endpoint para enviar mensajes (POST)
@app.route('/api/enviar', methods=['POST'])
def enviar():
    try:
        data = request.get_json(force=True)
        de = data.get('de')
        para = data.get('para')
        texto = data.get('mensaje')

        if de and para and texto:
            nuevo_msg = {"de": de, "para": para, "mensaje": texto}
            mensajes_db.append(nuevo_msg)
            
            # 🧹 LIMPIEZA AUTOMÁTICA: Si hay más de 50, se elimina el más viejo (el primero)
            if len(mensajes_db) > MAX_MENSAJES:
                mensajes_db.pop(0)

            print(f"[NUEVO MENSAJE] De: {de} -> Para: {para}: {texto}")
            return jsonify({"status": "ok", "mensaje": "Enviado con exito"}), 200
        
        return jsonify({"status": "error", "mensaje": "Faltan campos"}), 400
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500

# Endpoint para que las 3DS consulten sus mensajes (GET)
@app.route('/api/recibir/<usuario>', methods=['GET'])
def recibir(usuario):
    try:
        # Filtra solo los mensajes que tienen como destinatario a este usuario
        mis_mensajes = [m for m in mensajes_db if m['para'] == usuario]
        return jsonify({"status": "ok", "mensajes": mis_mensajes}), 200
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)