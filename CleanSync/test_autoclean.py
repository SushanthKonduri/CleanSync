import pandas as pd
from autoclean import CleanSync

# Create a sample dataset with some issues
data = {
    'name': ['John', 'Jane', 'John', None, 'Bob'],
    'age': [25, 30, 25, 40, 1000],  # 1000 is an outlier
    'salary': [50000, None, 50000, 60000, 55000],
    'date': ['2023-01-01', '2023-02-01', '2023-01-01', '2023-04-01', '2023-05-01']
}

df = pd.DataFrame(data)

# Run CleanSync
cleaner = CleanSync(
    df,
    mode='auto',  # Automatic cleaning
    duplicates='auto',  # Remove duplicates
    missing_num='auto',  # Handle missing numerical values
    missing_categ='auto',  # Handle missing categorical values
    encode_categ=['auto'],  # Encode categorical variables
    extract_datetime='D',  # Extract date components
    outliers='winz',  # Handle outliers using winsorization
    verbose=True  # Show detailed logs
)

# Get the cleaned dataframe
cleaned_df = cleaner.output

print("\nOriginal DataFrame:")
print(df)
print("\nCleaned DataFrame:")
print(cleaned_df)
