import csv
import os

def filter_and_write_csv(input_file, output_folder, output_file, filter_by, column_to_filter_on):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Specify the output file path
    output_file_path = os.path.join(output_folder, f'{output_file}.csv')

    # Open the input CSV file for reading
    with open(input_file, 'r') as input_csv:
        # Create a CSV reader
        reader = csv.reader(input_csv)

        # looking in column E (4th column)
        column_index = column_to_filter_on

        # Filter rows based on the condition
        filtered_rows = [row for row in reader if row[column_index] in filter_by]

    # Check if there are any matching rows to write
    if filtered_rows:
        # Open the output CSV file for writing
        with open(output_file_path, 'w', newline='') as output_csv:
            # Create a CSV writer
            writer = csv.writer(output_csv)

            # Write the filtered rows to the output file
            writer.writerows(filtered_rows)

        print(f"Filtered data written to {output_file_path}")

""" # Example usage
input_file_path = 'path/to/your/input_file.csv'
output_folder_path = 'path/to/your/output_folder'
output_file_name = 'GCP'
filter_strings = ['gcp', 'pgcp']

filter_and_write_csv(input_file_path, output_folder_path, output_file_name, filter_strings) """