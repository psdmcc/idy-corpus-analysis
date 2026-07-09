import os
import re

def transform_idy_manuscript(filename="Literature_Review_Methodology.md"):
    """
    Standardizes the IDY manuscript to US English while stripping out 
    the specific text corruption bugs, layout artifacts, and typos found in the text.
    Targeted for execution within the papers/arxiv/ directory.
    """
    if not os.path.exists(filename):
        print(f"Error: Target IDY document file missing at: {os.path.abspath(filename)}")
        print("Please verify the filename parameter matches your target file exactly.")
        return

    print(f"Reading target IDY manuscript lines from: {filename}...")
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Define comprehensive translation pairs for your specific IDY document data
    localizations = {
        # 1. Clean the specific text corruption bugs and compile artifacts from the PDF
        r"environmental敲al": "environmental",
        r"heteroge杌eous": "heterogeneous",
        r"Ac杁ording": "According",
        r"stan杁ardized": "standardized",
        r"for杔alized": "formalized",
        
        # 2. Fix the specific literal typos and spacing rules found in the document
        r"change\.However": "change. However",
        r"it’s apparent lifestyle": "its apparent lifestyle",
        r"\bstrenght\b": "strength",
        r"\bidentify formation\b": "identity formation",
        r"\bhat\.hayoga\b": "hatha yoga",
        r"\bdefracted\b": "diffracted",
        
        # 3. British/Commonwealth to US spelling transformation loops (-our -> -or)
        r"(\b\w+)haviour(\b|\w+)": r"\1havior\2",
        r"(\b\w+)colour(\b|\w+)": r"\1color\2",
        r"(\b\w+)favour(\b|\w+)": r"\1favor\2",
        r"(\b\w+)labour(\b|\w+)": r"\1labor\2",
        r"(\b\w+)honour(\b|\w+)": r"\1honor\2",
        r"(\b\w+)rumour(\b|\w+)": r"\1rumor\2",
        r"(\b\w+)neighbour(\b|\w+)": r"\1neighbor\2",
        
        # 4. Suffix conversions (-ise -> -ize / -isation -> -ization)
        r"(\b\w+)organis(\b|\w+)": r"\1organiz\2",
        r"(\b\w+)standardis(\b|\w+)": r"\1standardiz\2",
        r"(\b\w+)synchronis(\b|\w+)": r"\1synchroniz\2",
        r"(\b\w+)characteris(\b|\w+)": r"\1characteriz\2",
        r"(\b\w+)prioritis(\b|\w+)": r"\1prioritiz\2",
        r"(\b\w+)conceptualis(\b|\w+)": r"\1conceptualiz\2",
        r"(\b\w+)contextualis(\b|\w+)": r"\1contextualiz\2",
        r"(\b\w+)specialis(\b|\w+)": r"\1specializ\2",
        r"(\b\w+)stabilis(\b|\w+)": r"\1stabiliz\2",
        r"(\b\w+)normalis(\b|\w+)": r"\1normaliz\2",
        r"(\b\w+)centralis(\b|\w+)": r"\1centraliz\2",
        
        # 5. Program and Centre adjustments (-mme -> -m / -re -> -er)
        r"(\b\w+)programme(\b|\w+)": r"\1program\2",
        r"(\b)centre(\b|\w+)": r"\1center\2",
        r"(\b)theatre(\b|\w+)": r"\1theater\2"
    }

    print("Executing linguistic transformation loop across IDY text assets...")
    transformed_content = content
    for pattern, replacement in localizations.items():
        transformed_content = re.sub(pattern, replacement, transformed_content)

    # Export to a clean, separate file destination prefixed for tracking
    output_filename = "US_ENGLISH_" + filename
    
    # CRITICAL ENHANCEMENT: Added errors="replace" to seamlessly write past broken characters
    with open(output_filename, "w", encoding="utf-8", errors="replace") as f:
        f.write(transformed_content)
        
    print(f"\nLinguistic standardization mapping sequence complete!")
    print(f"US English localized IDY file generated successfully at: {output_filename}")

if __name__ == "__main__":
    transform_idy_manuscript(filename="Literature_Review_Methodology.md")
