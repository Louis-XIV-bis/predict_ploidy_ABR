import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys

# Extract and flatten ABR values from the dataframe
def extract_abr_values(df: pd.DataFrame) -> list:
    """
    Extract and flatten ABR values from the 'ABR' column.
    
    Args:
        df (pd.DataFrame): DataFrame containing the 'ABR' column.
    
    Returns:
        list: List of ABR values.
    """
    abr_values = []
    for abr in df['ABR']:
        # Check if ABR is a string (list of values separated by commas)
        if isinstance(abr, str):
            abr_values.extend([float(x) for x in abr.split(',')])
        elif pd.notna(abr):  # If ABR is a single float or non-null
            abr_values.append(float(abr))
    return abr_values

# Plot the violin plot of ABR values
def plot_violin(abr_values: list, strain: str) -> None:
    """
    Create a violin plot for the given ABR values.
    
    Args:
        abr_values (list): List of ABR values to plot.
        path (str): Path to save the plot.
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 6))
    
    # Create the violin plot
    sns.violinplot(data=abr_values)
    
    # Add labels and title
    plt.title(f'{strain}')
    plt.xlabel('ABR')
    
    plt.savefig(path)

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
    df = pd.read_csv(input_file, sep="\t", low_memory=False)

    # Extract and flatten the ABR values
    abr_values = extract_abr_values(df)
    
    # Plot the violin plot with filtered ABR values
    plot_violin(filtered_abr_values, output_file)