# PDF Outline Extractor - Usage Instructions

## Quick Start

1. **Place your PDF files** in the `/app/input` directory
2. **Run the extractor**: `python main.py`
3. **Check results** in the `/app/output` directory

## Example Usage

```bash
# Ensure input and output directories exist
mkdir -p /app/input /app/output

# Copy your PDF files to input directory
cp your-document.pdf /app/input/

# Run the extraction
python main.py

# Check the results
ls /app/output/
cat /app/output/your-document.json
```

## Running with Docker

```bash
# Build the Docker image
docker build -t pdf-outline-extractor .

# Create local directories for file exchange
mkdir -p ./pdf-input ./pdf-output

# Place your PDFs in the input directory
cp your-documents/*.pdf ./pdf-input/

# Run the container
docker run -v $(pwd)/pdf-input:/app/input -v $(pwd)/pdf-output:/app/output pdf-outline-extractor

# Check results
ls ./pdf-output/
```

## Demo Mode

Run the demo to see the extractor in action with sample files:

```bash
python demo.py
```

## Output Format

Each PDF generates a JSON file with this structure:

```json
{
  "title": "Document Title (extracted from largest font on first page)",
  "outline": [
    {
      "level": "H1|H2|H3",
      "text": "Heading text",
      "page": 1
    }
  ]
}
```

## Heading Detection Logic

The system automatically detects headings based on:

1. **Font Size**: Text significantly larger than body text
2. **Formatting**: Bold or italic styling
3. **Position**: Left-aligned or properly indented text
4. **Content**: Common heading patterns and numbering
5. **Context**: Relative size compared to other headings in the document

### Hierarchy Assignment

- **H1**: Largest heading font sizes (main sections)
- **H2**: Medium heading font sizes (subsections)  
- **H3**: Smaller heading font sizes (sub-subsections)

## Performance

- ⚡ Processes 50-page PDFs in under 10 seconds
- 🎯 High accuracy on documents with clear heading structure
- 💾 Minimal memory footprint
- 🔄 Batch processing of multiple PDFs

## Troubleshooting

### No headings detected
- Ensure your PDF has clear font size differences
- Check that the document isn't image-based (scanned)
- Verify headings have distinct formatting (bold/larger fonts)

### Missing headings
- Some headings might not meet the size threshold
- Complex layouts may require manual verification
- Headers/footers might be incorrectly identified

### Incorrect hierarchy
- The system assigns levels based on relative font sizes
- Documents with inconsistent formatting may have mixed results

## Best Results With

✅ **Well-formatted documents** with clear heading hierarchy  
✅ **Academic papers** with consistent section numbering  
✅ **Technical manuals** with structured layouts  
✅ **Reports** with distinct section headers  

⚠️ **May struggle with:**  
- Scanned/image-based PDFs
- Documents with minimal font variation
- Complex multi-column layouts
- Heavily formatted decorative documents

## Advanced Usage

### Custom Configuration

You can modify the extractor parameters in `main.py`:

```python
class PDFOutlineExtractor:
    def __init__(self):
        self.min_heading_length = 3          # Minimum characters for heading
        self.max_heading_length = 200        # Maximum characters for heading
        self.heading_size_threshold = 1.1    # Font size multiplier vs body text
```

### Debug Mode

Enable debug logging to see detailed extraction information:

```python
# In main.py, change logging level
logging.basicConfig(level=logging.DEBUG)
```

This will show:
- Font size distribution in the document
- Individual heading candidates and scores
- Detection reasoning for each potential heading

## File Requirements

- **Input**: PDF files (up to 50 pages recommended)
- **Output**: JSON files with same base name
- **Format**: UTF-8 encoded JSON with proper structure
- **Size**: No specific size limits, but performance optimal under 10MB per PDF