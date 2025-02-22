# WortWunder - German Vocabulary Learning Platform

WortWunder is a modern web application designed to help users learn German vocabulary efficiently. It features word grouping, themes, and a user-friendly interface for vocabulary management.

## Project Structure

The project consists of two main components:

- `wortwunder-backend-flask/`: Flask-based REST API
- `wortwunder-launchpad/`: React-based frontend application

## Features

- Word group categorization (Basic, Intermediate, Advanced, etc.)
- Theme-based vocabulary organization
- Search functionality
- RESTful API for vocabulary management
- Modern, responsive UI

## Backend Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

```bash
cd wortwunder-backend-flask
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Backend

```bash
python app.py
```

The backend will start on `http://localhost:5001`

## Frontend Setup

### Prerequisites
- Node.js 16 or higher
- npm or yarn

### Installation

```bash
cd wortwunder-launchpad
npm install
# or
yarn install
```

### Running the Frontend

```bash
npm run dev
# or
yarn dev
```

The frontend will start on `http://localhost:5173`

## API Endpoints

- `GET /api/word-groups`: Get all word groups
- `GET /api/vocabulary`: Get vocabulary items (with optional filters)
- `POST /api/vocabulary`: Add new vocabulary items

## Deployment

### Backend Deployment (PythonAnywhere)
1. Create a new web app on PythonAnywhere
2. Upload the backend code
3. Set up a virtual environment
4. Configure WSGI file
5. Update environment variables

### Frontend Deployment (Netlify)
1. Connect your GitHub repository
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Configure environment variables

## Environment Variables

### Backend
No environment variables required for basic setup.

### Frontend
- `VITE_API_URL`: Backend API URL

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
