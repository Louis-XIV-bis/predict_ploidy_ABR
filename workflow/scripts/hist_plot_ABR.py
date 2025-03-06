import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import re 
import ast 

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
    
    # Convert ABR column from string to actual list
    df["ABR"] = df["ABR"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    for abr_list in df["ABR"]:
        if isinstance(abr_list, list):  # Ensure it's a list
            abr_values.extend([float(x) for x in abr_list])  # Append all float values
        elif pd.notna(abr_list):  # If it's a single float value, append directly
            abr_values.append(float(abr_list))

    return abr_values

def plot_histogram(abr_values: list, path: str) -> None:
    """
    Create a histogram for the given ABR values.
    
    Args:
        abr_values (list): List of ABR values to plot.
        path (str): Path to save the plot.
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 4))
    
    strain_match = re.search(r"results/hist_ABR/(.+)_ABR_filtered_hist\.png", path)
    strain = strain_match.group(1)

    # Create the histogram
    sns.histplot(abr_values, bins=20, kde=False)
    plt.xlim(0, 1)
    plt.xticks([i * 0.1 for i in range(11)])  # Set x-axis ticks every 0.1

    # Add labels and title
    plt.title(strain)
    plt.xlabel('Allele balance ratio (ABR)')
    plt.ylabel('Count')
    
    plt.savefig(path, bbox_inches='tight')
    plt.close()

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
    df = pd.read_csv(input_file, sep='\t', low_memory=False)

    # Extract and flatten the ABR values
    abr_values = extract_abr_values(df)
    
    # Plot the violin plot with filtered ABR values
    plot_histogram(abr_values, output_file)
if __name__ == "__main__":
    main()