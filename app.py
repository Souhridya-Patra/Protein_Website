# app.py
from flask import Flask, request, jsonify
import requests
import numpy as np
from colorama import Fore, Style

app = Flask(__name__)

# Keep your existing parameters dictionary
parameters = {
    'Alpha Helix': {'A': 1.42, 'R': 0.98, 'N': 0.67, 'D': 0.73, 'C': 0.70, 'E': 1.51, 'Q': 1.11, 'G': 0.57, 'H': 1.00, 'I': 1.08, 'L': 1.21, 'K': 1.16, 'M': 1.45, 'F': 1.13, 'P': 0.57, 'S': 0.76, 'T': 0.82, 'W': 1.08, 'Y': 0.69, 'V': 1.06},
    'Beta Sheet': {'A': 0.83, 'R': 0.93, 'N': 0.89, 'D': 1.01, 'C': 1.19, 'E': 0.74, 'Q': 0.80, 'G': 0.81, 'H': 0.81, 'I': 1.60, 'L': 1.22, 'K': 0.81, 'M': 1.05, 'F': 1.28, 'P': 0.62, 'S': 1.13, 'T': 1.20, 'W': 1.14, 'Y': 1.47, 'V': 1.65},
    'Coil': {'A': 0.75, 'R': 1.09, 'N': 1.44, 'D': 1.26, 'C': 0.11, 'E': 0.75, 'Q': 1.09, 'G': 1.62, 'H': 1.19, 'I': 0.32, 'L': 0.57, 'K': 1.03, 'M': 0.50, 'F': 0.59, 'P': 1.81, 'S': 0.11, 'T': 0.98, 'W': 0.78, 'Y': 0.84, 'V': 0.29},
    'Turn': {'A': 0.66, 'R': 0.95, 'N': 1.56, 'D': 1.46, 'C': 1.19, 'E': 0.74, 'Q': 0.98, 'G': 1.56, 'H': 0.95, 'I': 0.47, 'L': 0.59, 'K': 1.01, 'M': 0.60, 'F': 0.60, 'P': 1.52, 'S': 1.43, 'T': 0.96, 'W': 0.96, 'Y': 1.14, 'V': 0.50}
}

def calculate_structure(sequence):
    try:
        prediction = []
        for aa in sequence:
            if aa not in parameters['Alpha Helix']:
                raise ValueError(f"Invalid amino acid {aa} in sequence")
                
            probabilities = {
                'H': parameters['Alpha Helix'][aa],
                'E': parameters['Beta Sheet'][aa],
                'C': parameters['Coil'][aa],
                'T': parameters['Turn'][aa]
            }
            
            prediction.append(max(probabilities.items(), key=lambda x: x[1])[0])
            
        return ''.join(prediction)
    except Exception as e:
        return None

def calculate_stats(prediction):
    if not prediction:
        return None
        
    total = len(prediction)
    counts = {
        'H': prediction.count('H'),
        'E': prediction.count('E'),
        'C': prediction.count('C'),
        'T': prediction.count('T')
    }
    
    return {k: (v/total)*100 for k, v in counts.items()}

@app.route('/api/predict', methods=['POST'])
def predict_structure():
    data = request.get_json()
    sequence = data.get('sequence', '').upper()
    
    if not sequence:
        return jsonify({'error': 'No sequence provided'}), 400
        
    prediction = calculate_structure(sequence)
    if not prediction:
        return jsonify({'error': 'Invalid sequence'}), 400
        
    stats = calculate_stats(prediction)
    
    return jsonify({
        'sequence_length': len(sequence),
        'prediction': prediction,
        'statistics': stats
    })

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
