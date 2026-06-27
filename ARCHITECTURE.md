# Expense Tracker - Project Architecture & Organization

## 🏗️ High-Level Architecture

```
┌─────────────────┐    HTTP/HTTPS    ┌─────────────────┐    SQLAlchemy    ┌─────────────────┐
│                 │ ◄──────────────► │                 │ ◄──────────────► │                 │
│   Frontend      │                  │    Backend      │                  │    Database     │
│   (React)       │                  │   (FastAPI)     │                  │   (SQLite)      │
│                 │                  │                 │                  │                 │
│ Port: 5173      │                  │ Port: 8000      │                  │ File: .db       │
└─────────────────┘                  └─────────────────┘                  └─────────────────┘
```

## 📁 Project Structure Overview

```
expense-tracker/
├── 📁 backend/                    # FastAPI Python Backend
│   ├── 📁 app/
│   │   ├── 🐍 main.py            # FastAPI application entry point
│   │   ├── 🐍 database.py        # Database connection & session
│   │   ├── 🐍 models.py          # SQLAlchemy ORM models
│   │   ├── 🐍 schemas.py         # Pydantic data validation
│   │   ├── 🐍 auth.py            # JWT authentication logic
│   │   └── 📁 routes/            # API route handlers
│   │       ├── 🐍 auth.py        # Authentication endpoints
│   │       └── 🐍 expenses.py    # Expense CRUD endpoints
│   └── 📄 requirements.txt       # Python dependencies
│
├── 📁 frontend/                   # React TypeScript Frontend
│   ├── 📁 src/
│   │   ├── ⚛️ App.tsx           # Main React application
│   │   ├── ⚛️ main.tsx          # Application entry point
│   │   ├── 📁 components/        # Reusable UI components
│   │   │   ├── ⚛️ Layout.tsx    # Main layout with navigation
│   │   │   └── ⚛️ ExpenseForm.tsx # Expense creation/editing form
│   │   ├── 📁 pages/            # Page-level components
│   │   │   ├── ⚛️ Login.tsx     # User login page
│   │   │   ├── ⚛️ Register.tsx  # User registration page
│   │   │   ├── ⚛️ Dashboard.tsx # Analytics dashboard
│   │   │   └── ⚛️ Expenses.tsx  # Expense management page
│   │   ├── 📁 hooks/            # Custom React hooks
│   │   │   └── ⚛️ useAuth.tsx   # Authentication state management
│   │   ├── 📁 utils/            # Utility functions
│   │   │   └── ⚛️ api.ts        # API client with axios
│   │   └── 📁 types/            # TypeScript type definitions
│   │       └── ⚛️ index.ts      # Shared interfaces
│   ├── 📄 package.json          # Node.js dependencies
│   └── ⚙️ vite.config.ts        # Vite build configuration
│
└── 📄 README.md                 # Project documentation
```

## 🔐 Authentication Flow

```
┌─────────────┐    1. Login Request    ┌─────────────┐    2. Validate Credentials    ┌─────────────┐
│             │ ◄─────────────────── │             │ ◄────────────────────────── │             │
│   Frontend  │                      │   Backend   │                              │   Database  │
│             │                      │             │                              │             │
│  (React)    │                      │ (FastAPI)   │                              │  (SQLite)   │
└─────────────┘                      └─────────────┘                              └─────────────┘
       │                                     │                                           │
       │ 3. JWT Token                         │ 4. User Record                          │
       │    Return                           │    Fetch                                │
       │─────────────────────────────────────▶│───────────────────────────────────────▶│
       │                                     │                                           │
       │                                     │ 5. User Data                            │
       │                                     │    Return                               │
       │◀─────────────────────────────────────│◀────────────────────────────────────────│
       │                                     │                                           │
       │ 6. Store JWT                         │                                           │
       │    in localStorage                  │                                           │
       │                                     │                                           │
┌─────────────┐                      ┌─────────────┐                              ┌─────────────┐
│   Frontend  │                      │   Backend   │                              │   Database  │
│             │                      │             │                              │             │
│ Authenticated│                      │   Ready     │                              │   Storage   │
└─────────────┘                      └─────────────┘                              └─────────────┘
```

## 🌐 API Data Flow

### Authentication Endpoints
```
POST /auth/register
┌─────────────┐    User Data          ┌─────────────┐    Create User       ┌─────────────┐
│   Frontend  │ ◄─────────────────── │   Backend   │ ◄────────────────── │   Database  │
│             │                      │             │                     │             │
│  Register   │                      │ Validate &  │                     │   Users     │
│   Form      │                      │  Hash Pwd   │                     │   Table     │
└─────────────┘                      └─────────────┘                     └─────────────┘

POST /auth/login
┌─────────────┐    Credentials        ┌─────────────┐    Verify User       ┌─────────────┐
│   Frontend  │ ◄─────────────────── │   Backend   │ ◄────────────────── │   Database  │
│             │                      │             │                     │             │
│  Login      │                      │ Issue JWT   │                     │   Users     │
│   Form      │                      │   Token     │                     │   Table     │
└─────────────┘                      └─────────────┘                     └─────────────┘
```

### Expense Management Endpoints
```
GET /expenses
┌─────────────┐    Request + JWT      ┌─────────────┐    Query Expenses    ┌─────────────┐
│   Frontend  │ ◄─────────────────── │   Backend   │ ◄────────────────── │   Database  │
│             │                      │             │                     │             │
│  Dashboard  │                      │ Filter &    │                     │  Expenses   │
│  Expenses   │                      │  Return     │                     │   Table     │
└─────────────┘                      └─────────────┘                     └─────────────┘

POST /expenses
┌─────────────┐    Expense Data       ┌─────────────┐    Create Expense    ┌─────────────┐
│   Frontend  │ ◄─────────────────── │   Backend   │ ◄────────────────── │   Database  │
│             │                      │             │                     │             │
│  Expense    │                      │ Validate &  │                     │  Expenses   │
│   Form      │                      │   Save      │                     │   Table     │
└─────────────┘                      └─────────────┘                     └─────────────┘
```

## 🗄️ Database Schema

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                SQLite Database                                      │
│                                expense_tracker.db                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐         ┌─────────────────────┐
│      users          │         │     expenses        │
├─────────────────────┤         ├─────────────────────┤
│ id (PK)             │◄────────┤ owner_id (FK)       │
│ username (UNIQUE)   │         │ id (PK)             │
│ email (UNIQUE)      │         │ title               │
│ hashed_password     │         │ description         │
│ created_at          │         │ amount              │
└─────────────────────┘         │ category            │
                              │ date                │
                              │ created_at          │
                              │ updated_at          │
                              └─────────────────────┘

Relationship: One User → Many Expenses
```

## 🎨 Frontend Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    React App                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ App.tsx                                                                              │
│ ├─ AuthProvider (Context)                                                           │
│ ├─ Router (React Router)                                                            │
│ │  ├─ PublicRoute (Login/Register)                                                  │
│ │  └─ ProtectedRoute (Dashboard/Expenses)                                           │
│ │     └─ Layout                                                                     │
│ │        ├─ Navigation                                                              │
│ │        └─ Outlet (Page Content)                                                   │
│ │           ├─ Dashboard                                                            │
│ │           └─ Expenses                                                             │
│ │              ├─ ExpenseList                                                       │
│ │              └─ ExpenseForm (Modal)                                               │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔧 Technology Stack Details

### Backend Technologies
```
🐍 FastAPI (0.104.1)
├── 🚀 High-performance async web framework
├── 📚 Automatic API documentation (Swagger/OpenAPI)
├── 🔒 Built-in data validation with Pydantic
└── 🌐 CORS support for frontend integration

🗄️ SQLAlchemy (2.0.23)
├── 🏗️ ORM for database operations
├── 🔗 Relationship management
└── 📊 Database-agnostic queries

🔐 JWT Authentication
├── 🎫 python-jose for token handling
├── 🔑 passlib for password hashing
└── 🛡️ bcrypt for secure password storage

📦 Additional Libraries
├── 🌊 uvicorn (ASGI server)
├── 📋 python-multipart (form data)
├── 🌍 python-dotenv (environment variables)
└── ✅ pydantic (data validation)
```

### Frontend Technologies
```
⚛️ React 18 + TypeScript
├── 🏗️ Component-based architecture
├── 🔒 Type safety
├── 🎣 Custom hooks for state management
└── ⚡ Concurrent features

🎨 Tailwind CSS (3.3.6)
├── 🎯 Utility-first CSS framework
├── 📱 Responsive design utilities
├── 🎨 Consistent design system
└── ⚡ Optimized production builds

🛣️ React Router (6.20.1)
├── 📍 Declarative routing
├── 🛡️ Route protection
└── 🔄 Navigation management

📊 Recharts (2.8.0)
├── 📈 Data visualization
├── 🎨 Interactive charts
└── 📱 Responsive chart components

🔧 Development Tools
├── ⚡ Vite (fast build tool)
├── 🔍 ESLint (code linting)
├── 🎯 TypeScript (type checking)
└── 🌐 Axios (HTTP client)
```

## 🔄 Data Flow Summary

1. **User Authentication**
   - Frontend sends credentials to `/auth/login`
   - Backend validates against database
   - JWT token issued and stored in localStorage
   - Subsequent requests include Authorization header

2. **Expense Management**
   - Frontend requests data with JWT token
   - Backend validates token and extracts user info
   - Database queries filtered by user_id
   - Response data rendered in React components

3. **Real-time Updates**
   - State changes trigger API calls
   - Backend updates database
   - Frontend refetches data and re-renders
   - UI reflects latest data instantly

This architecture provides a solid foundation for the expense tracking application with clear separation of concerns, type safety, and scalable design patterns.
