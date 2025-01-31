import sys
import pandas as pd

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

    # Filters to add in function :  ############################## 
    # Convert ABR to list of floats (if it's a comma-separated string of floats)
    df['ABR'] = df['ABR'].apply(lambda x: [float(i) for i in x.split(',')] if pd.notna(x) else [])

    # Remove values less than 0.125 or greater than 0.875
    df['ABR'] = df['ABR'].apply(lambda x: [i for i in x if 0.125 <= i <= 0.875])

    # Remove rows where all values are removed from ABR (i.e., the ABR list is empty)
    df = df[df['ABR'].apply(len) > 0]
      #   + somme ABR site != 1
    ##############################

    # Save the updated dataset to a new file
    df.to_csv(output_file, sep='\t', index=False)
  
if __name__ == "__main__":
    main()