import pandas as pd
import numpy as np
import os

###############################
filename = 'IWood_1.csv'
folder_path = "merged_Data"
radius = 1000       
threshold = 1000    ## SNR
output_paht = 'thickness_result'
################################
# Create the full file path by joining the folder path and the filename
full_file_path = os.path.join(folder_path, filename)

# Load the data from the CSV
df = pd.read_csv(full_file_path)

# Extract the 'Value' column to a numpy array
data = df['Value'].values

# Define the radius
# radius = 1000

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


# threshold = 1000

# Use pandas to get frequency counts for all numbers, including negatives
freq_counts = pd.Series(data[np.isfinite(data)]).value_counts()

# Only keep numbers that appear more than 'threshold' times
high_frequency_values = freq_counts[freq_counts > threshold].index.values

# Make sure there are high frequency values
if high_frequency_values.size == 0:
    raise ValueError("No values found with frequency over the threshold.")

# Find the maximum and minimum of the high-frequency values
avg_noise = high_frequency_values.max() - high_frequency_values.min()


# Calculate the SNR
snr = 10* np.log10(mean_difference**2 / avg_noise**2)

# print("Number of NaN values in the data: ", np.sum(np.isnan(df['Value'].values)))
# print("Number of infinite values in the data: ", np.sum(np.isinf(df['Value'].values)))

print("Signal:", mean_difference)
print("The max get from noise: ", high_frequency_values.max())
print("The min get from noise: ", high_frequency_values.min())
print("Average Noise:", avg_noise)
print("SNR:", snr)

# Remove the extension from the original filename
base_filename = filename.split('.')[0]

# Create a new filename for the output
output_filename = base_filename + '_result.txt'

# Create a results directory if it does not exist
if not os.path.exists(output_paht):
    os.makedirs(output_paht)

# Write the differences to the output file inside the results directory
counter = 0
with open(os.path.join(output_paht, output_filename), 'w') as f:
    f.write('This result is for: ' + filename + '\n')  # write filename
    for diff in differences:
        f.write(str(diff) + '\n')  # write each difference value
        counter +=1
        
    f.write('Total count is: ' +  str(counter) + '\n')  # write the mean difference
    f.write('Noise Max: ' + str(high_frequency_values.max()) + '\n')
    f.write('Noise Min: ' + str(high_frequency_values.min()) + '\n')
    f.write('Signal: ' +  str(mean_difference) + '\n')  # write the mean difference
    f.write('Average Noise: ' + str(avg_noise) + '\n') # write the average noise
    f.write('SNR: ' + str(snr))  # write the SNR
