# HSE Xt-EHR Analysis Platform

A mobile-first Flask web application for viewing and exporting Xt-EHR Imaging Report analysis documents with Health Service Executive (HSE) branding.

## Features

### 📱 Mobile-First Design
- **Responsive Layout**: Optimized for mobile devices first, scales up to desktop
- **Touch-Friendly**: Large buttons, easy navigation, swipe-friendly interfaces
- **Progressive Enhancement**: Works on all devices, enhanced experience on modern browsers
- **Fast Loading**: Minimal CSS/JS, optimized for mobile networks

### 🎨 HSE Branding
- **Official HSE Colors**: Primary green (#009639), primary blue (#005eb8), and supporting palette
- **Professional Design**: Clean, medical-grade interface suitable for healthcare professionals
- **Accessibility**: High contrast ratios, clear typography, semantic HTML

### 📄 Document Management
- **Markdown Rendering**: Beautiful rendering of analysis documents
- **PDF Export**: Generate professional PDFs with HSE branding
- **Organized Categories**: Auto-categorized document library
- **Search-Friendly**: Easy navigation and document discovery

### 🔧 Technical Features
- **Responsive Tables**: Mobile-friendly table display with stack layout
- **Touch Gestures**: Swipe navigation, touch-optimized interactions
- **Offline-Ready**: Progressive Web App capabilities
- **Fast Performance**: Optimized for mobile connections

## Installation

### Prerequisites
- Python 3.8+
- wkhtmltopdf (for PDF generation)

### Install wkhtmltopdf

**Windows:**
1. Download from: https://wkhtmltopdf.org/downloads.html
2. Install the appropriate version for your system
3. Add to PATH or note installation directory

**macOS:**
```bash
brew install wkhtmltopdf
```

**Ubuntu/Debian:**
```bash
sudo apt-get install wkhtmltopdf
```

### Python Dependencies

```bash
# Navigate to flask_app directory
cd flask_app

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Start the Server

```bash
# From the flask_app directory
python app.py
```

The application will be available at: http://localhost:5000

### Mobile Access
- **Local Network**: Use your computer's IP address (e.g., http://192.168.1.100:5000)
- **Development**: Server binds to 0.0.0.0 for easy mobile testing

## Mobile-First Features

### Responsive Breakpoints
- **Mobile**: 320px - 767px (single column, stacked layout)
- **Tablet**: 768px - 991px (two-column layout)
- **Desktop**: 992px+ (full multi-column layout)

### Mobile Navigation
- **Collapsible Header**: Space-efficient mobile header
- **Floating Action Button**: Quick access to common actions
- **Breadcrumb Navigation**: Simplified for mobile screens
- **Touch-Friendly Buttons**: Minimum 44px touch targets

### Mobile-Optimized Tables
- **Stack Layout**: Tables transform to card-like layout on mobile
- **Data Labels**: Column headers become inline labels
- **Horizontal Scroll**: Fallback with scroll indicators
- **Touch Scrolling**: Smooth momentum scrolling

### Performance Optimizations
- **Lazy Loading**: Progressive content loading
- **Minimal Dependencies**: Lightweight asset loading
- **Mobile-First CSS**: Smaller initial payload
- **Touch Gestures**: Native mobile interactions

## Document Structure

The app automatically discovers and categorizes markdown files from:

```
project_root/
├── docs/                    # Documentation files
├── analysis/               # Analysis reports
├── README.md              # Project overview
├── EXECUTIVE_SUMMARY.md   # Key findings
└── flask_app/
    ├── app.py             # Main application
    ├── templates/         # HTML templates
    ├── static/           # CSS, JS, images
    └── requirements.txt  # Python dependencies
```

## API Endpoints

### Web Interface
- `GET /` - Document library homepage
- `GET /document/<path>` - View specific document
- `GET /export-pdf/<path>` - Export document as PDF

### API
- `GET /api/documents` - JSON list of all documents

## Customization

### HSE Color Palette
The application uses the official HSE color scheme:

```css
:root {
  --hse-primary-green: #009639;
  --hse-primary-blue: #005eb8;
  --hse-dark-blue: #003d7a;
  --hse-light-blue: #41b6e6;
  --hse-orange: #fa6c1b;
  --hse-red: #e31e24;
}
```

### Mobile Breakpoints
Customize responsive behavior in `static/hse-styles.css`:

```css
/* Mobile First (default) */
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 992px) { /* Desktop */ }
@media (min-width: 1200px) { /* Large Desktop */ }
```

## Browser Support

### Mobile Browsers
- **iOS Safari**: 12+
- **Chrome Mobile**: 70+
- **Firefox Mobile**: 68+
- **Samsung Internet**: 9+

### Desktop Browsers
- **Chrome**: 70+
- **Firefox**: 68+
- **Safari**: 12+
- **Edge**: 79+

## Development

### Running in Development
```bash
# Enable debug mode
export FLASK_ENV=development
python app.py
```

### Mobile Testing
1. Start the server: `python app.py`
2. Find your computer's IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
3. Access from mobile: `http://YOUR_IP:5000`

### Adding New Documents
1. Place markdown files in `docs/` or `analysis/` directories
2. Restart the Flask app
3. Documents will be automatically discovered and categorized

## Troubleshooting

### PDF Generation Issues
- **Error**: "wkhtmltopdf not found"
  - **Solution**: Install wkhtmltopdf and ensure it's in PATH
- **Error**: "Permission denied"
  - **Solution**: Check file permissions and temp directory access

### Mobile Display Issues
- **Problem**: Text too small on mobile
  - **Solution**: Check viewport meta tag, ensure mobile-first CSS
- **Problem**: Buttons too small for touch
  - **Solution**: Minimum 44px touch targets implemented

### Performance Issues
- **Problem**: Slow loading on mobile
  - **Solution**: Enable gzip, optimize images, use CDN for Bootstrap
- **Problem**: Large documents freeze browser
  - **Solution**: Implement pagination or lazy loading for large content

## License

© Health Service Executive - This application is designed for HSE internal use with official branding and styling guidelines.