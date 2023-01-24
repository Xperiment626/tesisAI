# This program aims to accurately predict the emotional states of a subject while watching various movie scenes given their EEG readings using a recurrent neural network
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
import json

"""
Data import for training and testing
"""

data = pd.read_csv('emotions.csv')
headers = np.array(data.columns)

"""
Trying to convert to json file
"""

data = {
    "headers": headers.tolist()
}

json_data = json.dumps(data)

# write the data to a json file
with open("data.json", "w") as outfile:
    outfile.write(json_data)