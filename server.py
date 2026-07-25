from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Base de datos temporal en memoria
mensajes_db = {}

@app.route('/')
def home():
    return jsonify({"status": "Servidor Mensinger 3DS Activo 🚀"})

# 1. ENDPOINT PARA ENVIAR UN MENSAJE
@app.route('/api/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    
    if not data or 'de' not in data or 'para' not in data or 'mensaje' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    remitente = str(data['de'])
    destinatario = str(data['para'])
    texto = data['mensaje']

    nuevo_mensaje = {
        "de": remitente,
        "texto": texto,
        "fecha": datetime.now().strftime("%H:%M")
    }

    if destinatario not in mensajes_db:
        mensajes_db[destinatario] = []

    mensajes_db[destinatario].append(nuevo_mensaje)

    print(f"[NUEVO MENSAJE] De: {remitente} -> Para: {destinatario}: {texto}")
    return jsonify({"status": "ok", "mensaje": "Enviado con éxito"}), 200

# 2. ENDPOINT PARA CONSULTAR MENSAJES NUEVOS (Recibir)
@app.route('/api/recibir', methods=['GET'])
def recibir_mensajes():
    mi_key = request.args.get('my_key')
    
    if not mi_key:
        return jsonify({"error": "Falta parametro my_key"}), 400

    mi_key = str(mi_key)

    if mi_key in mensajes_db and mensajes_db[mi_key]:
        mensajes = mensajes_db[mi_key].copy()
        mensajes_db[mi_key] = []  # Vaciar cola una vez entregados
        return jsonify({"mensajes": mensajes}), 200

    return jsonify({"mensajes": []}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)