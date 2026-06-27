# Expense Tracker - Visual Flow Diagrams

## 🔄 Complete Application Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERACTION FLOW                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    1. Visit App    ┌─────────────┐    2. Check Auth     ┌─────────────┐
│             │ ──────────────────► │             │ ──────────────────► │             │
│    User     │                    │  Frontend   │                    │ localStorage│
│   Browser   │                    │   (React)   │                    │             │
└─────────────┘                    └─────────────┘                    └─────────────┘
       │                                   │                                   │
       │                                   │ 3. No Token Found?               │
       │                                   │─────────────────────────────────►│
       │                                   │                                   │
       │                                   │ 4. Redirect to Login              │
       │                                   │                                   │
       ▼                                   ▼                                   ▼
┌─────────────┐    5. Show Login    ┌─────────────┐    6. Submit Form    ┌─────────────┐
│             │ ◄────────────────── │             │ ◄────────────────── │             │
│ Login Page  │                    │  Frontend   │                    │   User      │
│             │                    │             │                    │   Input     │
└─────────────┘                    └─────────────┘                    └─────────────┘
       │                                   │                                   │
       │ 7. Send to API                     │                                   │
       │─────────────────────────────────────┼─────────────────────────────────────│
       │                                   │                                   │
       ▼                                   ▼                                   ▼
┌─────────────┐    8. Validate      ┌─────────────┐    9. Check User     ┌─────────────┐
│             │ ◄────────────────── │             │ ◄────────────────── │             │
│   Backend   │                    │   Backend   │                    │   Database  │
│  (FastAPI)  │                    │  (Auth)     │                    │  (SQLite)   │
└─────────────┘                    └─────────────┘                    └─────────────┘
       │                                   │                                   │
       │ 10. Issue JWT                      │                                   │
       │─────────────────────────────────────┼─────────────────────────────────────│
       │                                   │                                   │
       ▼                                   ▼                                   ▼
┌─────────────┐    11. Store JWT     ┌─────────────┐    12. Show          ┌─────────────┐
│             │ ◄────────────────── │             │ ◄────────────────── │             │
│localStorage │                    │  Frontend   │                    │ Dashboard   │
│             │                    │             │                    │             │
└─────────────┘                    └─────────────┘                    └─────────────┘
```

## 🔐 Authentication Flow (Detailed)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            AUTHENTICATION SEQUENCE                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘

REGISTRATION FLOW:
┌─────────────┐
│   User      │
│             │ 1. Fill Registration Form
└─────────────┘
       │
       ▼
┌─────────────┐    2. POST /auth/register    ┌─────────────┐
│  Frontend   │ ──────────────────────────► │   Backend   │
│             │                              │             │
│  {username, │                              │ Validate:   │
│   email,    │                              │ - Email uniq │
│  password}  │                              │ - User uniq │
└─────────────┘                              │ - Hash pwd  │
       │                                     └─────────────┘
       │ 3. Success/Error Response                 │
       │◀─────────────────────────────────────────┘
       ▼
┌─────────────┐
│  Show Result│
│  (Login or  │
│   Error)    │
└─────────────┘

LOGIN FLOW:
┌─────────────┐
│   User      │
│             │ 1. Fill Login Form
└─────────────┘
       │
       ▼
┌─────────────┐    2. POST /auth/login       ┌─────────────┐    3. Query User   ┌─────────────┐
│  Frontend   │ ──────────────────────────► │   Backend   │ ──────────────────► │   Database  │
│             │                              │             │                     │             │
│  {username, │                              | Validate:   │                     │   users     │
│  password}  │                              │ - Find user │                     │   table     │
└─────────────┘                              │ - Verify pwd│                     └─────────────┘
       │                                     └─────────────┘                             │
       │ 4. JWT Token or Error                     │                               5. User Data
       │◀─────────────────────────────────────────┘                               │
       ▼                                                                             │
┌─────────────┐                                                                      │
│ Store JWT   │                                                                      │
│ in localStorage│                                                                     │
└─────────────┘                                                                      │
       │                                                                             │
       │                                                                             ▼
       │                                                                   ┌─────────────┐
       │◀──────────────────────────────────────────────────────────────────────│   Return    │
       │                                                                   │   User      │
       ▼                                                                   │   Record    │
┌─────────────┐                                                          └─────────────┘
│ Redirect to │
│ Dashboard   │
└─────────────┘
```

## 💰 Expense Management Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           EXPENSE CRUD OPERATIONS                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘

CREATE EXPENSE:
┌─────────────┐    1. Fill Form       ┌─────────────┐    2. POST /expenses   ┌─────────────┐
│   User      │ ───────────────────► │  Frontend   │ ────────────────────► │   Backend   │
│             │                      │             │                      │             │
│  Expense    │                      │ + JWT Token │                      │ Validate:   │
│   Details   │                      │             │                      │ - Auth user │
└─────────────┘                      └─────────────┘                      │ - Validate  │
       │                                     │                          │   data      │
       │ 3. Success/Error Response            │                          └─────────────┘
       │◀─────────────────────────────────────┘                                   │
       ▼                                                                         │ 4. Save to DB
┌─────────────┐                                                                │
│  Update UI  │                                                                │
│ (Add to list)│                                                               │
└─────────────┘                                                                ▼
                                                                         ┌─────────────┐
                                                                         │   Database  │
                                                                         │             │
                                                                         │  expenses   │
                                                                         │   table     │
                                                                         └─────────────┘

READ EXPENSES:
┌─────────────┐    1. Load Page       ┌─────────────┐    2. GET /expenses   ┌─────────────┐
│   User      │ ───────────────────► │  Frontend   │ ────────────────────► │   Backend   │
│             │                      │             │                      │             │
│  Dashboard  │                      │ + JWT Token │                      │ Filter by:  │
│  or List    │                      │ + Params    │                      │ - user_id   │
└─────────────┘                      └─────────────┘                      │ - category  │
       │                                     │                          │ - date      │
       │ 3. Expense List                     │                          └─────────────┘
       │◀─────────────────────────────────────┘                                   │
       ▼                                                                         │ 4. Query DB
┌─────────────┐                                                                │
│  Display    │                                                                │
│  Expenses   │                                                                ▼
└─────────────┘                                                    ┌─────────────┐
                                                                     │   Database  │
                                                                     │             │
                                                                     │  expenses   │
                                                                     │   table     │
                                                                     └─────────────┘

UPDATE EXPENSE:
┌─────────────┐    1. Click Edit      ┌─────────────┐    2. PUT /expenses/  ┌─────────────┐
│   User      │ ───────────────────► │  Frontend   │ ────────────────────► │   Backend   │
│             │                      │             │        {id}           │             │
│  Modify     │                      │ + JWT Token │                      │ Validate:   │
│  Expense    │                      │ + New Data  │                      │ - Ownership │
└─────────────┘                      └─────────────┘                      │ - Update DB │
       │                                     │                          └─────────────┘
       │ 3. Updated Expense                  │                                   │
       │◀─────────────────────────────────────┘                                   │
       ▼                                                                         │ 4. Save Changes
┌─────────────┐                                                                │
│  Update UI  │                                                                │
│ (Replace in │                                                                │
│    list)    │                                                                ▼
└─────────────┘                                                    ┌─────────────┐
                                                                     │   Database  │
                                                                     │             │
                                                                     │  expenses   │
                                                                     │   table     │
                                                                     └─────────────┘

DELETE EXPENSE:
┌─────────────┐    1. Click Delete    ┌─────────────┐    2. DELETE /expenses/ ┌─────────────┐
│   User      │ ───────────────────► │  Frontend   │ ────────────────────► │   Backend   │
│             │                      │             │         {id}           │             │
│  Confirm    │                      │ + JWT Token │                      │ Validate:   │
│  Delete     │                      │             │                      │ - Ownership │
└─────────────┘                      └─────────────┘                      │ - Delete DB │
       │                                     │                          └─────────────┘
       │ 3. Success Message                  │                                   │
       │◀─────────────────────────────────────┘                                   │
       ▼                                                                         │ 4. Remove from DB
┌─────────────┐                                                                │
│  Remove from│                                                                │
│     UI      │                                                                ▼
└─────────────┘                                                    ┌─────────────┐
                                                                     │   Database  │
                                                                     │             │
                                                                     │  expenses   │
                                                                     │   table     │
                                                                     └─────────────┘
```

## 📊 Data Visualization Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           DASHBOARD DATA FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    1. Load Dashboard   ┌─────────────┐    2. Multiple API Calls   ┌─────────────┐
│   User      │ ───────────────────► │  Frontend   │ ──────────────────────────► │   Backend   │
│             │                      │             │                           │             │
│  Visits     │                      │ Dashboard   │ ├─ GET /expenses           │             │
│ Dashboard   │                      │ Component   │ ├─ GET /expenses/summary/ │             │
└─────────────┘                      └─────────────┘ │   monthly                 └─────────────┘
       │                                     │                           │
       │ 3. Process Data                      │ 4. Aggregate Data        │
       │◀─────────────────────────────────────┼───────────────────────────│
       ▼                                     ▼                           ▼
┌─────────────┐                      ┌─────────────┐              ┌─────────────┐
│  Calculate  │                      │  Query DB   │              │  Return     │
│  Totals     │                      │             │              │  Aggregated │
│  & Charts   │                      │  expenses   │              │   Data      │
└─────────────┘                      │   table     │              └─────────────┘
       │                             └─────────────┘                         │
       │                                     │                               │
       ▼                                     ▼                               │
┌─────────────┐                      ┌─────────────┐                         │
│  Render     │                      │  Group by   │                         │
│  Charts     │                      │  Category/  │                         │
│  (Recharts) │                      │    Month    │                         │
└─────────────┘                      └─────────────┘                         │
       │                                     │                               │
       │                                     │                               │
       ▼                                     ▼                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            INTERACTIVE DASHBOARD                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   Total     │  │   This      │  │  Monthly    │  │  Category   │  │  Expense    │ │
│  │  Expenses   │  │   Month     │  │   Trend     │  │ Breakdown   │  │   List      │ │
│  │   Card      │  │   Card      │  │  (Line)     │  │  (Pie)      │  │  (Table)    │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 State Management Flow

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           REACT STATE MANAGEMENT                                    │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐
│ AuthContext │ ◄─────────────────────────────────────────────────────────────────────┐
│ Provider    │                                                                          │
│             │                                                                          │
│ State:      │                                                                          │
│ - user      │                                                                          │
│ - login()   │                                                                          │
│ - logout()  │                                                                          │
│ - register()│                                                                          │
└─────────────┘                                                                          │
       │                                                                                │
       │ Provides Auth State                                                            │
       ▼                                                                                │
┌─────────────┐                                                                          │
│ App Router  │                                                                          │
│             │                                                                          │
│ Routes:     │                                                                          │
│ - /login    │                                                                          │
│ - /register │                                                                          │
│ - /dashboard│                                                                          │
│ - /expenses │                                                                          │
└─────────────┘                                                                          │
       │                                                                                │
       │ Protected Routes Require Auth                                                  │
       ▼                                                                                │
┌─────────────┐                                                                          │
│ Components  │                                                                          │
│             │                                                                          │
│ Local State:│                                                                          │
│ - formData  │                                                                          │
│ - errors    │                                                                          │
│ - loading   │                                                                          │
│ - filters   │                                                                          │
└─────────────┘                                                                          │
       │                                                                                │
       │ API Calls with JWT                                                             │
       ▼                                                                                │
┌─────────────┐                                                                          │
│   API       │                                                                          │
│   Client    │                                                                          │
│             │                                                                          │
│ Features:   │                                                                          │
│ - Axios     │                                                                          │
│ - Interceptors│                                                                        │
│ - Error     │                                                                          │
│   Handling  │                                                                          │
└─────────────┘                                                                          │
       │                                                                                │
       └──────────────────────────────────────────────────────────────────────────────┘
```

These flow diagrams provide a comprehensive visual understanding of how the Expense Tracker application operates, from user interactions to data persistence.
