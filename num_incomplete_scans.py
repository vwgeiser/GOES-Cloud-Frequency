import glob

# Path to the directory containing the .txt files
directory_path = 'D:/GOES_CF_RASTERS/incomplete and missing scans/'

# Use glob to get a list of all .txt files in the directory
txt_files = glob.glob(directory_path + '*.txt')

# Initialize total count for lines starting with 's'
total_s_count = 0

# Initialize total count for numbers in lines starting with 'Max scans for'
total_max_scans = 0

# Iterate over each .txt file
for file_path in txt_files:
    # Open the file
    with open(file_path, 'r') as file:
        # Initialize count for lines starting with 's' for this file
        s_count = 0
        # Initialize sum for numbers in lines starting with 'Max scans for' for this file
        max_scans_sum = 0
        # Iterate through each line in the file
        for line in file:
            # Check if the line starts with 's'
            if line.startswith('s'):
                s_count += 1
            # Check if the line starts with 'Max scans for'
            elif line.startswith('Max scans for'):
                # Extract the number from the line
                number = int(line.split()[-1])
                # Add the number to the sum
                max_scans_sum += number
                # print(number)
        # Print the count for lines starting with 's' for this file
        print("Number of lines starting with 's' in", file_path, ":", s_count)
        # Add the count for lines starting with 's' for this file to the total count
        total_s_count += s_count
        # Print the sum for numbers in lines starting with 'Max scans for' for this file
        print("Sum of numbers in lines starting with 'Max scans for' in", file_path, ":", max_scans_sum)
        # Add the sum for numbers in lines starting with 'Max scans for' for this file to the total sum
        total_max_scans += max_scans_sum

# Print the total count for lines starting with 's'
print("Total number of lines starting with 's' in all files:", total_s_count)

# Print the total sum for numbers in lines starting with 'Max scans for'
print("Total sum of numbers in lines starting with 'Max scans for' in all files:", total_max_scans)
