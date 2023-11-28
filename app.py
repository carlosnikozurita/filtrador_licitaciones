from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['file']

    # Ruta para guardar el archivo de carga
    upload_path = 'uploads/' + file.filename
    file.save(upload_path)

    # Leer el archivo CSV
    try:
        df = pd.read_csv(upload_path, header=2)

        # Lógica de filtrado
        palabras_clave_adicionales = ['áreas verdes', 'bosque', 'nativo', 'ambiental', 'paisajismo', 'flora', 'fauna', 'vegetación', 'parque', 'jardín', 'conservación', 'ecología', 'sostenibilidad', 'reserva natural', 'biodiversidad', 'arboricultura', 'restauración', 'ecosistema', 'jardinería','árbol', 'naturaleza', 'parque urbano', 'manejo forestal', 'ecosistema', 'medio ambiente', 'conservación del suelo', 'corte']

        filtro_keywords = (
            df['Textbox37'].str.contains('|'.join(palabras_clave_adicionales), case=False) |
            df['Textbox38'].str.contains('|'.join(palabras_clave_adicionales), case=False)
        )    

        filtro_regiones = df['citName'].str.contains('Región de los Lagos|Región de Los Ríos', case=False)

        df_filtrado = df[filtro_keywords & filtro_regiones]

        # Exportar el DataFrame filtrado a un nuevo archivo CSV
        result_path = 'uploads/resultado_filtrado.csv'
        df_filtrado.to_csv(result_path, index=False)

        return jsonify({'download_link': result_path})

    except pd.errors.ParserError as e:
        return jsonify({'error': f'Error al analizar el archivo CSV: {e}'})

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
