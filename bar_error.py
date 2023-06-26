import os
import re
import glob
import numpy as np
import matplotlib.pyplot as plt

####
show_graph = True
save_graph = True
###

# Ask the user for the directory to read the files from
directory_name = input("Enter the directory name to read the files from: ")

# Construct the full path based on the directory name
directory = os.path.join(os.getcwd(), directory_name)

# Get a list of all txt files in the directory
files = glob.glob(os.path.join(directory, "*.txt"))

# Initialize a dictionary to hold the signal values for each type of file
signals = {}
snrs = {}

# Define order of the file types
order = ['IWood', '3of4', '1of2', '3of8', '1of4', '1of8']

# Function to sort file types according to defined order
def sort_file_types(file_type):
    try:
        return order.index(file_type)
    except ValueError:
        return len(order)

# Iterate over each file in the directory
for filename in files:
    # Extract the base of the filename
    base_filename = os.path.basename(filename)
    
    # Extract the type of the file by splitting on the underscore and keeping the first part
    file_type = base_filename.split("_")[0]

    with open(filename, 'r') as file:
        # Read the lines of the file
        lines = file.readlines()
        
        # Iterate over each line
        for line in lines:
            # If the line starts with 'Signal:'
            if line.startswith('Signal:'):
                # Extract the number after 'Signal:'
                signal = float(re.findall("\d+\.\d+", line)[0])
                
                # If the file type is not already in the dictionary, add it
                if file_type not in signals:
                    signals[file_type] = []

                # Add the signal to the list for this file type
                signals[file_type].append(signal)

            # If the line starts with 'SNR:'
            if line.startswith('SNR:'):
                # Extract the number after 'SNR:'
                snr = float(re.findall("\d+\.\d+", line)[0])

                # If the file type is not already in the dictionary, add it
                if file_type not in snrs:
                    snrs[file_type] = []

                # Add the SNR to the list for this file type
                snrs[file_type].append(snr)
                break

# Prepare the data for the bar plot
file_types = list(signals.keys())
file_types.sort(key=sort_file_types)

avg_signals = [np.mean(signals[file_type]) for file_type in file_types]
std_signals = [np.std(signals[file_type]) for file_type in file_types]

avg_snrs = [np.mean(snrs[file_type]) for file_type in file_types]
std_snrs = [np.std(snrs[file_type]) for file_type in file_types]

# Create the bar plot with error bars for signals
plt.figure()
plt.bar(file_types, avg_signals, yerr=std_signals, capsize=10)

# Set the labels and title
plt.xlabel('Thickness')
plt.ylabel('Average Signal')
plt.title('Average Signal per Thickness')
if save_graph == True:
    # Save the plot
    graph_directory = os.path.join(directory, 'graph')
    os.makedirs(graph_directory, exist_ok=True)
    plt.savefig(os.path.join(graph_directory, 'Average_Signal_Thickness.png'))

if show_graph == True:  
    # Show the plot
    plt.show()

# Create the bar plot with error bars for SNRs
plt.figure()
plt.bar(file_types, avg_snrs, yerr=std_snrs, capsize=10)

# Set the labels and title
plt.xlabel('Thickness')
plt.ylabel('Average SNR')
plt.title('Average SNR per File Type')
if save_graph == True:
    # Save the plot
    plt.savefig(os.path.join(graph_directory, 'Average_SNR_Thickness.png'))

if show_graph == True:  
    # Show the plot
    plt.show()
