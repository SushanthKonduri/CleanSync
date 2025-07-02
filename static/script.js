document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const optionsSection = document.getElementById('optionsSection');
    const resultsSection = document.getElementById('resultsSection');
    const cleanBtn = document.getElementById('cleanBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const originalPreview = document.getElementById('originalPreview');
    const cleanedPreview = document.getElementById('cleanedPreview');

    let currentFile = null;
    let cleanedData = null;

    // Drag and drop handlers
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('drag-over');
    }

    function unhighlight() {
        dropZone.classList.remove('drag-over');
    }

    dropZone.addEventListener('drop', handleDrop, false);
    fileInput.addEventListener('change', handleFileSelect, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length > 0) {
            currentFile = files[0];
            showOptions();
            previewOriginalData(currentFile);
        }
    }

    function showOptions() {
        optionsSection.style.display = 'block';
        resultsSection.style.display = 'none';
    }

    function previewOriginalData(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const data = e.target.result;
            if (file.name.endsWith('.csv')) {
                const rows = data.split('\n').slice(0, 6); // Show first 5 rows
                originalPreview.innerHTML = `<pre>${rows.join('\n')}</pre>`;
            } else {
                // For Excel files, we'll show a message that preview is not available
                originalPreview.innerHTML = '<p>Excel file preview not available. Data will be shown after cleaning.</p>';
            }
        };
        reader.readAsText(file);
    }

    cleanBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        loadingOverlay.style.display = 'flex';
        
        const formData = new FormData();
        formData.append('file', currentFile);
        formData.append('duplicates', document.getElementById('duplicates').checked);
        formData.append('missingNum', document.getElementById('missingNum').checked);
        formData.append('missingCateg', document.getElementById('missingCateg').checked);
        formData.append('outliers', document.getElementById('outliers').checked);
        formData.append('encodeCateg', document.getElementById('encodeCateg').checked);

        try {
            const response = await fetch('/clean', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Cleaning failed');
            }

            const result = await response.json();
            cleanedData = result.cleaned_data;
            
            // Show results
            resultsSection.style.display = 'block';
            cleanedPreview.innerHTML = `<pre>${result.preview}</pre>`;
            
        } catch (error) {
            alert('Error cleaning data: ' + error.message);
        } finally {
            loadingOverlay.style.display = 'none';
        }
    });

    downloadBtn.addEventListener('click', () => {
        if (!cleanedData) return;

        const blob = new Blob([cleanedData], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = currentFile.name.replace(/\.[^/.]+$/, '') + '_cleaned.csv';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    });
}); 