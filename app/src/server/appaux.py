# from flask import Flask, request, jsonify
# import pickle
# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# import numpy as np
# import json

# app = Flask(__name__)

# # dataf = pd.read_csv('../assets/emotions.csv')

# # print(dataf.head(10))
# # dataf = dataf.drop("label", axis=1)

# # datax = dataf.head(10)
# # # Convert to JSON string
# # df_json = datax.to_json('file.json', orient='records')

# model = pickle.load(open('../assets/lr_classifier.pkl', 'rb'))

# def evaluate_model(model, data):
#     scaler = StandardScaler()
#     #scaling Brain Signals
#     scaler.fit(data)
#     X = scaler.transform(data)
#     return model.predict(X)

# def process_results(results):
#     data, uniques = np.unique(results, return_counts=True)
    
#     dictionary = dict(zip(data, uniques))
#     sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1]))
#     minor_state = list(sorted_dict.keys())[0]
#     mid_state = list(sorted_dict.keys())[1]
#     mayor_state = list(sorted_dict.keys())[2]
    
#     print(uniques[mayor_state], uniques[mid_state], uniques[minor_state])
    
#     total = sum(uniques)
#     sub_total = uniques[mid_state] + uniques[minor_state]
#     # print(total)
#     # my_pc = (uniques[mayor_state]/total)
#     # md_pc = (uniques[mid_state]/total)
#     # mn_pc = (uniques[minor_state]/total)
    
#     emotional_states = {
#         'C1': ['Emocionado', 'Feliz', 'Complacido'],
#         'C2': ['Nervioso', 'Molesto', 'Enojado'],
#         'C3': ['Somnoliento', 'Aburrido', 'Triste'],
#         'C4': ['Relajado', 'Pacifico', 'Calmado']
#     }
    
#     y = {
#         'high': 0,
#         'low': 0,
#         'positive': False,
#         'negative': False
#     }
    
#     if mayor_state == 0:
#         if dictionary[mid_state] == 1:
#             y['high'] = dictionary[mid_state]/sub_total
#             y['low'] = 0
#             y['positive'] = True
#             y['negative'] = False
#         else:
#             y['high'] = 0
#             y['low'] = dictionary[mid_state]/sub_total
#             y['positive'] = False
#             y['negative'] = True
#     elif mayor_state == 1:
#         if dictionary[mid_state] == 0:
#             y['high'] = dictionary[mid_state]/sub_total
#             y['low'] = 0
#             y['positive'] = True
#             y['negative'] = False
#         else:
#             y['high'] = 0
#             y['low'] = dictionary[mid_state]/sub_total
#             y['positive'] = True
#             y['negative'] = False
#     else:
#         if dictionary[mid_state] == 0:
#             y['high'] = 0
#             y['low'] = dictionary[mid_state]/sub_total
#             y['positive'] = False
#             y['negative'] = True
#         else:
#             y['high'] = dictionary[mid_state]/sub_total
#             y['low'] = 0
#             y['positive'] = False
#             y['negative'] = True
    
#     emotional_state = ''
    
#     if y['positive']:
#         if y['high'] > 0 and y['high'] <= 0.33:
#             emotional_state = emotional_states['C1'][2]
#         elif y['high'] > 0.33 and y['high'] <= 0.66:
#             emotional_state = emotional_states['C1'][1]
#         elif y['high'] > 0.66:
#             emotional_state = emotional_states['C1'][0]
#         elif y['low'] > 0 and y['low'] <= 0.33:
#             emotional_state = emotional_states['C4'][2]
#         elif y['low'] > 0.33 and y['low'] <= 0.66:
#             emotional_state = emotional_states['C4'][1]
#         elif y['low'] > 0.66:
#             emotional_state = emotional_states['C4'][0]
#     else:
#         if y['high'] > 0 and y['high'] <= 0.33:
#             emotional_state = emotional_states['C2'][2]
#         elif y['high'] > 0.33 and y['high'] <= 0.66:
#             emotional_state = emotional_states['C2'][1]
#         elif y['high'] > 0.66:
#             emotional_state = emotional_states['C2'][0]
#         elif y['low'] > 0 and y['low'] <= 0.33:
#             emotional_state = emotional_states['C3'][2]
#         elif y['low'] > 0.33 and y['low'] <= 0.66:
#             emotional_state = emotional_states['C3'][1]
#         elif y['low'] > 0.66:
#             emotional_state = emotional_states['C3'][0]
            
#     print(dictionary, y, emotional_state)
#     return emotional_state
            
 
# @app.route('/inputdata', methods=['GET', 'POST'])
# def input_data():
#     if request.method == 'POST':
#         data = request.get_json()
#         if data: # check if data is valid
#             # Convert the list to a JSON string
#             json_data = json.dumps(data)
#             # Load JSON data into a pandas dataframe
#             datapd = pd.read_json(json_data)
#             results = evaluate_model(model, datapd)
#             emotional_state = process_results(results)
#             return jsonify(emotional_state), 200
#         else:
#             return jsonify({"error": "Invalid JSON data"}), 400
#     else:
#         return jsonify({"error": "Please make a POST request with JSON data to input data"}), 405

# if __name__ == '__main__':
#     app.run()