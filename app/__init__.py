from flask import Flask, request, jsonify
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
import json
import os

app_dir = os.path.dirname(os.path.abspath(__file__))
pickle_model = os.path.join(app_dir, './src/assets/lr_classifier.pkl')

app = Flask(__name__)

with open(pickle_model, 'rb') as file:
    model = pickle.load(file)

def evaluate_model(model, data):
    scaler = StandardScaler()
    #scaling Brain Signals
    scaler.fit(data)
    X = scaler.transform(data)
    return model.predict(X)

def process_results(results):
    data, uniques = np.unique(results, return_counts=True)
    
    dictionary = dict(zip(data, uniques))
    sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1]))
    minor_state = list(sorted_dict.keys())[0]
    mid_state = list(sorted_dict.keys())[1]
    mayor_state = list(sorted_dict.keys())[2]
    
    total = uniques[mid_state] + uniques[minor_state] + uniques[mayor_state]
    
    emotional_states = {
        'C1': ['Emocionado', 'Feliz'],
        'C2': ['Molesto', 'Frustrado'],
        'C3': ['Triste', 'Aburrido'],
        'C4': ['Contento', 'Conforme']
    }
    
    y = {
        'high': 0,
        'low': 0,
        'positive': False,
        'negative': False
    }
    
    # NEUTRO
    if mayor_state == 1:
        if dictionary[mid_state] == 2:
            y['high'] = dictionary[mayor_state]/total
            y['low'] = 0
            y['positive'] = True
            y['negative'] = False
        else:
            y['high'] = 0
            y['low'] = dictionary[mayor_state]/total
            y['positive'] = False
            y['negative'] = True
    # POSITIVO
    elif mayor_state == 2:
        if dictionary[mid_state] == 1:
            y['high'] = dictionary[mayor_state]/total
            y['low'] = 0
            y['positive'] = True
            y['negative'] = False
        else:
            y['high'] = 0
            y['low'] = dictionary[mayor_state]/total
            y['positive'] = True
            y['negative'] = False
    # NEGATIVO
    else:
        if dictionary[mid_state] == 2:
            y['high'] = 0
            y['low'] = dictionary[mayor_state]/total
            y['positive'] = False
            y['negative'] = True
        else:
            y['high'] = dictionary[mayor_state]/total
            y['low'] = 0
            y['positive'] = False
            y['negative'] = True
    
    emotional_state = ''
    
    if y['positive']:
        if y['high'] > 0 and y['high'] <= 0.5:
            emotional_state = emotional_states['C1'][1]
        elif y['high'] > 0.5:
            emotional_state = emotional_states['C1'][0]
        elif y['low'] > 0 and y['low'] <= 0.5:
            emotional_state = emotional_states['C4'][1]
        elif y['low'] > 0.5:
            emotional_state = emotional_states['C4'][0]
    else:
        if y['high'] > 0 and y['high'] <= 0.5:
            emotional_state = emotional_states['C2'][1]
        elif y['high'] > 0.5:
            emotional_state = emotional_states['C2'][0]
        elif y['low'] > 0 and y['low'] <= 0.5:
            emotional_state = emotional_states['C3'][1]
        elif y['low'] > 0.5:
            emotional_state = emotional_states['C3'][0]
            
    print(dictionary, y, emotional_state)
    return emotional_state
 
@app.route('/inputdata', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        data = request.get_json()
        if data: # check if data is valid
            # Convert the list to a JSON string
            json_data = json.dumps(data)
            # Load JSON data into a pandas dataframe
            datapd = pd.read_json(json_data)
            results = evaluate_model(model, datapd)
            emotional_state = process_results(results)
            return jsonify(emotional_state), 200
        else:
            return jsonify({"error": "Invalid JSON data"}), 400
    else:
        return jsonify({"error": "Please make a POST request with JSON data to input data"}), 405

if __name__ == '__main__':
    app.run()