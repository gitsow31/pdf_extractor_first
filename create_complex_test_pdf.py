#!/usr/bin/env python3
"""
Create a more complex test PDF with varied heading structures.
"""

import fitz  # PyMuPDF
import os

def create_complex_test_pdf():
    """Create a complex PDF with various heading patterns."""
    doc = fitz.open()  # Create new PDF
    
    # Page 1 - Title page with complex structure
    page1 = doc.new_page()
    
    # Large title
    title_text = "Advanced Machine Learning Techniques: A Comprehensive Analysis"
    title_point = fitz.Point(50, 80)
    page1.insert_text(title_point, title_text, fontsize=22, color=(0, 0, 0))
    
    # Subtitle
    subtitle_text = "Research Report 2025"
    subtitle_point = fitz.Point(50, 120)
    page1.insert_text(subtitle_point, subtitle_text, fontsize=16, color=(0, 0, 0))
    
    # Abstract (should be detected as heading)
    abstract_title = "Abstract"
    abstract_point = fitz.Point(50, 200)
    page1.insert_text(abstract_point, abstract_title, fontsize=18, color=(0, 0, 0))
    
    # Abstract body
    abstract_body = "This research investigates the effectiveness of advanced machine learning techniques in various domains. We analyze performance metrics and provide comprehensive evaluation results."
    abstract_body_point = fitz.Point(50, 240)
    page1.insert_text(abstract_body_point, abstract_body, fontsize=12, color=(0, 0, 0))
    
    # Table of Contents (should be detected)
    toc_title = "Table of Contents"
    toc_point = fitz.Point(50, 320)
    page1.insert_text(toc_point, toc_title, fontsize=18, color=(0, 0, 0))
    
    # Page 2 - Introduction with subsections
    page2 = doc.new_page()
    
    # Chapter 1
    ch1_title = "Chapter 1: Introduction"
    ch1_point = fitz.Point(50, 80)
    page2.insert_text(ch1_point, ch1_title, fontsize=20, color=(0, 0, 0))
    
    # Section 1.1
    sec11_title = "1.1 Problem Statement"
    sec11_point = fitz.Point(50, 150)
    page2.insert_text(sec11_point, sec11_title, fontsize=16, color=(0, 0, 0))
    
    # Body text
    body1 = "Machine learning has become increasingly important in modern data analysis."
    body1_point = fitz.Point(50, 190)
    page2.insert_text(body1_point, body1, fontsize=12, color=(0, 0, 0))
    
    # Subsection 1.1.1
    subsec111_title = "1.1.1 Background Research"
    subsec111_point = fitz.Point(70, 230)
    page2.insert_text(subsec111_point, subsec111_title, fontsize=14, color=(0, 0, 0))
    
    # Section 1.2
    sec12_title = "1.2 Research Objectives"
    sec12_point = fitz.Point(50, 300)
    page2.insert_text(sec12_point, sec12_title, fontsize=16, color=(0, 0, 0))
    
    # Page 3 - Methodology
    page3 = doc.new_page()
    
    # Chapter 2
    ch2_title = "Chapter 2: Methodology"
    ch2_point = fitz.Point(50, 80)
    page3.insert_text(ch2_point, ch2_title, fontsize=20, color=(0, 0, 0))
    
    # Section 2.1
    sec21_title = "2.1 Data Collection Methods"
    sec21_point = fitz.Point(50, 140)
    page3.insert_text(sec21_point, sec21_title, fontsize=16, color=(0, 0, 0))
    
    # Subsection with different numbering
    subsec_alt = "Survey Design and Implementation"
    subsec_alt_point = fitz.Point(70, 180)
    page3.insert_text(subsec_alt_point, subsec_alt, fontsize=14, color=(0, 0, 0))
    
    # Section 2.2
    sec22_title = "2.2 Experimental Setup"
    sec22_point = fitz.Point(50, 240)
    page3.insert_text(sec22_point, sec22_title, fontsize=16, color=(0, 0, 0))
    
    # Results section
    results_title = "Results and Analysis"
    results_point = fitz.Point(50, 320)
    page3.insert_text(results_point, results_title, fontsize=18, color=(0, 0, 0))
    
    # Page 4 - Conclusions
    page4 = doc.new_page()
    
    # Conclusion chapter
    conclusion_title = "Conclusions"
    conclusion_point = fitz.Point(50, 80)
    page4.insert_text(conclusion_point, conclusion_title, fontsize=20, color=(0, 0, 0))
    
    # Final remarks
    final_title = "Future Work"
    final_point = fitz.Point(50, 160)
    page4.insert_text(final_point, final_title, fontsize=18, color=(0, 0, 0))
    
    # References
    references_title = "References"
    references_point = fitz.Point(50, 240)
    page4.insert_text(references_point, references_title, fontsize=18, color=(0, 0, 0))
    
    # Save the PDF
    output_path = "/app/input/complex_document.pdf"
    doc.save(output_path)
    doc.close()
    
    print(f"Complex test PDF created: {output_path}")

if __name__ == "__main__":
    create_complex_test_pdf()