import pandas as pd
import joblib
import sys
import sklearn
import os

# Load trained model with scaler (Pipeline())
MODEL_PATH = "workflow/scripts/model/ploidy_prediction_model.pkl"

def load_model_with_scaler(model_path):
    """
    Load the trained Random Forest model and StandardScaler.

    Args:
        model_path (str): Path to the trained model file. Contains a pipeline with scaler and model

    Returns:
        Loaded model.
    """
    if not os.path.exists(model_path):
        print(model_path)
        sys.exit("Error: Model w/ scaler file not found. Train the model first.")

    model = joblib.load(model_path)

    return model

def load_and_check_data(csv_file, expected_features):
    """
    Load new data from a CSV file and ensure it contains the required features.
    Normalize the counts into proportions.

    Args:
        csv_file (str): Path to the CSV file containing new data.
        expected_features (list): List of required feature names.

    Returns:
        pd.DataFrame: Processed DataFrame if valid, else exits.
    """
    if not os.path.exists(csv_file):
        sys.exit(f"Error: File '{csv_file}' not found.")

    try:
        data = pd.read_csv(csv_file)
    except Exception as e:
        sys.exit(f"Error reading CSV file: {e}")

    # Ensure all required features are present
    missing_features = [f for f in expected_features if f not in data.columns]
    if missing_features:
        sys.exit(f"Error: Missing required features in input data: {missing_features}")
    
    # Exclude the 'strain' (or other specified in main()) column from numeric columns
    numeric_columns = data.select_dtypes(include='number').columns 
    
    # Normalize counts into proportions
    row_sums = data[numeric_columns].sum(axis=1)
    data[numeric_columns] = data[numeric_columns].div(row_sums, axis=0).fillna(0)  # Replace NaN with 0

    return data

def predict_new_data(model, new_data, expected_features):
    """
    Scale the input data and make predictions using the trained model.

    Args:
        model: Trained RandomForestClassifier model.
        new_data (pd.DataFrame): Data to predict on.
        expected_features (list): List of required features.

    Returns:
        pd.DataFrame: DataFrame containing strain and predicted ploidy.
    """
    # Extract strain column if it exists
    strain_column = "strain" if "strain" in new_data.columns else None

    # Select only feature columns for prediction
    feature_data = new_data[expected_features]

    # Predict
    predictions = model.predict(feature_data)

    # Create a results DataFrame
    results = pd.DataFrame({
        "strain": new_data[strain_column] if strain_column else range(len(new_data)),
        "predicted_ploidy": predictions
    })

    return results

def main():
    """
    Main function to handle command-line arguments and run predictions.
    Uses sys.argv to get the input CSV filename.
    """
    if len(sys.argv) != 3:
        sys.exit("Usage: python predict.py <input_csv_file> <output_csv_file>")

    csv_file = sys.argv[1]
    output_file = sys.argv[2]

    # Define expected feature names (update based on your dataset)
    expected_features = [
        "[0.00-0.05]","[0.05-0.10]","[0.10-0.15]","[0.15-0.20]",
        "[0.20-0.25]","[0.25-0.30]","[0.30-0.35]","[0.35-0.40]",
        "[0.40-0.45]","[0.45-0.50]","[0.50-0.55]","[0.55-0.60]",
        "[0.60-0.65]","[0.65-0.70]","[0.70-0.75]","[0.75-0.80]",
        "[0.80-0.85]","[0.85-0.90]","[0.90-0.95]","[0.95-1.00]"]

    # Load model with scaler (pipeline)
    model = load_model_and_scaler(MODEL_PATH)

    # Load and validate input data
    new_data = load_and_check_data(csv_file, expected_features + ["strain"])  # Keep "strain" column if present
    print(new_data)
    # Make predictions
    results = predict_new_data(model, new_data, expected_features)

    # Save predictions to CSV
    results.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()