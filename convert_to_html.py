import os
import argparse
from nbconvert import HTMLExporter
from glob import glob


def _sanitize_surrogates(text: str) -> str:
    """
    Replace any Unicode surrogate code points (D800–DFFF) with the
    Unicode replacement character to avoid encoding errors when writing
    as UTF-8. These can sneak in from corrupted inputs.
    """
    if not text:
        return text
    return "".join(
        (ch if not (0xD800 <= ord(ch) <= 0xDFFF) else "\uFFFD")
        for ch in text
    )


def _resolve_notebooks(inputs):
    """Resolve input notebook paths or glob patterns to concrete files."""
    if inputs:
        files = []
        for pattern in inputs:
            if os.path.isfile(pattern) and pattern.lower().endswith('.ipynb'):
                files.append(pattern)
            else:
                files.extend(glob(pattern))
        # De-duplicate while preserving order and only keep .ipynb
        seen = set()
        ordered = []
        for f in files:
            if f not in seen and f.lower().endswith('.ipynb'):
                seen.add(f)
                ordered.append(f)
        return ordered
    else:
        return glob('*.ipynb')


def convert_notebooks_to_html(inputs=None):
    # Initialize HTML exporter
    html_exporter = HTMLExporter()
    
    # Determine which notebooks to convert
    notebooks = _resolve_notebooks(inputs)
    if not notebooks:
        print("No notebooks found to convert.")
        return
    
    for notebook in notebooks:
        try:
            # Convert the notebook
            (body, resources) = html_exporter.from_filename(notebook)
            # Sanitize potential surrogate code points to keep encoding safe
            body = _sanitize_surrogates(body)
            
            # Create HTML filename
            html_file = os.path.splitext(notebook)[0] + '.html'
            
            # Write the HTML file
            # Use errors='replace' as an extra safety net so conversion
            # doesn't fail on any remaining unexpected characters.
            with open(html_file, 'w', encoding='utf-8', errors='replace') as f:
                f.write(body)
                
            print(f"Successfully converted {notebook} to {html_file}")
            
        except Exception as e:
            print(f"Error converting {notebook}: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebooks to HTML."
    )
    parser.add_argument(
        'inputs',
        nargs='*',
        help=(
            "Notebook paths or glob patterns "
            "(default: all *.ipynb in current directory)"
        ),
    )
    args = parser.parse_args()
    convert_notebooks_to_html(args.inputs)
