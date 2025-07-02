# CleanSync - Smart Data Cleaning & Preprocessing Tool

## Overview
CleanSync is an intelligent web-based tool that helps you clean and preprocess your data with just a few clicks. Whether you're working with CSV or Excel files, CleanSync makes data cleaning effortless and efficient.

## Features
- User-friendly web interface
- Support for CSV and Excel files
- Multiple data cleaning options
- Real-time data preview
- Download cleaned data in multiple formats

## Quick Start Guide

1. Install the required dependencies:
```
pip install -r requirements.txt
```

2. Start the application:
```
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

4. Upload your data file (CSV or Excel)

5. Select cleaning options:
   - Handle duplicates
   - Handle missing values (numeric)
   - Handle missing values (categorical)
   - Handle outliers
   - Encode categorical variables

6. Click "Start Cleaning"

7. Preview and download the cleaned data

## Project Structure

```
CleanSync/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── sample_data.csv       # Sample data for testing
├── templates/
│   └── index.html        # Main web interface
└── static/
    ├── style.css         # CSS styles
    ├── script.js         # Frontend functionality
    └── upload-icon.svg   # Upload icon
```

## Dependencies

- Flask==2.0.1
- pandas==1.3.3
- numpy==1.21.2
- scikit-learn==0.24.2
- openpyxl==3.0.7
- werkzeug==2.0.1

## Sample Data

The project includes a sample dataset (`sample_data.csv`) with 150 employee records containing various data quality issues:
- Duplicate records
- Categorical data
- Outliers
- Date formats
- Boolean values

## Contributing

We welcome contributions to CleanSync! Feel free to:
- Submit bug reports
- Suggest new features
- Create pull requests
- Improve documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or support, please open an issue in the repository. 