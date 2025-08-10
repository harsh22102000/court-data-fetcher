from datetime import datetime
from app import db

class CaseQuery(db.Model):
    """Model to store case queries and responses for logging and caching"""
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(100), nullable=False)
    case_number = db.Column(db.String(100), nullable=False)
    filing_year = db.Column(db.Integer, nullable=False)
    query_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, default=False)
    error_message = db.Column(db.Text)
    
    # Parsed case data
    parties_name = db.Column(db.Text)
    filing_date = db.Column(db.String(50))
    next_hearing_date = db.Column(db.String(50))
    case_status = db.Column(db.String(200))
    
    # Raw response data
    raw_html_response = db.Column(db.Text)
    
    # PDF links found
    pdf_links = db.Column(db.Text)  # JSON string of PDF links
    
    def __repr__(self):
        return f'<CaseQuery {self.case_type}/{self.case_number}/{self.filing_year}>'

class PDFDownload(db.Model):
    """Model to track PDF downloads"""
    id = db.Column(db.Integer, primary_key=True)
    case_query_id = db.Column(db.Integer, db.ForeignKey('case_query.id'), nullable=False)
    pdf_url = db.Column(db.Text, nullable=False)
    download_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, default=False)
    file_size = db.Column(db.Integer)
    
    case_query = db.relationship('CaseQuery', backref=db.backref('pdf_downloads', lazy=True))
    
    def __repr__(self):
        return f'<PDFDownload {self.pdf_url}>'
