import os
from pathlib import Path
try:
    from pypdf import PdfReader
except ImportError:
    print("Error: 'pypdf' library not found. Please run 'pip install pypdf' first.")
    exit(1)

TARGET_DIR = Path("data/corpus_expansion")

def convert_pdfs_to_text():
    print("Initiating raw text extraction engine...")
    pdf_files = list(TARGET_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in data/corpus_expansion/")
        return
        
    for pdf_path in pdf_files:
        txt_path = pdf_path.with_suffix(".txt")
        print(f"Extracting text from: {pdf_path.name}...")
        
        try:
            reader = PdfReader(pdf_path)
            extracted_text = ""
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_text += f"\n--- Page {page_num+1} ---\n" + text
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)
                
            print(f"Successfully saved text variant: {txt_path.name}")
            
        except Exception as e:
            print(f"Failed to extract text from {pdf_path.name}: {e}")

if __name__ == "__main__":
    convert_pdfs_to_text()
