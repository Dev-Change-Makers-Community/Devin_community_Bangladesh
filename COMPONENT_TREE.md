# Expense Tracker - Component Tree & Structure

## 🌳 Frontend Component Hierarchy

```
App
├── AuthProvider
│   ├── Context: {user, login, logout, register, isLoading}
│   └── Provides authentication state to all children
│
└── Router (BrowserRouter)
    ├── Routes
    │   ├── /login → PublicRoute → Login
    │   │   ├── Form: {username, password, error, loading}
    │   │   ├── Validation: Required fields, password visibility
    │   │   └── Navigation: Link to /register
    │   │
    │   ├── /register → PublicRoute → Register
    │   │   ├── Form: {username, email, password, confirmPassword}
    │   │   ├── Validation: Password match, email format, required fields
    │   │   └── Navigation: Link to /login
    │   │
    │   └── / → ProtectedRoute → Layout
    │       ├── Navigation Header
    │       │   ├── Logo + App Title
    │       │   ├── Nav Links: [Dashboard, Expenses]
    │       │   └── Logout Button
    │       │
    │       └── Main Content (Outlet)
    │           ├── /dashboard → Dashboard
    │           │   ├── Stats Cards: [Total, This Month, Transactions]
    │           │   ├── Year Selector
    │           │   ├── Charts:
    │           │   │   ├── LineChart: Monthly Trend
    │           │   │   └── PieChart: Category Breakdown
    │           │   └── Data Hooks: useExpenses, useMonthlySummary
    │           │
    │           └── /expenses → Expenses
    │               ├── Header: [Title, Add Expense Button]
    │               ├── Filter Bar
    │               │   ├── Category Selector
    │               │   ├── Month Selector
    │               │   └── Year Selector
    │               │
    │               ├── Expenses Table
    │               │   ├── Columns: [Date, Title, Category, Amount, Actions]
    │               │   ├── Row Actions: [Edit, Delete]
    │               │   └── Empty State: No expenses found
    │               │
    │               └── Modal (Conditional)
    │                   └── ExpenseForm
    │                       ├── Form Fields: [Title, Description, Amount, Category, Date]
    │                       ├── Validation: Required fields, amount > 0
    │                       └── Actions: [Cancel, Submit]
```

## 🎨 Component Breakdown

### 1. **App Component** (`App.tsx`)
```typescript
App
├── AuthProvider
├── Router
├── PublicRoute (HOC)
├── ProtectedRoute (HOC)
└── Routes Configuration
```

**Responsibilities:**
- Application entry point
- Global state provider setup
- Route configuration
- Authentication guards

### 2. **Authentication Components**

#### **Login** (`pages/Login.tsx`)
```typescript
Login
├── State: {username, password, showPassword, error, loading}
├── Form Handler: handleSubmit()
├── Input Fields: [Username, Password]
├── Error Display
└── Navigation Link: Register
```

#### **Register** (`pages/Register.tsx`)
```typescript
Register
├── State: {username, email, password, confirmPassword, showPassword, error, loading}
├── Form Handler: handleSubmit()
├── Validation: validateForm()
├── Input Fields: [Username, Email, Password, Confirm Password]
├── Error Display
└── Navigation Link: Login
```

#### **AuthProvider** (`hooks/useAuth.tsx`)
```typescript
AuthProvider
├── Context: AuthContext
├── State: {user, isLoading}
├── Methods: {login, register, logout}
└── Token Management: localStorage
```

### 3. **Layout Component** (`components/Layout.tsx`)
```typescript
Layout
├── Navigation Header
│   ├── Logo & Title
│   ├── Nav Links
│   │   ├── Dashboard Link
│   │   └── Expenses Link
│   └── Logout Button
└── Main Content Outlet
```

### 4. **Dashboard Component** (`pages/Dashboard.tsx`)
```typescript
Dashboard
├── State: {expenses, monthlySummary, loading, selectedYear}
├── Effects: [fetchData, filterByYear]
├── Stats Section
│   ├── Total Expenses Card
│   ├── This Month Card
│   └── Transactions Card
├── Year Selector
└── Charts Section
    ├── LineChart (Monthly Trend)
    └── PieChart (Category Breakdown)
```

### 5. **Expenses Component** (`pages/Expenses.tsx`)
```typescript
Expenses
├── State: {
│   expenses, categories, filteredExpenses,
│   loading, showForm, editingExpense,
│   selectedCategory, selectedMonth, selectedYear
│   }
├── Effects: [fetchExpenses, fetchCategories, filterExpenses]
├── Header Section
│   ├── Page Title
│   └── Add Expense Button
├── Filter Bar
│   ├── Category Filter
│   ├── Month Filter
│   └── Year Filter
├── Expenses Table
│   ├── Table Headers
│   ├── Expense Rows
│   └── Empty State
└── ExpenseForm Modal
```

### 6. **ExpenseForm Component** (`components/ExpenseForm.tsx`)
```typescript
ExpenseForm
├── Props: {expense?, onSubmit, onCancel}
├── State: {formData, errors}
├── Effects: [populateFormForEdit]
├── Form Fields
│   ├── Title Input
│   ├── Description Textarea
│   ├── Amount Input
│   ├── Category Select
│   └── Date Input
├── Validation: validateForm()
└── Actions: [Cancel, Submit]
```

## 🔗 Data Flow Between Components

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           COMPONENT DATA FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────────────┘

AuthProvider (Global)
       │ Provides auth state
       ▼
┌─────────────┐    JWT Token    ┌─────────────┐    API Calls    ┌─────────────┐
│   Layout    │ ◄──────────────► │ Dashboard   │ ◄──────────────► │   API       │
│             │                 │             │                 │   Client    │
│ Navigation  │                 │ Charts      │                 │             │
└─────────────┘                 └─────────────┘                 └─────────────┘
       │                                 │                                 │
       │ Routes                          │                                 │
       ▼                                 ▼                                 ▼
┌─────────────┐                 ┌─────────────┐                 ┌─────────────┐
│   Login     │                 │  Expenses   │                 │  ExpenseForm│
│   Register  │                 │             │                 │             │
└─────────────┘                 └─────────────┘                 └─────────────┘
```

## 🎯 Component Responsibilities

### **Presentation Components**
- **Layout**: Navigation and page structure
- **ExpenseForm**: Form validation and submission
- **Charts**: Data visualization (Dashboard children)

### **Container Components**
- **Dashboard**: Data fetching and state management for analytics
- **Expenses**: Expense CRUD operations and filtering
- **Login/Register**: Authentication forms and user interaction

### **Utility Components**
- **AuthProvider**: Global authentication state
- **API Client**: HTTP request handling and error management
- **Route Guards**: Authentication-based routing

## 🔄 State Management Pattern

```
Global State (AuthProvider)
├── user: User | null
├── login: (username, password) => Promise<void>
├── register: (username, email, password) => Promise<void>
├── logout: () => void
└── isLoading: boolean

Component Local State
├── formData: Form data
├── errors: Validation errors
├── loading: Loading states
└── filters: Filter values

Server State (API)
├── expenses: Expense[]
├── categories: string[]
└── summaries: MonthlySummary[]
```

## 📱 Responsive Breakpoints

```
Mobile (sm):    640px+
Tablet (md):    768px+
Desktop (lg):   1024px+
Large (xl):     1280px+

Component Adaptations:
├── Navigation: Hamburger menu on mobile
├── Tables: Horizontal scroll on mobile
├── Charts: Responsive sizing
└── Forms: Full width on mobile
```

This component tree provides a clear understanding of the frontend architecture, showing how data flows through the application and how components are organized and related to each other.
