#!/usr/bin/env python3
"""
Create a sample PDF for testing the outline extractor.
"""

import fitz  # PyMuPDF
import os

def create_test_pdf():
    """Create a sample PDF with headings of different levels."""
    doc = fitz.open()  # Create new PDF
    
    # Page 1 - Title and Introduction
    page1 = doc.new_page()
    
    # Title (largest font)
    title_text = "Sample Document for Testing"
    title_point = fitz.Point(50, 100)
    page1.insert_text(title_point, title_text, fontsize=24, color=(0, 0, 0))
    
    # H1 heading
    h1_point = fitz.Point(50, 180)
    page1.insert_text(h1_point, "1. Introduction", fontsize=18, color=(0, 0, 0))
    
    # Body text
    body_point = fitz.Point(50, 220)
    body_text = "This is a sample document created to test the PDF outline extractor. The document contains various heading levels to demonstrate the extraction capabilities."
    page1.insert_text(body_point, body_text, fontsize=12, color=(0, 0, 0))
    
    # H2 heading
    h2_point = fitz.Point(50, 280)
    page1.insert_text(h2_point, "1.1 Background", fontsize=15, color=(0, 0, 0))
    
    # More body text
    body2_point = fitz.Point(50, 320)
    body2_text = "This section provides background information about the document structure and purpose."
    page1.insert_text(body2_point, body2_text, fontsize=12, color=(0, 0, 0))
    
    # Page 2 - More content
    page2 = doc.new_page()
    
    # H1 heading
    h1_p2_point = fitz.Point(50, 100)
    page2.insert_text(h1_p2_point, "2. Methodology", fontsize=18, fontname="helv-bold")
    
    # Body text
    body_p2_point = fitz.Point(50, 140)
    body_p2_text = "This section describes the methodology used in the analysis."
    page2.insert_text(body_p2_point, body_p2_text, fontsize=12, fontname="helv")
    
    # H2 heading
    h2_p2_point = fitz.Point(50, 200)
    page2.insert_text(h2_p2_point, "2.1 Data Collection", fontsize=15, fontname="helv-bold")
    
    # H3 heading
    h3_p2_point = fitz.Point(70, 240)
    page2.insert_text(h3_p2_point, "2.1.1 Survey Design", fontsize=13, fontname="helv-bold")
    
    # Body text
    body3_p2_point = fitz.Point(70, 280)
    body3_p2_text = "The survey was designed to collect comprehensive data about user preferences."
    page2.insert_text(body3_p2_point, body3_p2_text, fontsize=12, fontname="helv")
    
    # Page 3 - Results
    page3 = doc.new_page()
    
    # H1 heading
    h1_p3_point = fitz.Point(50, 100)
    page3.insert_text(h1_p3_point, "3. Results", fontsize=18, fontname="helv-bold")
    
    # H2 heading
    h2_p3_point = fitz.Point(50, 160)
    page3.insert_text(h2_p3_point, "3.1 Statistical Analysis", fontsize=15, fontname="helv-bold")
    
    # H3 heading
    h3_p3_point = fitz.Point(70, 200)
    page3.insert_text(h3_p3_point, "3.1.1 Descriptive Statistics", fontsize=13, fontname="helv-bold")
    
    # Body text
    body_p3_point = fitz.Point(70, 240)
    body_p3_text = "The descriptive statistics show interesting patterns in the data."
    page3.insert_text(body_p3_point, body_p3_text, fontsize=12, fontname="helv")
    
    # H1 heading
    h1_conclusion_point = fitz.Point(50, 320)
    page3.insert_text(h1_conclusion_point, "4. Conclusion", fontsize=18, fontname="helv-bold")
    
    # Save the PDF
    output_path = "/app/input/test_document.pdf"
    doc.save(output_path)
    doc.close()
    
    print(f"Test PDF created: {output_path}")

if __name__ == "__main__":
    create_test_pdf()