import io
import datetime
import datetime

def generate_certificate_pdf(user_name: str, cert_type: str, school_name: str = "", student_class: str = "") -> bytes:
    buffer = io.BytesIO()
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import landscape, letter
        from reportlab.lib.colors import HexColor
    except ImportError:
        # Graceful fallback if reportlab is not installed
        buffer.write(f"CERTIFICATE OF {cert_type.upper()}\n\nPresented to {user_name}\n\n{school_name}".encode('utf-8'))
        return buffer.getvalue()
        
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    width, height = landscape(letter)
    
    # Draw Border
    c.setStrokeColor(HexColor("#003366"))
    c.setLineWidth(10)
    c.rect(20, 20, width - 40, height - 40)
    
    c.setStrokeColor(HexColor("#FFCC00"))
    c.setLineWidth(2)
    c.rect(30, 30, width - 60, height - 60)
    
    # Title
    c.setFont("Helvetica-Bold", 40)
    c.setFillColor(HexColor("#003366"))
    c.drawCentredString(width / 2, height - 150, "CERTIFICATE")
    
    c.setFont("Helvetica", 20)
    c.drawCentredString(width / 2, height - 200, "OF " + cert_type.upper())
    
    # Body
    c.setFont("Helvetica", 18)
    c.setFillColor(HexColor("#333333"))
    c.drawCentredString(width / 2, height - 280, "This is proudly presented to")
    
    c.setFont("Helvetica-Bold", 35)
    c.setFillColor(HexColor("#003366"))
    c.drawCentredString(width / 2, height - 350, user_name)
    
    if school_name or student_class:
        school_text = f"from {school_name}" if school_name else ""
        class_text = f" (Class: {student_class})" if student_class else ""
        c.setFont("Helvetica", 16)
        c.setFillColor(HexColor("#555555"))
        c.drawCentredString(width / 2, height - 380, f"{school_text}{class_text}".strip())
    
    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#333333"))
    c.drawCentredString(width / 2, height - 420, "For successfully fulfilling all requirements and demonstrating excellence.")
    
    # Date and Signature
    c.setFont("Helvetica", 12)
    today = datetime.datetime.now().strftime("%B %d, %Y")
    
    c.drawString(150, 100, today)
    c.line(120, 120, 250, 120)
    c.drawCentredString(185, 80, "Date")
    
    c.drawString(width - 250, 100, "TalentSphere Elevate")
    c.line(width - 280, 120, width - 120, 120)
    c.drawCentredString(width - 200, 80, "Authorized Signature")
    
    c.showPage()
    c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

def generate_report_pdf(title: str, content: str) -> bytes:
    """
    Generates a professional PDF report with a given title and content.
    Handles multiline content by splitting on newlines and formats different
    types of content (lists, headers, key-values).
    """
    buffer = io.BytesIO()
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.colors import HexColor
    except ImportError:
        # Graceful fallback if reportlab is not installed
        buffer.write(f"Report: {title}\n\n{content}".encode('utf-8'))
        return buffer.getvalue()

    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Theme Colors
    primary_color = HexColor("#003366")
    secondary_color = HexColor("#0f9b8e")
    text_color = HexColor("#333333")
    light_gray = HexColor("#f0f2f6")
    
    def draw_background():
        # Top banner
        c.setFillColor(primary_color)
        c.rect(0, height - 80, width, 80, fill=1, stroke=0)
        # Bottom banner
        c.setFillColor(secondary_color)
        c.rect(0, 0, width, 20, fill=1, stroke=0)
        
    def draw_header(page_num):
        draw_background()
        # Title
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(HexColor("#ffffff"))
        c.drawString(40, height - 50, title)
        
        # Logo placeholder or Project Name
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(width - 40, height - 45, "TalentSphere Elevate")
        
        # Date Generated
        today = datetime.datetime.now().strftime("%B %d, %Y, %I:%M %p")
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor("#dddddd"))
        c.drawString(40, height - 70, f"Generated on: {today}")
        
        # Footer text
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(HexColor("#ffffff"))
        c.drawString(40, 6, f"TalentSphere Elevate - Confidential Report | Page {page_num}")
        
    page_number = 1
    draw_header(page_number)
    
    # Body Content
    c.setFont("Helvetica", 12)
    c.setFillColor(text_color)
    y_position = height - 120
    line_spacing = 20
    
    lines = content.split('\n')
    for line in lines:
        if y_position < 60: # Page break logic
            c.showPage()
            page_number += 1
            draw_header(page_number)
            c.setFont("Helvetica", 12)
            c.setFillColor(text_color)
            y_position = height - 120
        
        line = line.strip()
        if not line:
            y_position -= line_spacing / 2
            continue
            
        # Basic markdown-like parsing for PDF formatting
        if line.startswith('### '):
            c.setFont("Helvetica-Bold", 16)
            c.setFillColor(primary_color)
            c.drawString(40, y_position, line[4:])
            c.setFont("Helvetica", 12)
            c.setFillColor(text_color)
            y_position -= line_spacing + 5
        elif line.startswith('**') and line.endswith('**'):
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y_position, line[2:-2])
            c.setFont("Helvetica", 12)
            y_position -= line_spacing
        elif ':' in line and len(line.split(':', 1)[0]) < 30 and not line.startswith('http'):
            # Key-value pair formatting
            key, val = line.split(':', 1)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(40, y_position, key + ":")
            c.setFont("Helvetica", 12)
            c.drawString(40 + c.stringWidth(key + ": ", "Helvetica-Bold", 12), y_position, val.strip())
            y_position -= line_spacing
        elif line.startswith('- ') or line.startswith('• '):
            c.drawString(50, y_position, "• " + line[2:])
            y_position -= line_spacing
        else:
            c.drawString(40, y_position, line)
            y_position -= line_spacing
            
    c.showPage()
    c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
