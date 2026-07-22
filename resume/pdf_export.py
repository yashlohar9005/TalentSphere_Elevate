"""
PDF Export Module using ReportLab.
"""
from io import BytesIO
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError:
    pass

from resume.templates import draw_modern_template, draw_professional_template, draw_minimal_template

def generate_pdf(resume_data: dict, template_choice: str) -> bytes:
    """Generates a PDF resume and returns it as bytes."""
    buffer = BytesIO()
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
    except ImportError:
        raise ImportError("ReportLab is not installed. Run 'pip install reportlab'")
        
    c = canvas.Canvas(buffer, pagesize=letter)
    
    if template_choice == "Modern":
        draw_modern_template(c, resume_data)
    elif template_choice == "Professional":
        draw_professional_template(c, resume_data)
    else:
        draw_minimal_template(c, resume_data)
        
    c.showPage()
    c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
