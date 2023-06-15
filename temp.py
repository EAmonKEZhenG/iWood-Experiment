import pandas as pd

data = pd.read_csv("merged_data.csv")
print(data['Value'].max())