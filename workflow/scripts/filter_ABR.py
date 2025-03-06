import sys
import pandas as pd
from typing import List

def filter_abr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the ABR column in the dataset based on specific criteria.

    - Converts ABR values from comma-separated strings into lists of floats.
    - Keeps only sites where ABR has exactly 2 or 3 values.
    - Ensures the sum of ABR values is approximately 1.
    - Removes ABR values less than 0.125 or greater than 0.875.
    - Removes rows where all ABR values are filtered out.

    Args:
        df (pd.DataFrame): Input dataframe containing an 'ABR' column.

    Returns:
        pd.DataFrame: Filtered dataframe.
    """
    # Convert ABR to a list of floats (if it's a comma-separated string)
    df['ABR'] = df['ABR'].apply(lambda x: [float(i) for i in x.split(',')] if pd.notna(x) else [])

    # Keep sites only if ABR has exactly 2 or 3 values
    df = df[df['ABR'].apply(lambda x: len(x) in [2, 3])]

    # Filter sites if sum of ABR is not approximately 1
    df = df[df['ABR'].apply(lambda x: abs(sum(x) - 1) < 1e-6)]  # Account for float imprecision

    # Remove ABR values less than 0.125 or greater than 0.875: should be 8n or more to see peak here   
    df['ABR'] = df['ABR'].apply(lambda x: [i for i in x if 0.125 <= i <= 0.875])

    # Remove rows where all values are removed from ABR (i.e., empty lists)
    df = df[df['ABR'].apply(len) > 0]

    return df

def main() -> None:
    """
    Main function to load data, filter ABR values, and save the updated dataset.
    """
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python filter_ABR.py <input_file> <output_file>")
        sys.exit(1)
    
    # Define input and output paths
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Load the dataset
    df = pd.read_csv(input_file, sep="\t", low_memory=False)

    # Apply the filtering function
    df = filter_abr(df)

    # Save the updated dataset to a new file
    df.to_csv(output_file, sep='\t', index=False)
  
if __name__ == "__main__":
    main()
