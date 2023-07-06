import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# Define the directory to read the files from
input_directory_name = 'merged_Data'

# Define the directory to save the result
output_directory_name = 'electromagnetic_noise_result'

# Construct the full paths based on the directory names
input_directory = os.path.join(os.getcwd(), input_directory_name)
output_directory = os.path.join(os.getcwd(), output_directory_name)

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Define the prefix for files to analyze
prefix = "IWood_without_"

# Find all files that start with the defined prefix
files = glob.glob(os.path.join(input_directory, f"{prefix}*.csv"))

average_noises = []
file_names = []

# Iterate over each file in the directory
for file in files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file)

    # Calculate the average noise
    avg_noise = df['Value'].abs().sum() / len(df)
    average_noises.append(avg_noise)

    # Extract the base of the filename without extension for plot labels and output filenames
    base_filename = os.path.basename(file)
    base_filename_no_ext = os.path.splitext(base_filename)[0]

    # Here, we split the base filename on underscore and take the last element as label
    x_label = base_filename_no_ext.split('_')[-1]
    file_names.append(x_label)

    # Prepare the output filename
    output_filename = os.path.join(output_directory, f"{base_filename_no_ext}.txt")

    # Write the average noise to the output file
    with open(output_filename, 'w') as output_file:
        output_file.write(f"Average Noise: {avg_noise}")

# Create bar plot of average noises
plt.bar(file_names, average_noises)

# Set the labels and title
plt.xlabel('File')
plt.ylabel('Average Noise')
plt.title('Average Noise per File')

# Rotate x-axis labels for better readability
plt.xticks(rotation='vertical')

# Save the plot with the prefix as the filename
plt.savefig(os.path.join(output_directory, f'{prefix}Average_Noise_Bar_Plot.png'))

# Show the plot
plt.show()
