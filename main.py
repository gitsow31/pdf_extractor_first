#!/usr/bin/env python3
"""
PDF Outline Extractor

Extracts hierarchical outlines from PDF files based on font properties.
Processes all PDFs from /app/input and outputs JSON files to /app/output.
"""

import os
import json
import sys
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from collections import Counter
import fitz  # PyMuPDF
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TextBlock:
    """Represents a text block with its properties."""
    text: str
    font_size: float
    font_name: str
    font_flags: int  # Bold, italic flags
    page_number: int
    bbox: Tuple[float, float, float, float]  # x0, y0, x1, y1
    x_position: float
    y_position: float

@dataclass 
class HeadingCandidate:
    """Represents a potential heading."""
    text: str
    level: str
    page: int
    font_size: float
    score: float

class PDFOutlineExtractor:
    """Extract hierarchical outline from PDF based on font properties."""
    
    def __init__(self):
        self.min_heading_length = 3
        self.max_heading_length = 200
        self.heading_size_threshold = 1.1  # Font size must be at least 10% larger than body text
        
    def extract_text_blocks(self, pdf_path: str) -> List[TextBlock]:
        """Extract all text blocks with their properties from PDF."""
        text_blocks = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                blocks = page.get_text("dict")
                
                for block in blocks.get("blocks", []):
                    if "lines" not in block:
                        continue
                        
                    for line in block["lines"]:
                        for span in line.get("spans", []):
                            text = span.get("text", "").strip()
                            if not text:
                                continue
                                
                            # Extract font properties
                            font_size = span.get("size", 0)
                            font_name = span.get("font", "")
                            font_flags = span.get("flags", 0)
                            bbox = span.get("bbox", (0, 0, 0, 0))
                            
                            text_block = TextBlock(
                                text=text,
                                font_size=font_size,
                                font_name=font_name,
                                font_flags=font_flags,
                                page_number=page_num + 1,
                                bbox=bbox,
                                x_position=bbox[0],
                                y_position=bbox[1]
                            )
                            text_blocks.append(text_block)
            
            doc.close()
            
        except Exception as e:
            logger.error(f"Error extracting text blocks from {pdf_path}: {e}")
            return []
            
        return text_blocks
    
    def is_bold(self, font_flags: int) -> bool:
        """Check if font is bold."""
        return bool(font_flags & 2**4)  # Bold flag
    
    def is_italic(self, font_flags: int) -> bool:
        """Check if font is italic."""
        return bool(font_flags & 2**1)  # Italic flag
    
    def find_body_text_size(self, text_blocks: List[TextBlock]) -> float:
        """Find the most common font size (assumed to be body text)."""
        if not text_blocks:
            return 12.0
            
        font_sizes = [block.font_size for block in text_blocks if block.font_size > 0]
        if not font_sizes:
            return 12.0
            
        # Find most common font size
        size_counter = Counter(font_sizes)
        return size_counter.most_common(1)[0][0]
    
    def extract_document_title(self, text_blocks: List[TextBlock]) -> str:
        """Extract document title from the largest font text on first page."""
        if not text_blocks:
            return "Untitled Document"
        
        # Filter first page blocks
        first_page_blocks = [block for block in text_blocks if block.page_number == 1]
        if not first_page_blocks:
            return "Untitled Document"
        
        # Find blocks with largest font size
        max_font_size = max(block.font_size for block in first_page_blocks)
        title_candidates = [
            block for block in first_page_blocks 
            if block.font_size == max_font_size and len(block.text.strip()) > 5
        ]
        
        if title_candidates:
            # Choose the first substantial title candidate
            for candidate in title_candidates:
                # Skip if it looks like a header/footer based on position
                page_height = 800  # Approximate page height
                if candidate.y_position > page_height * 0.1 and candidate.y_position < page_height * 0.9:
                    return candidate.text.strip()
            
            # Fallback to first candidate
            return title_candidates[0].text.strip()
        
        return "Untitled Document"
    
    def detect_headings(self, text_blocks: List[TextBlock]) -> List[HeadingCandidate]:
        """Detect headings based on font properties and position."""
        if not text_blocks:
            return []
        
        body_text_size = self.find_body_text_size(text_blocks)
        min_heading_size = body_text_size * self.heading_size_threshold
        
        heading_candidates = []
        
        # Get document title first to exclude it from headings
        title_text = self.extract_document_title(text_blocks).strip()
        
        for block in text_blocks:
            text = block.text.strip()
            
            # Skip if text is too short or too long
            if len(text) < self.min_heading_length or len(text) > self.max_heading_length:
                continue
            
            # Skip if this is the document title
            if text == title_text:
                continue
            
            # Skip if font size is not significantly larger than body text
            if block.font_size < min_heading_size:
                continue
            
            # Calculate heading score based on various factors
            score = self.calculate_heading_score(block, body_text_size)
            
            if score > 0.3:  # Lower threshold for better detection
                level = self.determine_heading_level(block, body_text_size, text_blocks)
                
                heading_candidate = HeadingCandidate(
                    text=text,
                    level=level,
                    page=block.page_number,
                    font_size=block.font_size,
                    score=score
                )
                heading_candidates.append(heading_candidate)
        
        return self.refine_headings(heading_candidates)
    
    def calculate_heading_score(self, block: TextBlock, body_text_size: float) -> float:
        """Calculate a score indicating how likely this text is to be a heading."""
        score = 0.0
        
        # Font size factor (larger = more likely to be heading)
        size_ratio = block.font_size / body_text_size
        score += min(size_ratio - 1.0, 1.0) * 0.4
        
        # Bold font bonus
        if self.is_bold(block.font_flags):
            score += 0.3
        
        # Position factor (left-aligned or indented text more likely to be heading)
        if block.x_position < 100:  # Left margin
            score += 0.2
        
        # Length factor (moderate length text more likely to be heading)
        text_length = len(block.text.strip())
        if 10 <= text_length <= 80:
            score += 0.1
        
        # Special patterns that suggest headings (numbers, sections)
        text = block.text.strip()
        if any(pattern in text.lower() for pattern in ['introduction', 'conclusion', 'methodology', 'results', 'background']):
            score += 0.2
        
        # Numbered sections
        import re
        if re.match(r'^\d+\.', text) or re.match(r'^\d+\.\d+', text):
            score += 0.2
        
        return min(score, 1.0)
    
    def determine_heading_level(self, block: TextBlock, body_text_size: float, 
                               all_blocks: List[TextBlock]) -> str:
        """Determine the heading level (H1, H2, H3) based on font size and context."""
        
        # Get all font sizes larger than body text, excluding title
        title_text = self.extract_document_title(all_blocks).strip()
        
        heading_sizes = []
        for b in all_blocks:
            if (b.font_size > body_text_size * self.heading_size_threshold and 
                b.text.strip() != title_text and
                len(b.text.strip()) >= self.min_heading_length):
                heading_sizes.append(b.font_size)
        
        # Remove duplicates and sort in descending order
        heading_sizes = sorted(set(heading_sizes), reverse=True)
        
        if not heading_sizes:
            return "H1"
        
        # Assign levels based on font size ranking
        if len(heading_sizes) == 1:
            return "H1"
        elif len(heading_sizes) == 2:
            return "H1" if block.font_size == heading_sizes[0] else "H2"
        else:
            if block.font_size == heading_sizes[0]:
                return "H1"
            elif block.font_size == heading_sizes[1]:
                return "H2"
            else:
                return "H3"
    
    def refine_headings(self, candidates: List[HeadingCandidate]) -> List[HeadingCandidate]:
        """Refine heading candidates by removing duplicates and false positives."""
        if not candidates:
            return []
        
        # Sort by page and position
        candidates.sort(key=lambda x: (x.page, x.font_size), reverse=True)
        
        # Remove near-duplicates (same text on same page)
        refined = []
        seen_texts = set()
        
        for candidate in candidates:
            text_key = (candidate.text.lower(), candidate.page)
            if text_key not in seen_texts:
                refined.append(candidate)
                seen_texts.add(text_key)
        
        # Sort by page and logical order
        refined.sort(key=lambda x: x.page)
        
        return refined
    
    def extract_outline(self, pdf_path: str) -> Dict[str, Any]:
        """Extract hierarchical outline from PDF."""
        logger.info(f"Processing: {pdf_path}")
        
        # Extract text blocks
        text_blocks = self.extract_text_blocks(pdf_path)
        if not text_blocks:
            logger.warning(f"No text blocks found in {pdf_path}")
            return {
                "title": "Untitled Document",
                "outline": []
            }
        
        # Extract title
        title = self.extract_document_title(text_blocks)
        
        # Detect headings
        headings = self.detect_headings(text_blocks)
        
        # Convert to output format
        outline = []
        for heading in headings:
            outline.append({
                "level": heading.level,
                "text": heading.text,
                "page": heading.page
            })
        
        result = {
            "title": title,
            "outline": outline
        }
        
        logger.info(f"Extracted {len(outline)} headings from {pdf_path}")
        return result

def process_pdf_files():
    """Process all PDF files from input directory and save results to output directory."""
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    # Create directories if they don't exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    extractor = PDFOutlineExtractor()
    
    # Find all PDF files
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        logger.warning(f"No PDF files found in {input_dir}")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    for pdf_file in pdf_files:
        try:
            pdf_path = os.path.join(input_dir, pdf_file)
            
            # Extract outline
            result = extractor.extract_outline(pdf_path)
            
            # Save result
            output_file = pdf_file.replace('.pdf', '.json').replace('.PDF', '.json')
            output_path = os.path.join(output_dir, output_file)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved outline to {output_path}")
            
        except Exception as e:
            logger.error(f"Error processing {pdf_file}: {e}")

if __name__ == "__main__":
    try:
        process_pdf_files()
        logger.info("PDF outline extraction completed successfully")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)