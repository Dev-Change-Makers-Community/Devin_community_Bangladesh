export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface Expense {
  id: number;
  title: string;
  description?: string;
  amount: number;
  category: string;
  date: string;
  owner_id: number;
  created_at: string;
  updated_at?: string;
}

export interface ExpenseCreate {
  title: string;
  description?: string;
  amount: number;
  category: string;
  date: string;
}

export interface ExpenseUpdate {
  title?: string;
  description?: string;
  amount?: number;
  category?: string;
  date?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface MonthlySummary {
  month: number;
  total: number;
}
