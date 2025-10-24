from flask import Flask, render_template, request, send_file, jsonify
import markdown
import os
import io
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import re
import html

app = Flask(__name__)

# Configuration
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / 'docs'
ANALYSIS_DIR = BASE_DIR / 'analysis'

class MarkdownRenderer:
    """Handles markdown rendering and PDF generation"""
    
    def __init__(self):
        self.md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code', 
            'toc',
            'attr_list',
            'def_list'
        ])
    
    def render_markdown(self, content):
        """Convert markdown to HTML"""
        return self.md.convert(content)
    
    def get_document_files(self):
        """Get all markdown files from docs and analysis directories"""
        files = []
        
        # Get docs files
        if DOCS_DIR.exists():
            for file in DOCS_DIR.glob('*.md'):
                files.append({
                    'name': file.stem,
                    'path': str(file.relative_to(BASE_DIR)),
                    'category': 'Documentation',
                    'file_path': str(file)
                })
        
        # Get analysis files
        if ANALYSIS_DIR.exists():
            for file in ANALYSIS_DIR.glob('*.md'):
                files.append({
                    'name': file.stem,
                    'path': str(file.relative_to(BASE_DIR)),
                    'category': 'Analysis',
                    'file_path': str(file)
                })
        
        # Add root level files
        for file in BASE_DIR.glob('*.md'):
            files.append({
                'name': file.stem,
                'path': str(file.relative_to(BASE_DIR)),
                'category': 'Project Root',
                'file_path': str(file)
            })
        
        return sorted(files, key=lambda x: (x['category'], x['name']))

renderer = MarkdownRenderer()

@app.route('/')
def index():
    """Main page showing all available documents"""
    files = renderer.get_document_files()
    return render_template('index.html', files=files)

@app.route('/document/<path:doc_path>')
def view_document(doc_path):
    """View a specific markdown document"""
    file_path = BASE_DIR / doc_path
    
    if not file_path.exists() or not file_path.suffix == '.md':
        return "Document not found", 404
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        html_content = renderer.render_markdown(content)
        
        return render_template('document.html', 
                             content=html_content, 
                             title=file_path.stem,
                             doc_path=doc_path)
    except Exception as e:
        return f"Error reading document: {str(e)}", 500

@app.route('/export-pdf/<path:doc_path>')
def export_pdf(doc_path):
    """Export document as PDF"""
    file_path = BASE_DIR / doc_path
    
    if not file_path.exists() or not file_path.suffix == '.md':
        return "Document not found", 404
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        html_content = renderer.render_markdown(content)
        
        # Generate PDF using reportlab
        try:
            # Create a BytesIO buffer to store the PDF
            buffer = io.BytesIO()
            
            # Create PDF document
            doc = SimpleDocTemplate(buffer, pagesize=A4, 
                                  rightMargin=0.8*inch, leftMargin=0.8*inch,
                                  topMargin=1*inch, bottomMargin=1*inch)
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Create custom styles with HCO colors
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.Color(0, 95/255, 95/255),  # HCO primary teal
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.Color(45/255, 90/255, 39/255),  # HCO secondary green
                spaceBefore=20,
                spaceAfter=12
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.Color(45/255, 55/255, 72/255),  # HCO neutral dark
                spaceAfter=12
            )
            
            # Build PDF content with proper markdown parsing
            story = []
            
            # Add header
            story.append(Paragraph("Healthcare Organisation", title_style))
            story.append(Paragraph(f"Xt-EHR Analysis Platform", normal_style))
            story.append(Paragraph(f"Document: {file_path.stem}", heading_style))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", normal_style))
            story.append(Spacer(1, 20))
            
            # Parse markdown content properly
            lines = content.split('\n')
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                # Skip empty lines
                if not line:
                    i += 1
                    continue
                
                # Handle headers
                if line.startswith('#'):
                    level = len(line) - len(line.lstrip('#'))
                    header_text = line.lstrip('#').strip()
                    
                    if level == 1:
                        story.append(Spacer(1, 20))
                        story.append(Paragraph(html.escape(header_text), title_style))
                    elif level == 2:
                        story.append(Spacer(1, 15))
                        story.append(Paragraph(html.escape(header_text), heading_style))
                    else:
                        story.append(Spacer(1, 10))
                        story.append(Paragraph(html.escape(header_text), heading_style))
                    
                    story.append(Spacer(1, 6))
                    i += 1
                    continue
                
                # Handle tables
                if '|' in line and ('Element' in line or 'Classification' in line or '---' in line):
                    # This looks like a table, let's parse it
                    table_data = []
                    
                    # Get table rows
                    while i < len(lines) and ('|' in lines[i] or not lines[i].strip()):
                        current_line = lines[i].strip()
                        if current_line and '|' in current_line:
                            # Parse table row
                            row_data = [cell.strip() for cell in current_line.split('|')[1:-1]]  # Remove empty first/last
                            if row_data and not all('---' in cell for cell in row_data):  # Skip separator lines
                                table_data.append(row_data)
                        i += 1
                    
                    if table_data:
                        # Create ReportLab table
                        table = Table(table_data)
                        
                        # Style the table
                        table_style = TableStyle([
                            # Header row styling
                            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 95/255, 95/255)),  # HCO teal
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 10),
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, -1), 9),
                            
                            # Body styling
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 6),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                            ('TOPPADDING', (0, 0), (-1, -1), 4),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                            
                            # Alternating row colors
                            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)])
                        ])
                        
                        table.setStyle(table_style)
                        story.append(table)
                        story.append(Spacer(1, 12))
                    continue
                
                # Handle regular paragraphs
                paragraph_lines = [line]
                i += 1
                
                # Collect multi-line paragraphs
                while i < len(lines) and lines[i].strip() and not lines[i].startswith('#') and '|' not in lines[i]:
                    paragraph_lines.append(lines[i].strip())
                    i += 1
                
                if paragraph_lines:
                    # Join paragraph lines and clean up markdown
                    para_text = ' '.join(paragraph_lines)
                    
                    # Clean up markdown formatting
                    para_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', para_text)  # Bold
                    para_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', para_text)      # Italic
                    para_text = re.sub(r'`(.*?)`', r'<font name="Courier">\1</font>', para_text)  # Code
                    
                    story.append(Paragraph(para_text, normal_style))
                    story.append(Spacer(1, 6))
            
            # Build PDF
            doc.build(story)
            
            # Get PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            # Create response
            response = send_file(
                io.BytesIO(pdf_bytes),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f"{file_path.stem}.pdf"
            )
            return response
        except Exception as pdf_error:
            # Fallback error handling
            return jsonify({
                'error': 'PDF generation failed',
                'message': str(pdf_error),
                'suggestion': 'Please check the document format and try again'
            }), 500
            
    except Exception as e:
        return f"Error generating PDF: {str(e)}", 500

@app.route('/api/documents')
def api_documents():
    """API endpoint to get document list"""
    files = renderer.get_document_files()
    return jsonify(files)

if __name__ == '__main__':
    print(f"Serving documents from: {BASE_DIR}")
    print(f"Available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)