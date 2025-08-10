import json
import logging
from flask import render_template, request, flash, redirect, url_for, make_response, abort
from app import app, db
from models import CaseQuery, PDFDownload
from scraper import DelhiHighCourtScraper

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Main page with case search form"""
    # Common case types for Delhi High Court
    case_types = [
        'W.P.(C)',  # Writ Petition (Civil)
        'CRL.A.',   # Criminal Appeal
        'CRL.REV.P.',  # Criminal Revision Petition
        'CS(OS)',   # Civil Suit (Original Side)
        'FAO',      # First Appeal from Order
        'CRL.M.C.', # Criminal Miscellaneous Case
        'W.P.(CRL)', # Writ Petition (Criminal)
        'CRL.W.',   # Criminal Writ
        'LPA',      # Letters Patent Appeal
        'CM',       # Chamber Matter
    ]
    
    # Get recent queries for display
    recent_queries = CaseQuery.query.filter_by(success=True).order_by(
        CaseQuery.query_timestamp.desc()
    ).limit(5).all()
    
    return render_template('index.html', case_types=case_types, recent_queries=recent_queries)

@app.route('/search', methods=['POST'])
def search_case():
    """Handle case search request"""
    try:
        case_type = request.form.get('case_type', '').strip()
        case_number = request.form.get('case_number', '').strip()
        filing_year = request.form.get('filing_year', '').strip()
        
        # Validate input
        if not all([case_type, case_number, filing_year]):
            flash('All fields are required', 'error')
            return redirect(url_for('index'))
        
        try:
            filing_year = int(filing_year)
            if filing_year < 1950 or filing_year > 2025:
                flash('Invalid filing year', 'error')
                return redirect(url_for('index'))
        except ValueError:
            flash('Filing year must be a valid number', 'error')
            return redirect(url_for('index'))
        
        # Check if we have a recent cached result
        cached_query = CaseQuery.query.filter_by(
            case_type=case_type,
            case_number=case_number,
            filing_year=filing_year,
            success=True
        ).order_by(CaseQuery.query_timestamp.desc()).first()
        
        # Use cache if less than 1 hour old
        if cached_query and (cached_query.query_timestamp.timestamp() > 
                           (db.func.now().timestamp() - 3600)):
            logger.info(f"Using cached result for {case_type} {case_number}/{filing_year}")
            return render_template('results.html', 
                                 case_data=cached_query, 
                                 pdf_links=json.loads(cached_query.pdf_links or '[]'))
        
        # Create new query record
        query = CaseQuery(
            case_type=case_type,
            case_number=case_number,
            filing_year=filing_year
        )
        
        # Perform scraping
        scraper = DelhiHighCourtScraper()
        result = scraper.scrape_case_data(case_type, case_number, filing_year)
        
        # Update query record with results
        if result['success']:
            query.success = True
            query.parties_name = result.get('parties_name', '')
            query.filing_date = result.get('filing_date', '')
            query.next_hearing_date = result.get('next_hearing_date', '')
            query.case_status = result.get('case_status', '')
            query.raw_html_response = result.get('raw_html', '')
            query.pdf_links = json.dumps(result.get('pdf_links', []))
            
            flash('Case details retrieved successfully', 'success')
        else:
            query.success = False
            query.error_message = result.get('error', 'Unknown error occurred')
            query.raw_html_response = result.get('raw_html', '')
            
            flash(f"Search failed: {query.error_message}", 'error')
        
        # Save query to database
        db.session.add(query)
        db.session.commit()
        
        if result['success']:
            return render_template('results.html', 
                                 case_data=query, 
                                 pdf_links=result.get('pdf_links', []))
        else:
            return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Error in search_case: {e}")
        flash(f"An unexpected error occurred: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/download_pdf')
def download_pdf():
    """Handle PDF download requests"""
    try:
        pdf_url = request.args.get('url')
        case_query_id = request.args.get('case_id')
        
        if not pdf_url:
            flash('PDF URL is required', 'error')
            return redirect(url_for('index'))
        
        # Create download record
        download_record = PDFDownload(
            case_query_id=case_query_id,
            pdf_url=pdf_url
        )
        
        # Download the PDF
        scraper = DelhiHighCourtScraper()
        result = scraper.download_pdf(pdf_url)
        
        if result['success']:
            download_record.success = True
            download_record.file_size = result.get('size', 0)
            
            # Create response with PDF content
            response = make_response(result['content'])
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename="{result["filename"]}"'
            
            # Save download record
            db.session.add(download_record)
            db.session.commit()
            
            return response
        else:
            download_record.success = False
            db.session.add(download_record)
            db.session.commit()
            
            flash(f"PDF download failed: {result.get('error', 'Unknown error')}", 'error')
            return redirect(request.referrer or url_for('index'))
        
    except Exception as e:
        logger.error(f"Error in download_pdf: {e}")
        flash(f"PDF download failed: {str(e)}", 'error')
        return redirect(request.referrer or url_for('index'))

@app.route('/history')
def query_history():
    """Display query history"""
    page = request.args.get('page', 1, type=int)
    queries = CaseQuery.query.order_by(CaseQuery.query_timestamp.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('history.html', queries=queries)

@app.route('/api/case/<int:case_id>')
def api_case_details(case_id):
    """API endpoint to get case details as JSON"""
    try:
        case = CaseQuery.query.get_or_404(case_id)
        
        return {
            'id': case.id,
            'case_type': case.case_type,
            'case_number': case.case_number,
            'filing_year': case.filing_year,
            'success': case.success,
            'parties_name': case.parties_name,
            'filing_date': case.filing_date,
            'next_hearing_date': case.next_hearing_date,
            'case_status': case.case_status,
            'pdf_links': json.loads(case.pdf_links or '[]'),
            'query_timestamp': case.query_timestamp.isoformat() if case.query_timestamp else None
        }
    except Exception as e:
        logger.error(f"Error in API case details: {e}")
        abort(500)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('base.html', 
                         content='<div class="alert alert-warning">Page not found</div>'), 404

@app.route('/download-project')
def download_project():
    """Download the complete project as ZIP file"""
    import zipfile
    import tempfile
    from flask import send_file
    from pathlib import Path
    import os
    
    try:
        # Create a temporary ZIP file
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, 'court-data-fetcher.zip')
        project_root = Path(__file__).parent
        
        # Files and folders to include
        include_patterns = ['*.py', '*.md', '*.txt', '*.html', '*.css', '*.js', '*.example']
        include_folders = ['templates', 'static']
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all Python and config files
            for pattern in include_patterns:
                for file_path in project_root.glob(pattern):
                    if file_path.is_file() and file_path.name != 'download_zip.html':
                        arcname = file_path.name
                        zipf.write(file_path, arcname)
            
            # Add template and static folders
            for folder in include_folders:
                folder_path = project_root / folder
                if folder_path.exists():
                    for file_path in folder_path.rglob('*'):
                        if file_path.is_file():
                            arcname = file_path.relative_to(project_root)
                            zipf.write(file_path, arcname)
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name='court-data-fetcher.zip',
            mimetype='application/zip'
        )
        
    except Exception as e:
        logger.error(f"Error creating project ZIP: {e}")
        flash(f"Error creating download: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base.html', 
                         content='<div class="alert alert-danger">Internal server error</div>'), 500
