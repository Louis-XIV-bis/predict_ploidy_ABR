import pandas as pd
import numpy as np
import sys


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
    Compute bin counts for ABR values and generate a binned summary for a given strain.

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

    # Initialize a dictionary to store bin counts
    bin_counts = {label: 0 for label in bin_labels}

    # Flatten ABR values and assign them to bins
    for abr_list in df["ABR"]:
        for abr_value in abr_list:  # Process each value in the ABR list
            bin_index = np.digitize(abr_value, bin_edges, right=False) - 1  # Find bin index
            if 0 <= bin_index < len(bin_labels):  # Ensure valid index
                bin_counts[bin_labels[bin_index]] += 1  # Increment count in the correct bin

    # Convert dictionary to a dataframe
    binned_counts_df = pd.DataFrame([bin_counts])

    return binned_counts_df

def main() -> None:    """
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
    binned_counts_df = compute_binned_counts(df, strain)

    # Save the final dataset to a new file
    binned_counts_df.to_csv(output_file, index=False)