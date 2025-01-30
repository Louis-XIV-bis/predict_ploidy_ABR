import sys
import pandas as pd

def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the dataset from a tab-separated file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        pd.DataFrame: Dataframe containing the loaded dataset.
    """
    # Read file as string to prevent dtype warnings, then handle conversions
    df = pd.read_csv(file_path, sep="\t", dtype=str, low_memory=False)

    # Convert "." to NaN
    df.replace(".", pd.NA, inplace=True)

    # Convert DP column to numeric, replacing NaN with 0 if needed
    df['DP'] = pd.to_numeric(df['DP'], errors='coerce')

    return df


def compute_abr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute ABR (Allele Balance Ratio) for each site and add a new column.

    ABR is calculated as AD divided by DP for each allele in the AD column.

    Args:
        df (pd.DataFrame): Input dataframe with DP and AD columns.

    Returns:
        pd.DataFrame: Dataframe with an added ABR column.
    """
    # Drop rows where DP or AD is missing
    df.dropna(subset=['DP', 'AD'], inplace=True)

    # Convert DP to numeric if not already
    df['DP'] = pd.to_numeric(df['DP'], errors='coerce')

    # Compute ABR per allele
    def compute_row_abr(row: pd.Series) -> str:
        """
        Compute ABR (Allele Balance Ratio) for a single row.

        Args:
            row (pd.Series): Row of the dataframe containing 'DP' and 'AD'.

        Returns:
            str: A comma-separated string representing ABR values for each allele.
        """
        if row['DP'] == 0:  # Prevent division by zero
            return ""
        
        ad_values = row['AD'].split(",")  # Split AD values into a list
        ad_values = [pd.to_numeric(x, errors='coerce') for x in ad_values]  # Convert to numeric

        # Compute ABR for each allele, return empty string for NaN values
        abr_values = [
            f"{x / row['DP']:.2f}" if pd.notna(x) else "" for x in ad_values
        ]
        return ",".join(abr_values)  # Join the ABR values without extra commas

    # Apply function to each row
    df['ABR'] = df.apply(compute_row_abr, axis=1)

    return df


def main() -> None:
    """
    Main function to load data, compute ABR, and save the updated dataset.
    """
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python compute_ABR.py <input_file> <output_file>")
        sys.exit(1)
    
    # Define input and output paths
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Load the dataset
    df = load_dataset(input_file)
    
    # Compute ABR and add it to the dataset
    df = compute_abr(df)
    
    # Save the updated dataset to a new file
    df.to_csv(output_file, sep='\t', index=False)