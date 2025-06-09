# E-Commerce Website

A beautiful and modern e-commerce website built with Flask, featuring a responsive design and essential e-commerce functionality.

## Features

- User authentication (login/register)
- Product browsing and search
- Shopping cart functionality
- Product details with reviews
- Responsive design for all devices
- Modern UI with Bootstrap 5
- SQLite database for data storage

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd e-commerce
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure you're in the project directory and your virtual environment is activated.

2. Run the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
e-commerce/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   ├── login.html     # Login page
│   ├── register.html  # Registration page
│   ├── cart.html      # Shopping cart
│   └── product_detail.html  # Product details
└── instance/         # Instance-specific files
    └── ecommerce.db  # SQLite database
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 