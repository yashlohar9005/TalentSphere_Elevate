"""
Templates for PDF Resume Export.
"""

def draw_modern_template(c, data):
    _draw_header(c, data, font_color=(0.1, 0.3, 0.6))
    _draw_body(c, data, title_color=(0.1, 0.3, 0.6))

def draw_professional_template(c, data):
    _draw_header(c, data, font_color=(0, 0, 0))
    _draw_body(c, data, title_color=(0, 0, 0))

def draw_minimal_template(c, data):
    _draw_header(c, data, font_color=(0.2, 0.2, 0.2), minimal=True)
    _draw_body(c, data, title_color=(0.2, 0.2, 0.2))

def _draw_header(c, data, font_color, minimal=False):
    personal = data.get("personal", {})
    name = personal.get("name", "Your Name")
    email = personal.get("email", "email@example.com")
    phone = personal.get("phone", "123-456-7890")
    
    c.setFillColorRGB(*font_color)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 800, name)
    
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    contact_info = f"{email} | {phone}"
    if data.get("linkedin"):
        contact_info += f" | {data.get('linkedin')}"
    if data.get("github"):
        contact_info += f" | {data.get('github')}"
        
    c.drawString(50, 780, contact_info)
    
    if not minimal:
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.line(50, 770, 550, 770)

def _draw_body(c, data, title_color):
    y = 740
    sections = [
        ("Experience", data.get("experience")),
        ("Education", data.get("education")),
        ("Projects", data.get("projects")),
        ("Skills", data.get("skills")),
        ("Certifications", data.get("certifications")),
        ("Achievements", data.get("achievements")),
        ("Languages", data.get("languages"))
    ]
    
    for title, content in sections:
        if content and content.strip():
            # Draw section title
            c.setFillColorRGB(*title_color)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, title.upper())
            y -= 20
            
            # Draw content (simple text wrapping heuristic)
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica", 11)
            
            lines = content.split('\n')
            for line in lines:
                if y < 50: # Page break handling simplified
                    c.showPage()
                    y = 800
                # A robust implementation would wrap long lines here
                c.drawString(50, y, line[:100]) # Cap width for demo
                y -= 15
            y -= 15
