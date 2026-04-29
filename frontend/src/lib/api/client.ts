import axios, { type AxiosInstance, type AxiosError, type InternalAxiosRequestConfig } from 'axios';
import { API_ENDPOINTS } from './endpoints';

const getBaseURL = (): string => {
  if (typeof window !== 'undefined') {
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
  }
  return 'http://localhost:8000/api/v1';
};

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: getBaseURL(),
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        // Add auth token if needed in future
        // if (typeof window !== 'undefined') {
        //   const token = localStorage.getItem('token');
        //   if (token && config.headers) {
        //     config.headers.Authorization = `Bearer ${token}`;
        //   }
        // }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        // Centralized error handling
        console.error('API Error:', error.response?.data || error.message);

        // You can add custom error handling logic here
        // For example, redirect to login on 401, show toast on 409, etc.

        return Promise.reject(error);
      }
    );
  }

  get<T = unknown>(url: string, config?: InternalAxiosRequestConfig) {
    return this.client.get<T>(url, config);
  }

  post<T = unknown, D = unknown>(url: string, data?: D, config?: InternalAxiosRequestConfig) {
    return this.client.post<T>(url, data, config);
  }

  patch<T = unknown, D = unknown>(url: string, data?: D, config?: InternalAxiosRequestConfig) {
    return this.client.patch<T>(url, data, config);
  }

  delete<T = unknown>(url: string, config?: InternalAxiosRequestConfig) {
    return this.client.delete<T>(url, config);
  }
}

export const apiClient = new ApiClient();
export default apiClient;
