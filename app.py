from flask import Flask, render_template, request, jsonify
import pandas as pd
from CleanSync import CleanSync
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clean', methods=['POST'])
def clean_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read the file based on its extension
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        # Get cleaning options from the form
        duplicates = request.form.get('duplicates') == 'true'
        missing_num = request.form.get('missingNum') == 'true'
        missing_categ = request.form.get('missingCateg') == 'true'
        outliers = request.form.get('outliers') == 'true'
        encode_categ = request.form.get('encodeCateg') == 'true'
        
        # Initialize CleanSync with the selected options
        cleaner = CleanSync(
            input_data=df,
            mode='manual',
            duplicates='auto' if duplicates else False,
            missing_num='auto' if missing_num else False,
            missing_categ='auto' if missing_categ else False,
            outliers='winz' if outliers else False,
            encode_categ=['auto'] if encode_categ else False,
            verbose=False
        )
        
        # Get the cleaned dataframe
        cleaned_df = cleaner.output
        
        # Generate preview of cleaned data
        preview = cleaned_df.head().to_string()
        
        # Convert cleaned data to CSV
        cleaned_csv = cleaned_df.to_csv(index=False)
        
        # Clean up the temporary file
        os.remove(filepath)
        
        return jsonify({
            'preview': preview,
            'cleaned_data': cleaned_csv
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True) 