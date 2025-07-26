#!/usr/bin/env python3
"""
Demo script to showcase the PDF Outline Extractor functionality.
"""

import os
import json
from main import PDFOutlineExtractor

def run_demo():
    """Run a demo of the PDF outline extraction."""
    print("🔍 PDF Outline Extractor Demo")
    print("=" * 40)
    
    # Check if there are any PDFs to process
    input_dir = "/app/input"
    output_dir = "/app/output"
    
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found in /app/input")
        print("   Please add some PDF files to test the extraction.")
        return
    
    print(f"📁 Found {len(pdf_files)} PDF file(s) to process:")
    for pdf_file in pdf_files:
        print(f"   • {pdf_file}")
    
    print("\n🚀 Running extraction...")
    
    extractor = PDFOutlineExtractor()
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        output_file = pdf_file.replace('.pdf', '.json').replace('.PDF', '.json')
        output_path = os.path.join(output_dir, output_file)
        
        print(f"\n📄 Processing: {pdf_file}")
        
        try:
            result = extractor.extract_outline(pdf_path)
            
            # Save result
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            # Display results
            print(f"✅ Title: {result['title']}")
            print(f"📋 Outline ({len(result['outline'])} headings):")
            
            for i, heading in enumerate(result['outline'], 1):
                indent = "  " * (int(heading['level'][1]) - 1)  # H1=0, H2=1, H3=2 spaces
                print(f"   {i:2}. {indent}{heading['level']}: {heading['text']} (Page {heading['page']})")
            
            print(f"💾 Saved to: {output_path}")
            
        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {e}")
    
    print(f"\n🎉 Demo completed!")
    print(f"📂 Check the {output_dir} directory for JSON output files.")

if __name__ == "__main__":
    run_demo()