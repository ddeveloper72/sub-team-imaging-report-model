from flask import Flask, render_template, request, send_file, jsonify
import markdown
import os
import io
from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus.flowables import CondPageBreak
from reportlab.platypus import Flowable
from reportlab.lib.utils import ImageReader
from datetime import datetime
import re
import html
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'true'

# Base directory configuration
BASE_DIR = Path(os.environ.get('BASE_DIR', Path(__file__).parent.parent))
DOCS_DIR = BASE_DIR / 'docs'
ANALYSIS_DIR = BASE_DIR / 'analysis'

class DocumentSeparator(Flowable):
    """Custom flowable to create visual document separators"""
    
    def __init__(self, doc_title, doc_number, total_docs, width=None, is_landscape=True):
        Flowable.__init__(self)
        self.doc_title = doc_title
        self.doc_number = doc_number
        self.total_docs = total_docs
        self.is_landscape = is_landscape
        
        # Set width and font sizes based on orientation
        if is_landscape:
            self.width = width or 10.2 * inch  # Landscape width
            self.doc_title_font = 14
            self.doc_number_font = 16
            self.branding_font = 10
        else:
            self.width = width or 6.8 * inch   # Portrait width
            self.doc_title_font = 11
            self.doc_number_font = 12
            self.branding_font = 8
            
        self.height = 1.5 * inch
    
    def draw(self):
        """Draw the document separator"""
        canvas = self.canv
        
        # Draw top border line
        canvas.setStrokeColor(colors.Color(0, 95/255, 95/255))  # HCO teal
        canvas.setLineWidth(3)
        canvas.line(0, self.height - 0.1*inch, self.width, self.height - 0.1*inch)
        
        # Draw main title background
        canvas.setFillColor(colors.Color(0, 95/255, 95/255, alpha=0.1))  # Light teal background
        canvas.rect(0, self.height - 0.8*inch, self.width, 0.5*inch, fill=1, stroke=0)
        
        # Draw document title with orientation-appropriate font size
        canvas.setFont("Helvetica-Bold", self.doc_number_font)
        canvas.setFillColor(colors.Color(0, 95/255, 95/255))
        canvas.drawString(0.2*inch, self.height - 0.6*inch, f"Document {self.doc_number} of {self.total_docs}")
        
        # Draw document name with orientation-appropriate font size
        canvas.setFont("Helvetica-Bold", self.doc_title_font)
        canvas.setFillColor(colors.Color(30/255, 58/255, 95/255))  # HCO accent blue
        
        # Truncate title if too long for portrait mode
        display_title = self.doc_title
        if not self.is_landscape and len(display_title) > 50:
            display_title = display_title[:47] + "..."
            
        canvas.drawString(0.2*inch, self.height - 0.9*inch, display_title)
        
        # Draw Xt-EHR team branding with orientation-appropriate font size
        canvas.setFont("Helvetica", self.branding_font)
        canvas.setFillColor(colors.Color(45/255, 55/255, 72/255))  # HCO neutral
        
        # Adjust branding text for portrait mode
        if self.is_landscape:
            canvas.drawRightString(self.width - 0.2*inch, self.height - 0.6*inch, "Xt-EHR T7.2 Sub-team for Imaging Reports Model")
            canvas.drawRightString(self.width - 0.2*inch, self.height - 0.9*inch, "Xt-EHR Analysis Platform")
        else:
            # Shorter branding text for portrait mode
            canvas.drawRightString(self.width - 0.2*inch, self.height - 0.6*inch, "Xt-EHR T7.2 Imaging Reports")
            canvas.drawRightString(self.width - 0.2*inch, self.height - 0.9*inch, "Analysis Platform")
        
        # Draw bottom border line
        canvas.setStrokeColor(colors.Color(0, 95/255, 95/255))
        canvas.setLineWidth(1)
        canvas.line(0, 0.1*inch, self.width, 0.1*inch)


class PageFooter(Flowable):
    """Custom flowable for page footers"""
    
    def __init__(self, doc_title, page_info, width=None):
        Flowable.__init__(self)
        self.doc_title = doc_title
        self.page_info = page_info
        self.width = width or 10.2 * inch
        self.height = 0.5 * inch
    
    def draw(self):
        """Draw the page footer"""
        canvas = self.canv
        
        # Draw footer line
        canvas.setStrokeColor(colors.Color(0, 95/255, 95/255, alpha=0.5))
        canvas.setLineWidth(0.5)
        canvas.line(0, self.height - 0.1*inch, self.width, self.height - 0.1*inch)
        
        # Draw document title on left
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.Color(45/255, 55/255, 72/255))
        canvas.drawString(0, 0.1*inch, self.doc_title[:60] + "..." if len(self.doc_title) > 60 else self.doc_title)
        
        # Draw page info on right
        canvas.drawRightString(self.width, 0.1*inch, self.page_info)


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
    
    def clean_html_for_reportlab(self, html_content):
        """Clean HTML content for ReportLab compatibility"""
        import re
        
        # Remove problematic tags and attributes
        html_content = re.sub(r'<div[^>]*>', '', html_content)
        html_content = re.sub(r'</div>', '', html_content)
        html_content = re.sub(r'<span[^>]*>', '', html_content)
        html_content = re.sub(r'</span>', '', html_content)
        html_content = re.sub(r'<a[^>]*>', '', html_content)
        html_content = re.sub(r'</a>', '', html_content)
        html_content = re.sub(r' class="[^"]*"', '', html_content)
        html_content = re.sub(r' id="[^"]*"', '', html_content)
        
        # Fix nested font and italic tags that cause parsing issues
        # Replace <font> tags with simpler markup
        html_content = re.sub(r'<font[^>]*>', '<code>', html_content)
        html_content = re.sub(r'</font>', '</code>', html_content)
        
        # Fix specific problem patterns from the error
        html_content = re.sub(r'<i></font>', '</i>', html_content)
        html_content = re.sub(r'<font[^>]*><i>', '<i>', html_content)
        html_content = re.sub(r'</i></font>', '</i>', html_content)
        
        # Clean up any remaining malformed tags
        html_content = re.sub(r'<([^>]+)>\s*</\1>', '', html_content)  # Remove empty tags
        html_content = re.sub(r'<code>\s*<i>', '<i><code>', html_content)  # Fix nested order
        html_content = re.sub(r'</i>\s*</code>', '</code></i>', html_content)  # Fix nested order
        
        return html_content
    
    def needs_landscape(self, table_data):
        """Determine if a table needs landscape orientation based on content"""
        if not table_data or len(table_data) == 0:
            return False
        
        # Count total characters across all columns in the header row
        if len(table_data) > 0:
            header_length = sum(len(str(cell)) for cell in table_data[0])
            # If header is very long or we have many columns, use landscape
            return header_length > 80 or len(table_data[0]) >= 4
        
        return False
    
    def create_wrapped_table(self, table_data, is_landscape=True):
        """Create a table with proper text wrapping in cells"""
        if not table_data:
            return None
        
        # Create paragraph styles for table cells
        from reportlab.lib.styles import ParagraphStyle
        
        # Header cell style
        header_style = ParagraphStyle(
            'TableHeader',
            fontName='Helvetica-Bold',
            fontSize=12 if is_landscape else 10,
            textColor=colors.whitesmoke,
            alignment=0,  # Left align
            spaceAfter=0,
            spaceBefore=0,
            leftIndent=0,
            rightIndent=0
        )
        
        # Body cell style
        body_style = ParagraphStyle(
            'TableBody',
            fontName='Helvetica',
            fontSize=10 if is_landscape else 9,
            textColor=colors.black,
            alignment=0,  # Left align
            spaceAfter=0,
            spaceBefore=0,
            leftIndent=0,
            rightIndent=0,
            leading=12 if is_landscape else 11  # Line spacing
        )
        
        # Convert table data to paragraph objects for proper wrapping
        wrapped_table_data = []
        for row_idx, row in enumerate(table_data):
            wrapped_row = []
            for cell in row:
                # Clean cell content
                clean_cell = str(cell).strip()
                clean_cell = ' '.join(clean_cell.split())
                
                # Don't truncate - let wrapping handle long content
                # Create paragraph object for proper wrapping
                if row_idx == 0:  # Header row
                    para = Paragraph(clean_cell, header_style)
                else:  # Body rows
                    para = Paragraph(clean_cell, body_style)
                
                wrapped_row.append(para)
            wrapped_table_data.append(wrapped_row)
        
        # Calculate column widths for landscape orientation
        if is_landscape:
            page_width = 10.2 * inch
        else:
            page_width = 6.8 * inch
            
        num_cols = len(wrapped_table_data[0]) if wrapped_table_data else 4
        
        # Set column widths optimized for content type
        if num_cols == 4:  # Element, Classification, Rationale, Real-World Usage
            if is_landscape:
                col_widths = [
                    page_width * 0.30,  # Element (30%)
                    page_width * 0.15,  # Classification (15%) 
                    page_width * 0.40,  # Rationale (40%) - most space for wrapping
                    page_width * 0.15   # Real-World Usage (15%)
                ]
            else:
                col_widths = [
                    page_width * 0.28,  # Element (28%)
                    page_width * 0.18,  # Classification (18%)
                    page_width * 0.32,  # Rationale (32%)
                    page_width * 0.22   # Real-World Usage (22%)
                ]
        elif num_cols == 6:  # Element, Path, Cardinality, Status, Type, Description
            if is_landscape:
                col_widths = [
                    page_width * 0.20,  # Element (20%)
                    page_width * 0.25,  # Path (25%)
                    page_width * 0.10,  # Cardinality (10%)
                    page_width * 0.08,  # Status (8%)
                    page_width * 0.12,  # Type (12%)
                    page_width * 0.25   # Description (25%)
                ]
            else:
                col_widths = [page_width / num_cols] * num_cols
        else:
            # Equal width for other tables
            col_widths = [page_width / num_cols] * num_cols
        
        table = Table(wrapped_table_data, colWidths=col_widths)
        
        # Enhanced table style with proper wrapping support
        table_style = TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0, 95/255, 95/255)),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            
            # Body styling  
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            
            # Padding for wrapped content
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
            
            # Allow row height to expand for wrapped content
            ('MINROWHEIGHT', (0, 0), (-1, -1), 0.3*inch),  # Minimum row height
            ('WORDWRAP', (0, 0), (-1, -1), 'WORD'),  # Enable word wrapping
            ('SPLITLONGWORDS', (0, 0), (-1, -1), True),  # Split very long words
        ])
        
        table.setStyle(table_style)
        return table
    
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

@app.route('/collection')
def document_collection():
    """Document collection page for bulk PDF generation"""
    files = renderer.get_document_files()
    return render_template('collection.html', files=files)

@app.route('/export-bulk-pdf', methods=['POST'])
def export_bulk_pdf():
    """Generate a combined PDF from selected documents with user-selected orientation"""
    try:
        # Get selected documents and orientation from form
        selected_docs = request.form.getlist('selected_documents')
        pdf_orientation = request.form.get('pdf_orientation', 'landscape')  # Default to landscape
        
        if not selected_docs:
            return jsonify({'error': 'No documents selected'}), 400
        
        # Create a BytesIO buffer to store the PDF
        buffer = io.BytesIO()
        
        # Create PDF document with user-selected orientation
        if pdf_orientation == 'portrait':
            page_size = A4
        else:
            page_size = landscape(A4)
            
        doc = SimpleDocTemplate(buffer, pagesize=page_size, 
                              rightMargin=0.8*inch, leftMargin=0.8*inch,
                              topMargin=1*inch, bottomMargin=1*inch)
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Determine font sizes based on orientation
        if page_size == landscape(A4):
            # Landscape orientation - more horizontal space, can use larger fonts
            title_font_size = 22
            doc_title_font_size = 18
            heading_font_size = 16
        else:
            # Portrait orientation - less horizontal space, use smaller fonts to prevent overflow
            title_font_size = 14
            doc_title_font_size = 12
            heading_font_size = 11
        
        # Create custom styles with HCO colors and dynamic sizing
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=title_font_size,
            textColor=colors.Color(0, 95/255, 95/255),  # HCO primary teal
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        doc_title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=doc_title_font_size,
            textColor=colors.Color(0, 95/255, 95/255),  # HCO primary teal
            spaceBefore=30,
            spaceAfter=20,
            alignment=0  # Left alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=heading_font_size,
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
        
        # Build PDF content
        story = []
        
        # Add main header
        story.append(Paragraph("Xt-EHR T7.2 Sub-team for Imaging Reports Model", title_style))
        story.append(Paragraph("Xt-EHR Analysis Platform - Document Collection", normal_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", normal_style))
        story.append(Spacer(1, 30))
        
        # Add table of contents
        story.append(Paragraph("Table of Contents", heading_style))
        for i, doc_path in enumerate(selected_docs, 1):
            file_path = BASE_DIR / doc_path
            if file_path.exists():
                story.append(Paragraph(f"{i}. {file_path.stem}", normal_style))
        story.append(Spacer(1, 20))
        
        # Process each selected document
        for i, doc_path in enumerate(selected_docs, 1):
            file_path = BASE_DIR / doc_path
            
            if not file_path.exists():
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add document separator (except for the first document)
                if i > 1:
                    story.append(PageBreak())
                    story.append(Spacer(1, 20))
                
                # Add prominent document separator
                doc_separator = DocumentSeparator(
                    doc_title=file_path.stem.replace('_', ' ').replace('-', ' ').title(),
                    doc_number=i,
                    total_docs=len(selected_docs),
                    is_landscape=(pdf_orientation == 'landscape')
                )
                story.append(doc_separator)
                story.append(Spacer(1, 20))
                
                # Add document metadata section
                metadata_style = ParagraphStyle(
                    'DocumentMetadata',
                    parent=normal_style,
                    fontSize=9,
                    textColor=colors.Color(100/255, 100/255, 100/255),
                    leftIndent=0.2*inch,
                    spaceAfter=15
                )
                
                # Get file stats for metadata
                file_stat = file_path.stat()
                file_size = round(file_stat.st_size / 1024, 1)  # Size in KB
                modified_time = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                
                story.append(Paragraph(f"<b>File:</b> {file_path.name} | <b>Size:</b> {file_size} KB | <b>Modified:</b> {modified_time}", metadata_style))
                story.append(Spacer(1, 10))
                
                # Parse markdown content for this document
                lines = content.split('\n')
                line_idx = 0
                
                while line_idx < len(lines):
                    line = lines[line_idx].strip()
                    
                    # Skip empty lines
                    if not line:
                        line_idx += 1
                        continue
                    
                    # Handle headers
                    if line.startswith('#'):
                        level = len(line) - len(line.lstrip('#'))
                        header_text = line.lstrip('#').strip()
                        
                        if level == 1:
                            story.append(Spacer(1, 15))
                            story.append(Paragraph(html.escape(header_text), heading_style))
                        elif level == 2:
                            story.append(Spacer(1, 12))
                            story.append(Paragraph(html.escape(header_text), heading_style))
                        else:
                            story.append(Spacer(1, 8))
                            story.append(Paragraph(html.escape(header_text), heading_style))
                        
                        story.append(Spacer(1, 6))
                        line_idx += 1
                        continue
                    
                    # Handle tables
                    if '|' in line and ('Element' in line or 'Classification' in line or '---' in line):
                        # Parse table
                        table_data = []
                        
                        while line_idx < len(lines) and ('|' in lines[line_idx] or not lines[line_idx].strip()):
                            current_line = lines[line_idx].strip()
                            if current_line and '|' in current_line:
                                row_data = [cell.strip() for cell in current_line.split('|')[1:-1]]
                                if row_data and not all('---' in cell for cell in row_data):
                                    table_data.append(row_data)
                            line_idx += 1
                        
                        if table_data:
                            # Use the new wrapped table method with user-selected orientation
                            is_landscape = (pdf_orientation == 'landscape')
                            wrapped_table = renderer.create_wrapped_table(table_data, is_landscape=is_landscape)
                            if wrapped_table:
                                story.append(wrapped_table)
                                story.append(Spacer(1, 12))
                        continue
                    
                    # Handle regular paragraphs
                    paragraph_lines = [line]
                    line_idx += 1
                    
                    while line_idx < len(lines) and lines[line_idx].strip() and not lines[line_idx].startswith('#') and '|' not in lines[line_idx]:
                        paragraph_lines.append(lines[line_idx].strip())
                        line_idx += 1
                    
                    if paragraph_lines:
                        para_text = ' '.join(paragraph_lines)
                        
                        # First convert markdown to HTML
                        html_content = renderer.render_markdown(para_text)
                        
                        # Clean HTML for ReportLab compatibility
                        clean_html = renderer.clean_html_for_reportlab(html_content)
                        
                        # Remove paragraph tags as ReportLab adds them
                        clean_html = re.sub(r'</?p[^>]*>', '', clean_html)
                        
                        try:
                            story.append(Paragraph(clean_html, normal_style))
                            story.append(Spacer(1, 6))
                        except Exception as e:
                            # Fallback to plain text if HTML parsing fails
                            plain_text = html.escape(para_text)
                            story.append(Paragraph(plain_text, normal_style))
                            story.append(Spacer(1, 6))
                
                # Add document footer separator
                story.append(Spacer(1, 20))
                footer_separator_style = ParagraphStyle(
                    'FooterSeparator',
                    parent=normal_style,
                    fontSize=8,
                    textColor=colors.Color(150/255, 150/255, 150/255),
                    alignment=1,  # Center alignment
                    borderWidth=1,
                    borderColor=colors.Color(200/255, 200/255, 200/255),
                    borderPadding=5
                )
                story.append(Paragraph(f"— End of Document {i}: {file_path.stem.replace('_', ' ').replace('-', ' ').title()} —", footer_separator_style))
                story.append(Spacer(1, 15))
                        
            except Exception as e:
                # Add error note for failed documents with more detail
                error_msg = f"Error processing {file_path.stem}: {str(e)}"
                print(f"PDF Generation Error: {error_msg}")  # Log for debugging
                
                # Try to add a simple error message to the PDF
                try:
                    error_style = ParagraphStyle(
                        'ErrorMessage',
                        parent=normal_style,
                        fontSize=10,
                        textColor=colors.red,
                        leftIndent=0.2*inch,
                        borderWidth=1,
                        borderColor=colors.red,
                        borderPadding=10,
                        backColor=colors.Color(1, 0.95, 0.95)  # Light red background
                    )
                    story.append(Paragraph(f"<b>⚠ Error Processing Document {i}:</b> {file_path.stem}", error_style))
                    story.append(Paragraph(f"<i>Reason:</i> Document contains formatting that cannot be processed", error_style))
                    story.append(Spacer(1, 20))
                    
                    # Add document footer even for errors
                    footer_separator_style = ParagraphStyle(
                        'FooterSeparator',
                        parent=normal_style,
                        fontSize=8,
                        textColor=colors.Color(150/255, 150/255, 150/255),
                        alignment=1,  # Center alignment
                        borderWidth=1,
                        borderColor=colors.Color(200/255, 200/255, 200/255),
                        borderPadding=5
                    )
                    story.append(Paragraph(f"— End of Document {i}: {file_path.stem.replace('_', ' ').replace('-', ' ').title()} (Error) —", footer_separator_style))
                    story.append(Spacer(1, 15))
                except:
                    # If even the error message fails, continue silently
                    pass
        
        # Add final summary section
        story.append(PageBreak())
        story.append(Spacer(1, 30))
        
        # Final document summary
        summary_title_style = ParagraphStyle(
            'SummaryTitle',
            parent=title_style,
            fontSize=16,
            textColor=colors.Color(0, 95/255, 95/255),
            alignment=1,  # Center alignment
            spaceAfter=20
        )
        
        summary_style = ParagraphStyle(
            'SummaryContent',
            parent=normal_style,
            fontSize=11,
            alignment=1,  # Center alignment
            spaceAfter=10
        )
        
        # Credits section
        credits_style = ParagraphStyle(
            'CreditsContent',
            parent=normal_style,
            fontSize=9,
            textColor=colors.Color(100/255, 100/255, 100/255),
            alignment=1,  # Center alignment
            spaceAfter=8
        )
        
        story.append(Paragraph("📄 Document Collection Summary", summary_title_style))
        story.append(Paragraph(f"Total Documents Processed: <b>{len(selected_docs)}</b>", summary_style))
        story.append(Paragraph(f"Generated: <b>{datetime.now().strftime('%B %d, %Y at %I:%M %p')}</b>", summary_style))
        story.append(Paragraph("Xt-EHR T7.2 Sub-team for Imaging Reports Model", summary_style))
        story.append(Spacer(1, 20))
        
        # Add data source credits
        story.append(Paragraph("Data Sources", summary_title_style))
        story.append(Paragraph("Analysis based on PARROT v1.0 dataset and Xt-EHR FHIR Implementation Guide", credits_style))
        story.append(Paragraph("PARROT v1.0: https://github.com/PARROT-reports/PARROT_v1.0", credits_style))
        story.append(Paragraph("Xt-EHR: https://build.fhir.org/ig/Xt-EHR/xt-ehr-common/index.html", credits_style))
        story.append(Spacer(1, 30))
        
        # Add decorative footer
        final_footer_style = ParagraphStyle(
            'FinalFooter',
            parent=normal_style,
            fontSize=8,
            textColor=colors.Color(150/255, 150/255, 150/255),
            alignment=1,
            borderWidth=2,
            borderColor=colors.Color(0, 95/255, 95/255),
            borderPadding=10
        )
        story.append(Paragraph("Thank you for using the Xt-EHR Analysis Platform", final_footer_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        # Create filename with timestamp and orientation
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        orientation_suffix = pdf_orientation.capitalize()
        filename = f'XtEHR_T7.2_Document_Collection_{orientation_suffix}_{timestamp}.pdf'
        
        # Create response
        response = send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        return response
        
    except Exception as e:
        # Log the full error for debugging
        import traceback
        print(f"Bulk PDF Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        
        return jsonify({
            'error': 'Bulk PDF generation failed',
            'message': f'Technical error: {str(e)[:200]}{"..." if len(str(e)) > 200 else ""}',
            'suggestion': 'Some documents contain formatting issues. Try generating PDFs individually to identify problematic documents.'
        }), 500

@app.route('/export-pdf/<path:doc_path>', methods=['GET', 'POST'])
def export_pdf(doc_path):
    """Export document as PDF with user-selected orientation"""
    file_path = BASE_DIR / doc_path
    
    if not file_path.exists() or not file_path.suffix == '.md':
        return "Document not found", 404
    
    try:
        # Get orientation from form (POST) or default to landscape (GET)
        if request.method == 'POST':
            pdf_orientation = request.form.get('pdf_orientation', 'landscape')
        else:
            pdf_orientation = 'landscape'  # Default for backward compatibility
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        html_content = renderer.render_markdown(content)
        
        # Generate PDF using reportlab
        try:
            # Create a BytesIO buffer to store the PDF
            buffer = io.BytesIO()
            
            # Create PDF document with user-selected orientation
            if pdf_orientation == 'portrait':
                page_size = A4
            else:
                page_size = landscape(A4)
                
            doc = SimpleDocTemplate(buffer, pagesize=page_size, 
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
            story.append(Paragraph("Xt-EHR T7.2 Sub-team for Imaging Reports Model", title_style))
            story.append(Paragraph(f"Xt-EHR Analysis Platform", normal_style))
            story.append(Paragraph(f"Document: {file_path.stem}", heading_style))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", normal_style))
            story.append(Spacer(1, 10))
            
            # Add data source credits
            credits_style = ParagraphStyle(
                'CreditsContent',
                parent=normal_style,
                fontSize=9,
                textColor=colors.Color(100/255, 100/255, 100/255),
                alignment=1,  # Center alignment
                spaceAfter=8
            )
            story.append(Paragraph("Analysis based on PARROT v1.0 dataset and Xt-EHR FHIR Implementation Guide", credits_style))
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
                        # Use the new wrapped table method with user-selected orientation
                        is_landscape = (pdf_orientation == 'landscape')
                        wrapped_table = renderer.create_wrapped_table(table_data, is_landscape=is_landscape)
                        if wrapped_table:
                            story.append(wrapped_table)
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
                    
                    # First convert markdown to HTML
                    html_content = renderer.render_markdown(para_text)
                    
                    # Clean HTML for ReportLab compatibility
                    clean_html = renderer.clean_html_for_reportlab(html_content)
                    
                    # Remove paragraph tags as ReportLab adds them
                    clean_html = re.sub(r'</?p[^>]*>', '', clean_html)
                    
                    try:
                        story.append(Paragraph(clean_html, normal_style))
                        story.append(Spacer(1, 6))
                    except Exception as e:
                        # Fallback to plain text if HTML parsing fails
                        plain_text = html.escape(para_text)
                        story.append(Paragraph(plain_text, normal_style))
                        story.append(Spacer(1, 6))
            
            # Build PDF
            doc.build(story)
            
            # Get PDF bytes
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            # Create response with orientation in filename
            orientation_suffix = pdf_orientation.capitalize()
            response = send_file(
                io.BytesIO(pdf_bytes),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f"{file_path.stem}_{orientation_suffix}.pdf"
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

@app.route('/favicon.ico')
def favicon():
    """Serve the MyHealth@EU favicon"""
    return send_file(
        'static/favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"Serving documents from: {BASE_DIR}")
    print(f"Available at: http://localhost:{port}")
    print(f"Debug mode: {debug}")
    
    app.run(debug=debug, host=host, port=port)