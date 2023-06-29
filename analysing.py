import os
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt


############Set Data Here################
# Define the name variable
name = '1of2(2)_Iwood_1'
graph_show = True
graph_save = True
############Set Data Here################


def custom_converter(value):
    try:
        # Try to convert the value to a float
        return float(value)
    except ValueError:
        return 0

# Get the current directory
current_directory = os.getcwd()

# Define the folder path
folder_path = os.path.join(current_directory, "Data", name)

# Get a list of all files in the folder
files = os.listdir(folder_path)

# Filter only the CSV files
csv_files = [file for file in files if file.endswith(".csv")]
dataList = []

# Process each CSV file
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, usecols=[4], converters={4: custom_converter})

    # Extract the pulse signal
    signal = df.iloc[:, 0].values[5:]
    dataList.extend(signal)
    print(signal[0])

# Define pulse length and step
dataList = np.array(dataList)
print(len(dataList))

plt.plot(np.arange(len(dataList)), dataList)

# Set labels and title
plt.xlabel('Index')
plt.ylabel('Value')
plt.title( name + 'Graph')
plt.xlim(0, len(dataList) - 1)



# Create a DataFrame from the dataList
df_export = pd.DataFrame(dataList, columns=['Value'])

# Define the merged data folder path
merged_data_folder_path = os.path.join(current_directory, "merged_Data")
merged_graph_folder_path = os.path.join(current_directory, "merged_Graph")
# Create a merged data directory if it does not exist
if not os.path.exists(merged_data_folder_path):
    os.makedirs(merged_data_folder_path)
    
if not os.path.exists(merged_graph_folder_path):
    os.makedirs(merged_graph_folder_path)

# Define the export file path
export_file_path = os.path.join(merged_data_folder_path, name + '.csv')
if graph_save == True:
    plt.savefig(os.path.join(merged_graph_folder_path, name + '.png'), format = 'png')
    
# Display the plot
if graph_show == True:
    plt.show()

# Write DataFrame to a CSV file
df_export.to_csv(export_file_path, index=False)
