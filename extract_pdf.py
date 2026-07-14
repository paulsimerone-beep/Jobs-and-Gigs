from PyPDF2 import PdfReader
import os

pdf_path = r"C:\Users\TK\OneDrive\Desktop\Job listing 001.pdf"

try:
    pdf = PdfReader(pdf_path)
    print(f"Total pages: {len(pdf.pages)}\n")
    
    all_text = []
    
    for page_num, page in enumerate(pdf.pages):
        print(f"--- Page {page_num + 1} ---")
        text = page.extract_text()
        print(text)
        print("\n" + "="*80 + "\n")
        all_text.append(text)
    
    # Save extracted text to file
    with open("extracted_content.txt", "w", encoding="utf-8") as f:
        for i, text in enumerate(all_text):
            f.write(f"PAGE {i + 1}:\n")
            f.write(text)
            f.write("\n\n" + "="*80 + "\n\n")
    
    print("Text extraction complete! Saved to extracted_content.txt")
    
except Exception as e:
    print(f"Error: {e}")
