#Braeden King 23/12/23
#Function reads from a csv with headers and splits into multiple files based on contents of column with header: column_to_split, writing only columns with headers in: columns_to_write into the split files

import csv
import os

def split_and_write_csv(input_file, output_folder, column_to_split, columns_to_write):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Dictionary to store output files
    output_files = {}

    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Get the value from the specified column
            column_value = row[column_to_split]

            # Create a new output file if it doesn't exist
            if column_value not in output_files:
                output_files[column_value] = open(os.path.join(output_folder, f"{column_value}.csv"), 'w', newline='')
                writer = csv.DictWriter(output_files[column_value], fieldnames=columns_to_write)

            # Check if any cell value is "0" before writing the row
            if not any(value == "0" for value in row.values()):
                # Write only specified columns to the appropriate output file
                writer.writerow({col: row[col] for col in columns_to_write})

    # Close all output files
    for file in output_files.values():
        file.close()

##Example
"""         
input_csv_V1 = os.path.join(os.path.expanduser("~"), "Downloads", "TitanV1.csv")

titanCSVFolder = r'C:\temp\titan'
column_to_split = 'Machine Name'
columns_to_write = ['Tooth Start Fill E', 'Tooth Start Fill N', 'Tooth Start Fill Alt']


split_and_write_csv(input_csv_V1, titanCSVFolder, column_to_split, columns_to_write) """