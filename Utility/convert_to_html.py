import os
import nbconvert
from nbconvert import HTMLExporter
from glob import glob

def convert_notebooks_to_html():
    # Initialize HTML exporter
    html_exporter = HTMLExporter()
    
    # Get all .ipynb files in current directory
    notebooks = glob('*.ipynb')
    
    for notebook in notebooks:
        try:
            # Convert the notebook
            (body, resources) = html_exporter.from_filename(notebook)
            
            # Create HTML filename
            html_file = os.path.splitext(notebook)[0] + '.html'
            
            # Write the HTML file
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(body)
                
            print(f"Successfully converted {notebook} to {html_file}")
            
        except Exception as e:
            print(f"Error converting {notebook}: {str(e)}")

if __name__ == "__main__":
    convert_notebooks_to_html()
