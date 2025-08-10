# Court Data Fetcher

## Overview

A web application for searching and retrieving case information from Delhi High Court. Users can input case details (type, number, filing year) to fetch case metadata, party information, hearing dates, and downloadable court documents. The application features a clean, responsive interface with dark theme support and maintains a searchable history of all queries.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Flask with Jinja2 templating engine
- **UI Components**: Bootstrap 5 with dark theme and Font Awesome icons
- **Responsive Design**: Mobile-first approach using Bootstrap grid system
- **Client-side Functionality**: Vanilla JavaScript for form validation, tooltips, and keyboard shortcuts
- **Styling**: Custom CSS enhancements with hover effects and smooth transitions

### Backend Architecture
- **Web Framework**: Flask with SQLAlchemy ORM for database operations
- **Application Structure**: Modular design with separate files for routes, models, and scraping logic
- **Request Handling**: RESTful routes for case search, results display, and query history
- **Session Management**: Flask sessions with configurable secret key
- **Error Handling**: Comprehensive error catching with user-friendly flash messages

### Data Storage Solutions
- **Primary Database**: SQLite for development (configurable to other databases via DATABASE_URL)
- **ORM**: SQLAlchemy with declarative base model approach
- **Schema Design**: Two main entities - CaseQuery for storing search requests and results, PDFDownload for tracking document downloads
- **Data Persistence**: Raw HTML responses stored for debugging and potential re-parsing
- **Connection Management**: Pool recycling and pre-ping enabled for reliability

### Web Scraping Architecture
- **Primary Tool**: Selenium WebDriver with Chrome in headless mode
- **Fallback Strategy**: Requests session for simpler HTTP operations
- **Target Site**: Delhi High Court (delhihighcourt.nic.in)
- **CAPTCHA Handling**: Selenium-based approach with retry mechanisms
- **Session Management**: Dynamic view-state token parsing and session persistence
- **Data Extraction**: BeautifulSoup for HTML parsing and content extraction

### Authentication and Authorization
- **Current State**: No authentication system implemented
- **Session Security**: Secret key configuration for Flask sessions
- **Future Considerations**: Basic authentication could be added for query history protection

## External Dependencies

### Core Web Framework
- **Flask**: Web application framework and routing
- **Flask-SQLAlchemy**: Database ORM and connection management
- **Werkzeug**: WSGI utilities and proxy fix middleware

### Web Scraping Tools
- **Selenium**: Browser automation for dynamic content and CAPTCHA handling
- **BeautifulSoup**: HTML parsing and content extraction
- **Requests**: HTTP client for API calls and form submissions

### Frontend Libraries
- **Bootstrap 5**: CSS framework with dark theme support
- **Font Awesome**: Icon library for UI enhancement
- **Custom CSS/JS**: Application-specific styling and interactions

### Database Support
- **SQLite**: Default development database
- **PostgreSQL**: Production database support via DATABASE_URL configuration
- **SQLAlchemy**: Database abstraction layer supporting multiple backends

### Development and Deployment
- **Chrome WebDriver**: Required for Selenium browser automation
- **Environment Variables**: Configuration management for database URLs and secret keys
- **Logging**: Python's built-in logging for debugging and monitoring

### Court Website Integration
- **Delhi High Court Portal**: Primary data source at delhihighcourt.nic.in
- **Case Status API**: Integration with court's case status checking system
- **PDF Document Access**: Direct download links for court orders and judgments