# import pandas as pd

# pd_a = pd.read_csv('../assets/emotions.csv')

# print(pd_a)

# for i in range(10):
#     randompd = pd_a.sample(n=500)
#     randompd = randompd.drop(['label'], axis=1)
#     randompd.to_json(f'sample_subject_{i}.json', orient='records')
    
import pandas as pd
import numpy as np

# Original dataframe with 2000k rows
df = pd.read_csv("../assets/emotions.csv")

# Group the dataframe by the label column
grouped = df.groupby("label")

# Initialize an empty list to store the selected rows

for i in range(20):
    n_samples = {"POSITIVE": np.random.randint(20, 100), 
                 "NEGATIVE": np.random.randint(20, 100), 
                 "NEUTRAL": np.random.randint(20, 100)}
    selected_rows = []
    # Loop through each group and select random rows
    for name, group in grouped:
        n = n_samples.get(name, 0)
        if n > 0:
            selected_rows.extend(group.sample(n=n).index.tolist())

    # Create a new dataframe with the selected rows
    df_random = df.loc[selected_rows]
    df_random = df_random.drop(['label'], axis=1)
    # Export the new dataframe to JSON format
    df_random.to_json(f"sample_dataset_subject{i+10}.json", orient="records")