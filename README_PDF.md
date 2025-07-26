# PDF Outline Extractor

A Python script that runs offline in a Docker container and extracts hierarchical outlines from PDF files based on font properties and layout analysis.

## Features

- **Automatic Heading Detection**: Detects H1, H2, and H3 headings based on:
  - Font size analysis
  - Bold/italic styling
  - Text position and indentation
- **Document Title Extraction**: Extracts document title from the largest font text on the first page
- **Batch Processing**: Processes all PDF files from input directory
- **Offline Operation**: No internet access required, runs completely offline
- **Fast Performance**: Processes up to 50-page PDFs within 10 seconds

## Input/Output Format

### Input
- Place PDF files in `/app/input` directory
- Supports PDFs up to 50 pages each

### Output
- JSON files saved to `/app/output` directory
- Same filename as input (e.g., `document.pdf` → `document.json`)

### Output Format
```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "Background", "page": 2 },
    { "level": "H3", "text": "Historical Context", "page": 3 }
  ]
}
```

## Quick Start

### Option 1: Using Docker (Recommended)

1. **Build the Docker image**:
   ```bash
   docker build -t pdf-outline-extractor .
   ```

2. **Create directories for input and output**:
   ```bash
   mkdir -p ./pdf-input ./pdf-output
   ```

3. **Place your PDF files in the input directory**:
   ```bash
   cp your-documents/*.pdf ./pdf-input/
   ```

4. **Run the container**:
   ```bash
   docker run -v $(pwd)/pdf-input:/app/input -v $(pwd)/pdf-output:/app/output pdf-outline-extractor
   ```

5. **Check the results**:
   ```bash
   ls ./pdf-output/
   cat ./pdf-output/your-document.json
   ```

### Option 2: Running Locally

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create directories**:
   ```bash
   mkdir -p input output
   ```

3. **Place PDFs in input directory**:
   ```bash
   cp your-documents/*.pdf ./input/
   ```

4. **Run the script**:
   ```bash
   python main.py
   ```

5. **Check results in output directory**:
   ```bash
   ls ./output/
   ```

## How It Works

### Heading Detection Algorithm

1. **Font Analysis**: The script analyzes all text blocks in the PDF to identify:
   - Most common font size (assumed to be body text)
   - Larger font sizes that may indicate headings

2. **Heading Criteria**: Text is considered a heading candidate if it:
   - Has a font size significantly larger than body text (≥20% larger)
   - Is appropriately positioned (left-aligned or indented)
   - Has reasonable length (3-200 characters)
   - May be bold or italic formatted

3. **Level Assignment**: Heading levels are determined by:
   - Font size ranking (largest = H1, medium = H2, smaller = H3)
   - Context analysis within the document
   - Position and formatting cues

4. **Title Extraction**: Document title is extracted by:
   - Finding the largest font text on the first page
   - Filtering out headers/footers based on position
   - Selecting substantial text content

### Libraries Used

- **PyMuPDF (fitz)**: Primary library for PDF parsing and text extraction with detailed font information
- **Python Standard Library**: For file handling, JSON processing, and data structures

## Performance

- **Speed**: Processes 50-page PDFs in under 10 seconds
- **Memory**: Efficient memory usage with streaming text extraction
- **Compatibility**: Works with most PDF formats and layouts

## Troubleshooting

### Common Issues

1. **No headings detected**:
   - Check if PDF has clear font size differences
   - Verify PDF is not image-based (scanned document)
   - Try with PDFs that have distinct heading styles

2. **Incorrect title extraction**:
   - The script extracts title from largest font on first page
   - Some PDFs may have headers/footers with large fonts

3. **Missing text**:
   - Some PDFs may have text as images (OCR required)
   - Password-protected PDFs are not supported

### Debug Mode

To enable verbose logging, modify the script:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Docker Commands Reference

```bash
# Build image
docker build -t pdf-outline-extractor .

# Run with volume mounts
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-outline-extractor

# Run interactively for debugging
docker run -it -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-outline-extractor /bin/bash

# Check logs
docker logs <container-id>
```

## Examples

### Example 1: Academic Paper
Input: `research-paper.pdf`

Output: `research-paper.json`
```json
{
  "title": "Machine Learning in Healthcare: A Comprehensive Review",
  "outline": [
    { "level": "H1", "text": "Abstract", "page": 1 },
    { "level": "H1", "text": "Introduction", "page": 2 },
    { "level": "H2", "text": "Background and Motivation", "page": 2 },
    { "level": "H2", "text": "Research Questions", "page": 3 },
    { "level": "H1", "text": "Literature Review", "page": 4 },
    { "level": "H2", "text": "Supervised Learning Applications", "page": 4 },
    { "level": "H3", "text": "Image Classification", "page": 5 },
    { "level": "H3", "text": "Natural Language Processing", "page": 7 }
  ]
}
```

### Example 2: Technical Manual
Input: `user-manual.pdf`

Output: `user-manual.json`
```json
{
  "title": "Software Installation Guide v2.1",
  "outline": [
    { "level": "H1", "text": "Getting Started", "page": 1 },
    { "level": "H2", "text": "System Requirements", "page": 1 },
    { "level": "H2", "text": "Download Instructions", "page": 2 },
    { "level": "H1", "text": "Installation", "page": 3 },
    { "level": "H2", "text": "Windows Installation", "page": 3 },
    { "level": "H2", "text": "macOS Installation", "page": 5 },
    { "level": "H2", "text": "Linux Installation", "page": 7 }
  ]
}
```

## License

This project is open source and available under the MIT License.