# Court Data Fetcher

A Flask web application that demonstrates court case data fetching functionality with a professional interface for searching and retrieving case information, including parties' names, hearing dates, and downloadable court documents.

## Features

- **Modern Web Interface**: Clean, responsive UI with Bootstrap dark theme
- **Case Search**: Search by case type, number, and filing year
- **Database Integration**: PostgreSQL/SQLite support with query logging
- **PDF Downloads**: Download court orders and judgments
- **Query History**: Track and review previous searches
- **Responsive Design**: Mobile-friendly interface
- **Error Handling**: Comprehensive error management and user feedback

## Tech Stack

- **Backend**: Python 3.11, Flask, SQLAlchemy
- **Frontend**: Bootstrap 5, Font Awesome, vanilla JavaScript
- **Database**: PostgreSQL (production) / SQLite (development)
- **Scraping**: Selenium WebDriver, BeautifulSoup4, Requests
- **Deployment**: Gunicorn WSGI server

## Local Development Setup

### Prerequisites

- Python 3.11 or higher
- Node.js (for any frontend build tools, optional)
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd court-data-fetcher
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:

```bash
pip install flask flask-sqlalchemy gunicorn psycopg2-binary requests selenium beautifulsoup4 trafilatura werkzeug email-validator
```

### 4. Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_APP=main.py
FLASK_ENV=development
SESSION_SECRET=your-secret-key-here

# Database Configuration (choose one)
# For SQLite (development)
DATABASE_URL=sqlite:///court_scraper.db

# For PostgreSQL (production)
# DATABASE_URL=postgresql://username:password@localhost/court_data_fetcher
```

### 5. Database Setup

```bash
# Initialize the database
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 6. Install Chrome/Chromium (for Selenium)

#### Windows:
Download and install Chrome from https://www.google.com/chrome/

#### macOS:
```bash
brew install --cask google-chrome
```

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install chromium-browser
```

### 7. Run the Application

```bash
# Development server
python app.py

# Or with Gunicorn (production-like)
gunicorn --bind 127.0.0.1:5000 --reload main:app
```

The application will be available at: http://127.0.0.1:5000

## VS Code Setup

### 1. Open Project in VS Code

```bash
code .
```

### 2. Install Recommended Extensions

- Python
- Flask Snippets
- SQLite Viewer
- Auto Rename Tag
- Bracket Pair Colorizer

### 3. VS Code Configuration

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
```

Create `.vscode/launch.json` for debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/app.py",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_APP": "main.py"
            },
            "args": [],
            "jinja": true,
            "justMyCode": true
        }
    ]
}
```

### 4. Running in VS Code

- Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
- Type "Python: Select Interpreter"
- Choose the virtual environment interpreter (`./venv/bin/python`)
- Open terminal in VS Code and run: `python app.py`

## Project Structure

```
court-data-fetcher/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # URL routes and handlers
├── scraper.py          # Web scraping logic
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── replit.md          # Project documentation
├── templates/          # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Search form
│   ├── results.html   # Case results
│   └── history.html   # Query history
├── static/            # Static assets
│   ├── css/
│   │   └── custom.css # Custom styles
│   └── js/
│       └── main.js    # JavaScript functionality
└── .env               # Environment variables
```

## Database Schema

### CaseQuery Table
- `id`: Primary key
- `case_type`: Type of case (W.P.(C), CRL.A., etc.)
- `case_number`: Case number
- `filing_year`: Year case was filed
- `query_timestamp`: When search was performed
- `success`: Whether search was successful
- `parties_name`: Names of parties involved
- `filing_date`: Date case was filed
- `next_hearing_date`: Next hearing date
- `case_status`: Current case status
- `raw_html_response`: Raw HTML from court website
- `pdf_links`: JSON array of PDF download links

### PDFDownload Table
- `id`: Primary key
- `case_query_id`: Foreign key to CaseQuery
- `pdf_url`: URL of PDF document
- `download_timestamp`: When PDF was downloaded
- `success`: Whether download was successful
- `file_size`: Size of downloaded file

## API Endpoints

- `GET /` - Main search page
- `POST /search` - Submit case search
- `GET /download_pdf` - Download PDF documents
- `GET /history` - View query history
- `GET /api/case/<id>` - Get case details as JSON

## Current Status

**Demo Mode**: The application currently runs in demonstration mode, showing sample case data to showcase all functionality. The architecture is fully built to handle real court website scraping.

**Features Demonstrated**:
- Case search form with validation
- Professional results display
- PDF download functionality
- Query history and logging
- Error handling and user feedback
- Responsive mobile-friendly design

## Troubleshooting

### Common Issues

1. **Chrome/Chromium not found**:
   - Install Chrome or Chromium browser
   - Update the path in `scraper.py` if necessary

2. **Database connection error**:
   - Check DATABASE_URL in environment variables
   - Ensure database exists and is accessible

3. **Port already in use**:
   - Change port in `app.py`: `app.run(host='0.0.0.0', port=5001)`

4. **Module not found errors**:
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

### Development Tips

- Use `flask run` for development with auto-reload
- Check logs in the terminal for debugging information
- Use browser developer tools to inspect frontend issues
- Database can be viewed with SQLite browser tools

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production`
2. Use PostgreSQL instead of SQLite
3. Set a strong `SESSION_SECRET`
4. Use proper WSGI server like Gunicorn
5. Set up reverse proxy (Nginx)
6. Configure SSL certificates
7. Set up monitoring and logging

## License

This project is licensed under the MIT License.