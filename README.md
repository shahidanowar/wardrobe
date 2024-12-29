# Digital Wardrobe Application

A smart wardrobe management system that helps users organize their clothing and receive AI-powered outfit recommendations.

## Features

- User authentication and profile management
- Image upload for clothing items
- AI-powered clothing categorization
- Outfit recommendations based on occasions
- Responsive dashboard interface
- Admin panel for system management

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python Flask
- Database: SQLite
- ML: TensorFlow
- Authentication: Flask-Login

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

4. Run the application:
```bash
flask run
```

## Project Structure

```
digital_wardrobe/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/
│   ├── templates/
│   ├── models/
│   ├── routes/
│   └── ml_models/
├── migrations/
├── instance/
├── tests/
├── config.py
├── run.py
└── requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///wardrobe.db
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

MIT License
