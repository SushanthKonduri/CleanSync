import pandas as pd
from CleanSync import CleanSync
import sys

def clean_data(input_file):
    try:
        # Load your data
        print(f"Loading data from {input_file}...")
        
        # Detect file type and read accordingly
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        elif input_file.endswith('.xlsx') or input_file.endswith('.xls'):
            df = pd.read_excel(input_file)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel files.")

        print("\nOriginal DataFrame:")
        print(df.head())
        print("\nDataFrame Info:")
        print(df.info())
        
        # Check for data quality issues
        print("\nData Quality Report:")
        print("Missing values:\n", df.isnull().sum())
        print("\nDuplicated rows:", df.duplicated().sum())
        
        # Initialize CleanSync with automatic mode
        print("\nInitializing CleanSync...")
        cleaner = CleanSync(
            input_data=df,
            mode='auto',           # Use automatic mode for all cleaning steps
            duplicates='auto',     # Handle duplicates automatically
            missing_num='auto',    # Handle numerical missing values automatically
            missing_categ='auto',  # Handle categorical missing values automatically
            encode_categ=['auto'], # Encode categorical features automatically
            outliers='winz',       # Handle outliers using winsorization
            verbose=True           # Show progress in console
        )

        # Get the cleaned dataframe
        print("\nGetting cleaned dataframe...")
        cleaned_df = cleaner.output

        # Print the results
        print("\nCleaned DataFrame:")
        print(cleaned_df.head())
        print("\nCleaned DataFrame Info:")
        print(cleaned_df.info())
        
        # Save the cleaned data
        output_file = input_file.rsplit('.', 1)[0] + '_cleaned.' + input_file.rsplit('.', 1)[1]
        if input_file.endswith('.csv'):
            cleaned_df.to_csv(output_file, index=False)
        else:
            cleaned_df.to_excel(output_file, index=False)
        print(f"\nCleaned data saved to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_my_data.py <path_to_your_data_file>")
        print("Supported formats: CSV (.csv) or Excel (.xlsx, .xls)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    clean_data(input_file) 