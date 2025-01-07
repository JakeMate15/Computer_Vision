from flask import Flask, request, jsonify
import random
from flask_cors import CORS

app = Flask(__name__)

# Habilitar CORS para todas las rutas y orígenes
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/validate', methods=['POST'])
def validate():
    data = request.get_json()
    card1 = data.get('card1')
    card2 = data.get('card2')

    if not card1 or not card2:
        return jsonify({'error': 'Faltan nombres de cartas'}), 400

    # Validación ficticia: Puedes reemplazar esto con tu lógica real
    # result = random.choice([True, False])
    result = False

    print(f"Card1: {card1}, Card2: {card2}, Valid: {result}")

    # Devolver un objeto JSON con la clave 'valid'
    return jsonify({'valid': result})

if __name__ == '__main__':
    app.run(port=5000)
