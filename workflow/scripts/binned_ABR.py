import pandas as pd
import numpy as np
import sys
import ast

def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the dataset with ABR values.

    Args:
        file_path (str): Path to the ABR dataset.

    Returns:
        pd.DataFrame: Dataframe containing the ABR dataset.
    """
    df = pd.read_csv(file_path, sep='\t', dtype=str)
    df.replace(".", pd.NA, inplace=True)
    return df


def compute_binned_counts(df: pd.DataFrame, num_bins: int = 20) -> pd.DataFrame:
    """
    Compute bin counts for ABR values and generate a binned summary for a given     .

    Args:
        df (pd.DataFrame): Dataframe containing the 'ABR' column with lists of values.
        num_bins (int): Number of bins to divide ABR values into (default is 20).

    Returns:
        pd.DataFrame: Dataframe with binned counts, where each bin is a separate column.
    """
    # Define the bin edges from 0 to 1
    bin_edges = np.linspace(0, 1, num_bins + 1)
    
    # Create bin labels (intervals)
    bin_labels = [f"[{bin_edges[i]:.2f}-{bin_edges[i + 1]:.2f}]" for i in range(len(bin_edges) - 1)]

    # Initialize a dictionary for bin counts
    bin_counts = {label: 0 for label in bin_labels}

    # Convert ABR column from string to actual list
    df["ABR"] = df["ABR"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # Iterate over each row in the DataFrame
    for abr_list in df["ABR"]:
        for abr_value in abr_list:  
            # Find the bin index
            bin_index = np.digitize(abr_value, bin_edges, right=False) - 1  
            
            # Ensure valid index
            bin_index = min(bin_index, len(bin_labels) - 1)
            
            # Update bin count
            bin_counts[bin_labels[bin_index]] += 1  

    # Convert dictionary to a DataFrame
    binned_counts_df = pd.DataFrame([bin_counts])

    print(binned_counts_df)
    return binned_counts_df

def main() -> None:
    """
    Main function to load data, compute ABR, and save the updated dataset.
    """
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python filter_ABR.py <input_file> <output_file>")
        sys.exit(1)
    
    # Define input and output paths
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Load the dataset
    df = load_dataset(input_file)

    # Compute binned counts for ABR values
    binned_counts_df = compute_binned_counts(df)

    # Save the final dataset to a new file
    binned_counts_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()