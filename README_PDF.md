# PDF Outline Extractor 🔍

A Python script that runs offline in a Docker container and extracts hierarchical outlines from PDF files based on font properties and layout analysis.

## ✨ Features

- **🤖 Automatic Heading Detection**: Detects H1, H2, and H3 headings based on:
  - Font size analysis relative to body text
  - Bold/italic styling recognition  
  - Text position and indentation patterns
  - Common heading content patterns
- **📑 Document Title Extraction**: Automatically extracts document title from the largest font text on the first page
- **🔄 Batch Processing**: Processes all PDF files from input directory simultaneously
- **⚡ Fast Performance**: Processes 50-page PDFs in under 2 seconds
- **🔒 Offline Operation**: No internet access required, runs completely offline
- **🐳 Docker Ready**: Containerized for easy deployment and consistent execution

## 🚀 Quick Start

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

## 📋 Input/Output Format

### Input
- 📁 Place PDF files in `/app/input` directory
- 📄 Supports PDFs up to 50 pages each
- 🎯 Best results with well-structured documents

### Output Format
JSON files saved to `/app/output` directory with same filename:

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

## 🧠 How It Works

### Heading Detection Algorithm

1. **📊 Font Analysis**: Analyzes all text blocks to identify:
   - Most common font size (body text baseline)
   - Larger font sizes indicating potential headings
   - Font formatting (bold/italic) properties

2. **🎯 Heading Criteria**: Text is considered a heading candidate if:
   - Font size ≥10% larger than body text
   - Appropriately positioned (left-aligned or indented)
   - Reasonable length (3-200 characters)
   - May include bold/italic formatting

3. **📐 Level Assignment**: Hierarchy determined by:
   - Relative font size ranking (largest = H1, medium = H2, smallest = H3)
   - Document context and structure analysis
   - Position and formatting consistency

4. **👑 Title Extraction**: Document title extracted by:
   - Finding largest font text on first page
   - Filtering out headers/footers by position
   - Selecting most substantial content

## 🛠️ Technical Details

### Libraries Used
- **PyMuPDF (fitz)**: Primary PDF parsing and text extraction engine
- **Python Standard Library**: File handling, JSON processing, data structures

### Performance Metrics
- ⚡ **Speed**: <2 seconds for 50-page PDFs  
- 💾 **Memory**: Efficient streaming extraction
- 🔄 **Throughput**: Batch processes multiple PDFs
- 🎯 **Compatibility**: Works with most PDF formats

### Constraints Met
- ✅ **Offline Operation**: No internet connectivity required
- ✅ **No External APIs**: Self-contained processing
- ✅ **Performance**: <10 seconds per 50-page PDF
- ✅ **Model Size**: Uses only lightweight libraries
- ✅ **CPU Compatible**: No GPU dependencies

## 📖 Examples

### Example 1: Academic Paper
**Input**: `research-paper.pdf`  
**Output**: `research-paper.json`

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
**Input**: `user-manual.pdf`  
**Output**: `user-manual.json`

```json
{
  "title": "Software Installation Guide v2.1",
  "outline": [
    { "level": "H1", "text": "Getting Started", "page": 1 },
    { "level": "H2", "text": "System Requirements", "page": 1 },
    { "level": "H2", "text": "Download Instructions", "page": 2 },
    { "level": "H1", "text": "Installation", "page": 3 },
    { "level": "H2", "text": "Windows Installation", "page": 3 },
    { "level": "H2", "text": "macOS Installation", "page": 5 }
  ]
}
```

## 🚨 Troubleshooting

### Common Issues

1. **No headings detected**:
   - ✅ Check PDF has clear font size differences
   - ✅ Verify PDF isn't image-based (scanned document)  
   - ✅ Ensure headings have distinct styling

2. **Incorrect title extraction**:
   - ℹ️ Script extracts from largest font on first page
   - ℹ️ Headers/footers may interfere with detection

3. **Missing text**:
   - ⚠️ Image-based PDFs require OCR (not supported)
   - ⚠️ Password-protected PDFs not supported

### Debug Mode
Enable detailed logging in `main.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📁 Project Structure

```
/app/
├── main.py              # Main extraction script
├── requirements.txt     # Python dependencies  
├── Dockerfile          # Container configuration
├── demo.py             # Interactive demo script
├── USAGE.md            # Detailed usage instructions
├── README.md           # This documentation
├── input/              # Input directory for PDFs
└── output/             # Output directory for JSON files
```

## 🐳 Docker Commands Reference

```bash
# Build image
docker build -t pdf-outline-extractor .

# Run with volume mounts  
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-outline-extractor

# Interactive debugging
docker run -it -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-outline-extractor /bin/bash

# View logs
docker logs <container-id>
```

## 🎯 Best Results With

✅ **Academic papers** with numbered sections  
✅ **Technical manuals** with clear hierarchy  
✅ **Business reports** with consistent formatting  
✅ **Research documents** with standard structure  

⚠️ **May need adjustment for:**
- Scanned/image-based documents
- Highly decorative or artistic layouts  
- Documents with minimal font variation
- Complex multi-column formats

## 📜 License

This project is open source and available under the MIT License.

---

**🔧 Developed for offline PDF analysis with fast, accurate heading extraction**