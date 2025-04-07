# Subscription Management System

A modern and elegant web application for managing restaurant subscriptions and payments. Built with Flask, PostgreSQL, and Bootstrap 5.

![Subscription Manager](app/static/images/screenshot.png)

## Features

### Devmenu Subscription Management
- **Add/Edit Subscriptions**
  - Restaurant details (name, email, website)
  - Subscription pricing and terms
  - Payment method tracking
  - Website credentials management
- **Subscription Status**
  - Active, paused, and canceled states
  - Automatic expiration date calculation
  - Grace period handling
- **Subscription List**
  - Modern table view with sorting
  - Quick actions (edit, delete)
  - Status indicators with badges
  - Direct website access links

### Dashboard & Analytics
- **Monthly Statistics**
  - Revenue tracking
  - Subscription analytics
  - Churn rate monitoring
- **Visual Charts**
  - Revenue trends
  - Subscription distribution
  - Payment method breakdown

### Security & Authentication
- **User Management**
  - Secure login system
  - Password hashing with bcrypt
  - Session management
- **Data Protection**
  - CSRF protection
  - SQL injection prevention
  - Input validation
  - Secure password storage

### Modern UI/UX
- **Responsive Design**
  - Mobile-friendly interface
  - Clean and intuitive layout
  - Bootstrap 5 components
- **Visual Elements**
  - Bootstrap Icons integration
  - Card-based design
  - Modern form inputs
  - Interactive tables
  - Status badges
  - Confirmation modals

## Technology Stack

- **Backend**
  - Python 3.8+
  - Flask 2.0+
  - SQLAlchemy ORM
  - Flask-Migrate
  - Flask-Login
  - Flask-WTF

- **Frontend**
  - Bootstrap 5
  - Bootstrap Icons
  - Chart.js
  - jQuery

- **Database**
  - PostgreSQL 12+

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/MOHAMEDHAMED1S/Devmenu-managment
cd subscription-manager
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the project root with the following variables:
```env
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/subscription_db
SECRET_KEY=your-secret-key-here
```

5. **Set up the database**
```bash
# Create the database
psql -U postgres -c "CREATE DATABASE subscription_db;"

# Initialize migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Run the application**
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Database Schema

### Users Table
- id (Primary Key)
- restaurant_name
- email
- password_hash
- created_at
- updated_at

### Subscriptions Table
- id (Primary Key)
- user_id (Foreign Key)
- restaurant_name
- email
- website_url
- website_username
- website_password
- subscription_price
- subscription_term
- payment_method
- status
- created_at
- updated_at
- expiration_date

## Development

### Running Tests
```bash
python -m pytest
```

### Code Style
The project follows PEP 8 guidelines. Use flake8 for linting:
```bash
flake8 app
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 