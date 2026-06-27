# Expense Tracker Application

A modern full-stack expense tracking application built with React, TypeScript, FastAPI, and SQLite.

## Features

- **User Authentication**: Secure registration and login system
- **Expense Management**: Add, edit, and delete expenses
- **Monthly Dashboard**: Visual analytics with charts
- **Category Filtering**: Filter expenses by category and date
- **Responsive UI**: Mobile-friendly design with Tailwind CSS
- **Real-time Updates**: Instant data synchronization

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for development and building
- Tailwind CSS for styling
- React Router for navigation
- Recharts for data visualization
- Axios for API communication
- Lucide React for icons

### Backend
- FastAPI with Python
- SQLAlchemy for ORM
- SQLite for database
- JWT for authentication
- Bcrypt for password hashing

## Project Structure

```
expense-tracker/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database configuration
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── auth.py              # Authentication logic
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py          # Authentication routes
│   │       └── expenses.py      # Expense CRUD routes
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout.tsx       # Main layout component
│   │   │   └── ExpenseForm.tsx  # Expense form component
│   │   ├── pages/
│   │   │   ├── Login.tsx        # Login page
│   │   │   ├── Register.tsx     # Registration page
│   │   │   ├── Dashboard.tsx    # Dashboard with charts
│   │   │   └── Expenses.tsx     # Expense management page
│   │   ├── hooks/
│   │   │   └── useAuth.tsx      # Authentication context
│   │   ├── types/
│   │   │   └── index.ts         # TypeScript type definitions
│   │   ├── utils/
│   │   │   └── api.ts           # API utility functions
│   │   ├── App.tsx              # Main App component
│   │   ├── main.tsx             # Entry point
│   │   └── index.css            # Global styles
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
└── README.md
```

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user and get access token

### Expenses
- `GET /expenses` - Get all expenses (with optional filtering)
- `POST /expenses` - Create a new expense
- `GET /expenses/{id}` - Get a specific expense
- `PUT /expenses/{id}` - Update an expense
- `DELETE /expenses/{id}` - Delete an expense
- `GET /expenses/categories/list` - Get all expense categories
- `GET /expenses/summary/monthly` - Get monthly expense summary

## Usage

1. **Register/Login**: Create an account or login to existing account
2. **Dashboard**: View expense analytics and monthly trends
3. **Add Expenses**: Click "Add Expense" to add new transactions
4. **Manage Expenses**: Edit or delete existing expenses
5. **Filter**: Use filters to view expenses by category and date
6. **Analytics**: View charts and spending patterns on the dashboard

## Development

### Backend Development
- FastAPI auto-generates API documentation at `http://localhost:8000/docs`
- SQLite database file will be created automatically as `expense_tracker.db`

### Frontend Development
- Vite provides hot module replacement for fast development
- TypeScript ensures type safety throughout the application
- Tailwind CSS classes are used for responsive design

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
