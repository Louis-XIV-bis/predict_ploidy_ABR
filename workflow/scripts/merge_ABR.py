import pandas as pd
import sys
from typing import List
import os

def merge_csv_files(input_files: List[str], output_file: str) -> None:
    """
    Merges multiple CSV files into a single CSV file, keeping the header only from the first file
    and stacking the rows from subsequent files beneath. Adds a 'strain' column, derived from the
    file name (by removing "_ABR_filtered_binned.csv").

    Args:
        input_files (List[str]): A list of file paths to the input CSV files.
        output_file (str): The file path for the merged output CSV.

    Returns:
        None
    """
    # Initialize an empty list to hold DataFrames
    df_list = []
    
    for i, file in enumerate(input_files):
        # Extract strain from the file name by removing "_ABR_filtered_binned.csv"
        strain = os.path.basename(file).replace("_ABR_filtered_binned.csv", "")
        
        # Read each file, and only skip the header for subsequent files
        if i == 0:
            df = pd.read_csv(file)  # Read the first file with header
        else:
            df = pd.read_csv(file, header=0)  # Skip header for other files
        
        # Add the 'strain' column
        df.insert(0, 'strain', strain)  # Insert at the beginning (index 0)
        
        # Append the DataFrame to the list
        df_list.append(df)
    
    # Concatenate all DataFrames, stacking them vertically (row-wise)
    merged_df = pd.concat(df_list, ignore_index=True)

    # Save the merged DataFrame to the output file
    merged_df.to_csv(output_file, index=False)

def main() -> None:
    """
    Main function to merge multiple CSV files while ensuring only the first file retains its header,
    and adds a 'strain' column derived from the file name.
    """
    # Ensure correct number of arguments
    if len(sys.argv) < 3:
        print("Usage: python merge_ABR.py <input_file1> <input_file2> ... <output_file>")
        sys.exit(1)
    
    # Define input file list and output file path
    input_files = sys.argv[1:-1]  # All arguments except the last one are input files
    output_file = sys.argv[-1]  # Last argument is the output file

    # Merge CSV files
    merge_csv_files(input_files, output_file)

if __name__ == "__main__":
    main()
