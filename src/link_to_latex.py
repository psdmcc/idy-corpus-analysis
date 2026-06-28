import os
import shutil

def link_project_to_latex():
    # =========================================================================
    # DYNAMIC AUTO-PATH DETECTION (No manual path entry required)
    # =========================================================================
    # Automatically tracks exactly where your terminal prompt is currently sitting
    current_terminal_dir = os.getcwd() 
    
    # Define your actual paper manuscript target file name
    tex_filename = "main.tex" 
    # =========================================================================

    print(f"Initializing Smart Image Linker & Injector...")
    print(f"-> Detected active path: '{current_terminal_dir}'")

    images = [
        'idy_separated_raw_trends_600dpi.png',
        'idy_social_vs_physical_600dpi.png',
        'idy_bot_forensics_dashboard_600dpi.png'
    ]

    # Look for the images in the current folder, or check one step backward in the parent directory
    parent_dir = os.path.dirname(current_terminal_dir)
    
    print("\n--- Task 1: Moving images to LaTeX folder directory ---")
    for img in images:
        source_path = None
        
        # Check current folder
        if os.path.exists(os.path.join(current_terminal_dir, img)):
            source_path = os.path.join(current_terminal_dir, img)
        # Check parent folder if not found locally
        elif os.path.exists(os.path.join(parent_dir, img)):
            source_path = os.path.join(parent_dir, img)

        if source_path:
            dest_path = os.path.join(current_terminal_dir, img)
            # If the source and destination are the same file, skip copying to avoid errors
            if source_path != dest_path:
                shutil.copy2(source_path, dest_path)
                print(f"✅ Successfully linked: {img} -> {current_terminal_dir}")
            else:
                print(f"⏭️ Asset present: '{img}' is already located in this folder.")
        else:
            print(f"⚠️ Warning: '{img}' not found in current or parent folder. Re-run your plot scripts first.")

    # Task 2: Append the LaTeX figure code blocks safely to the file
    tex_file_path = os.path.join(current_terminal_dir, tex_filename)
    print(f"\n--- Task 2: Appending LaTeX blocks to '{tex_filename}' ---")
    
    if not os.path.exists(tex_file_path):
        print(f"⚠️ Warning: '{tex_filename}' not found in '{current_terminal_dir}'.")
        print("Please check your file names or run this script from inside your actual writing folder.")
        return

    # Raw LaTeX string code blocks to inject right before document closing tags
    latex_code_to_inject = """

% =========================================================================
% AUTOMATED INJECTION: IDY CHANNELS DATA DASHBOARDS
% =========================================================================

\\begin{figure}[H]
    \\centering
    \\includegraphics[width=\\textwidth]{idy_separated_raw_trends_600dpi.png}
    \\caption{Absolute Attendance Comparison: International vs. Domestic IDY Venues (2015--2026). Layout by @psdmccartney, CC BY 4.0.}
    \\label{fig:idy_attendance}
\end{figure}

\\begin{figure}[H]
    \\centering
    \\includegraphics[width=\\textwidth]{idy_social_vs_physical_600dpi.png}
    \\caption{Trajectories of IDY Expansion: Twitter Engagement vs. Physical Turnouts (2015--2026). Layout by @psdmccartney, CC BY 4.0.}
    \\label{fig:idy_social_vs_physical}
\end{figure}

\\begin{figure}[H]
    \\centering
    \\includegraphics[width=\\textwidth]{idy_bot_forensics_dashboard_600dpi.png}
    \\caption{Twitter/X Bot Anomaly Tracking Dashboard (2015--2026). Data and template compiled by @psdmccartney, CC BY 4.0.}
    \\label{fig:idy_bot_forensics}
\end{figure}

% =========================================================================
"""

    try:
        with open(tex_file_path, 'r') as file:
            content = file.read()

        if "idy_separated_raw_trends_600dpi.png" in content:
            print("⏭️ Text skipped: Figure code blocks already exist inside your main.tex file.")
        else:
            if "\\end{document}" in content:
                content = content.replace("\\end{document}", latex_code_to_inject + "\n\\end{document}")
                with open(tex_file_path, 'w') as file:
                    file.write(content)
            else:
                with open(tex_file_path, 'a') as file:
                    file.write(latex_code_to_inject)
            print(f"🎉 Success: All 3 figure blocks have been written into '{tex_file_path}'!")
            
    except Exception as e:
        print(f"❌ Error while editing text file: {e}")

if __name__ == "__main__":
    link_project_to_latex()
