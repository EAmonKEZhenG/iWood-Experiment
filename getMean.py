import pandas as pd
import numpy as np
import os

# Define the filename
filename = 'hardwood3.csv'

# Define the folder where all csv files are stored
folder_path = "merged_Data"

# Create the full file path by joining the folder path and the filename
full_file_path = os.path.join(folder_path, filename)

# Load the data from the CSV
df = pd.read_csv(full_file_path)

# Extract the 'Value' column to a numpy array
data = df['Value'].values

# Define the radius
radius = 1000

# Define a list to store the indices of the maximum values
max_indices = []

# Define a list to store the maximum and minimum values
max_values = []
min_values = []

# Define a list to store the differences
differences = []

# Loop until we find 26-28 maximum values
while len(max_indices) < 28:
    # If we have already found 26 maximum values, break the loop
    if len(max_indices) == 26:
        break

    # Find the index of the maximum value in the data
    max_index = np.argmax(data)

    # Add the index to the list
    max_indices.append(max_index)

    # Add the maximum value to the list
    max_values.append(data[max_index])

    # We use a dynamically increasing window to find the minimum value
    local_min = np.inf
    for r in range(radius, len(data), radius):
        window_start = max(0, max_index - r)
        window_end = min(len(data) - 1, max_index + r)
        
        # Copy the window data to avoid mutating the original data
        window_data = np.copy(data[window_start:window_end])
        
        # Find the minimum value that's not -np.inf
        window_data = window_data[window_data != -np.inf]
        if window_data.size != 0:
            current_min = np.min(window_data)

            # If current_min is a finite value (not inf), assign it to local_min
            if np.isfinite(current_min):
                local_min = current_min
                break

    # Add the minimum value to the list
    min_values.append(local_min)

    # Calculate the difference between the maximum and minimum values
    difference = data[max_index] - local_min

    # Add the difference to the list
    differences.append(difference)

    # Set the values in a window around the maximum to -np.inf
    data[max(0, max_index - radius):min(len(data) - 1, max_index + radius)] = -np.inf

# Calculate the mean of the differences
mean_difference = np.mean(differences)

# Create a new DataFrame which only includes the finite values
finite_data = df['Value'][np.isfinite(df['Value'])]

# Calculate the standard deviation of the finite data
std_dev = np.std(finite_data.values)

print("Number of NaN values in the data: ", np.sum(np.isnan(df['Value'].values)))
print("Number of infinite values in the data: ", np.sum(np.isinf(df['Value'].values)))


# Calculate the SNR
snr = 20 * np.log10(mean_difference / std_dev)
# print("The value is: ", mean_difference , ", " , std_dev , ", " , mean_difference/std_dev )

print("Mean difference:", mean_difference)
print("SNR:", snr)

# Remove the extension from the original filename
base_filename = filename.split('.')[0]

# Create a new filename for the output
output_filename = base_filename + '_result.txt'

# Create a results directory if it does not exist
if not os.path.exists('results'):
    os.makedirs('results')

# Write the differences to the output file inside the results directory
counter = 0
with open(os.path.join('results', output_filename), 'w') as f:
    f.write('This result is for: ' + filename + '\n')  # write filename
    for diff in differences:
        f.write(str(diff) + '\n')  # write each difference value
        counter +=1
        
    f.write('Total count is: ' +  str(counter) + '\n')  # write the mean difference
    f.write('Mean Difference: ' +  str(mean_difference) + '\n')  # write the mean difference
    f.write('SNR: ' + str(snr))  # write the SNR
