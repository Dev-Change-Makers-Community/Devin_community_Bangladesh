import axios from 'axios';
import { AuthResponse, User, Expense, ExpenseCreate, ExpenseUpdate, MonthlySummary } from '../types';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: async (userData: { username: string; email: string; password: string }): Promise<User> => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  
  login: async (credentials: { username: string; password: string }): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', credentials, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      data: new URLSearchParams(credentials)
    });
    return response.data;
  }
};

export const expensesAPI = {
  getExpenses: async (params?: {
    skip?: number;
    limit?: number;
    category?: string;
    month?: number;
    year?: number;
  }): Promise<Expense[]> => {
    const response = await api.get('/expenses', { params });
    return response.data;
  },
  
  getExpense: async (id: number): Promise<Expense> => {
    const response = await api.get(`/expenses/${id}`);
    return response.data;
  },
  
  createExpense: async (expense: ExpenseCreate): Promise<Expense> => {
    const response = await api.post('/expenses', expense);
    return response.data;
  },
  
  updateExpense: async (id: number, expense: ExpenseUpdate): Promise<Expense> => {
    const response = await api.put(`/expenses/${id}`, expense);
    return response.data;
  },
  
  deleteExpense: async (id: number): Promise<void> => {
    await api.delete(`/expenses/${id}`);
  },
  
  getCategories: async (): Promise<string[]> => {
    const response = await api.get('/expenses/categories/list');
    return response.data;
  },
  
  getMonthlySummary: async (year: number): Promise<MonthlySummary[]> => {
    const response = await api.get('/expenses/summary/monthly', { params: { year } });
    return response.data;
  }
};
