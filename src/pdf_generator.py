from fpdf import FPDF
import os
import urllib.request

FONT_URL = "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab-Regular.ttf"
FONT_PATH = "RobotoSlab-Regular.ttf"

def ensure_font():
    if not os.path.exists(FONT_PATH):
        print(f"Downloading font from {FONT_URL}...")
        try:
            urllib.request.urlretrieve(FONT_URL, FONT_PATH)
        except Exception as e:
            print(f"Failed to download font: {e}")
            return False
    return True

class TestPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.font_ready = ensure_font()
        if self.font_ready:
            self.add_font("RobotoSlab", "", FONT_PATH)

    def header(self):
        if self.font_ready:
            self.set_font('RobotoSlab', '', 20)
        else:
            self.set_font('helvetica', 'B', 20)
            
        self.cell(0, 10, 'English Knowledge Test', align='C', new_x="LMARGIN", new_y="NEXT")
        
        if self.font_ready:
            self.set_font('RobotoSlab', '', 12)
        else:
            self.set_font('helvetica', 'I', 12)
            
        self.cell(0, 10, 'Total Score: 100', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        if self.font_ready:
            self.set_font('RobotoSlab', '', 8)
            try:
                self.cell(0, 10, 'Copyright © Phạm Quang Hương', align='C')
            except Exception: # Catch any font encoding issues
                self.set_font('helvetica', 'I', 8)
                self.cell(0, 10, 'Copyright (c) Pham Quang Huong', align='C')
        else:
            # Fallback if download failed
            self.set_font('helvetica', 'I', 8)
            self.cell(0, 10, 'Copyright (c) Pham Quang Huong', align='C')

def create_pdf(questions, filename="test.pdf"):
    pdf = TestPDF()
    pdf.add_page()
    
    if pdf.font_ready:
        pdf.set_font("RobotoSlab", size=12)
    else:
        pdf.set_font("helvetica", size=12)
    
    for i, q in enumerate(questions, 1):
        # Format question text
        question_text = f"Q{i}. {q['question']} ({q['points']} pts)"
        
        # Check if page break is needed loosely
        if pdf.get_y() > 250:
            pdf.add_page()
            
        # Handle unicode in body text too
        try:
            pdf.multi_cell(0, 10, question_text)
        except Exception:
             # Fallback for body text
             pdf.set_font("helvetica", size=12)
             safe_text = question_text.encode('latin-1', 'replace').decode('latin-1')
             pdf.multi_cell(0, 10, safe_text)
             # Restore font if ready
             if pdf.font_ready: pdf.set_font("RobotoSlab", size=12)
        
        if "options" in q:
            # Multiple Choice
            for opt in q["options"]:
                pdf.cell(10, 8, "") # Indent
                try:
                    pdf.cell(0, 8, f"- {opt}", new_x="LMARGIN", new_y="NEXT")
                except Exception:
                    pdf.set_font("helvetica", size=12)
                    safe_opt = f"- {opt}".encode('latin-1', 'replace').decode('latin-1')
                    pdf.cell(0, 8, safe_opt, new_x="LMARGIN", new_y="NEXT")
                    if pdf.font_ready: pdf.set_font("RobotoSlab", size=12)
            pdf.ln(2)
        else:
            # Essay - give some space
            pdf.ln(30)
            
    pdf.output(filename)
    return filename
