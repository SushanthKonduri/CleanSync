import pandas as pd
from CleanSync import CleanSync
import sys

try:
    # Create a sample dataframe with some data cleaning challenges
    print("Creating sample dataframe...")
    data = {
        'numeric_col': [1, 2, None, 4, 5, 1000],  # Contains missing value and outlier
        'categorical_col': ['A', 'B', 'A', None, 'C', 'A'],  # Contains missing value
        'duplicate_col': [1, 1, 1, 2, 2, 2]  # Contains duplicates
    }
    df = pd.DataFrame(data)

    print("\nOriginal DataFrame:")
    print(df)
    print("\nDataFrame Info:")
    print(df.info())

    # Initialize CleanSync with automatic mode
    print("\nInitializing CleanSync...")
    cleaner = CleanSync(
        input_data=df,
        mode='auto',  # Use automatic mode
        duplicates='auto',  # Handle duplicates automatically
        missing_num='auto',  # Handle numerical missing values automatically
        missing_categ='auto',  # Handle categorical missing values automatically
        encode_categ=['auto'],  # Encode categorical features automatically
        outliers='winz',  # Handle outliers using winsorization
        verbose=True  # Show progress in console
    )

    # Get the cleaned dataframe
    print("\nGetting cleaned dataframe...")
    cleaned_df = cleaner.output

    # Print the results
    print("\nCleaned DataFrame:")
    print(cleaned_df)
    print("\nCleaned DataFrame Info:")
    print(cleaned_df.info())

except Exception as e:
    print(f"An error occurred: {str(e)}", file=sys.stderr)
    raise 