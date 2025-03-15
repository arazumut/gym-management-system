"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  image?: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const router = useRouter();

  // Sayfa yüklendiğinde localStorage'dan kullanıcı bilgilerini al
  useEffect(() => {
    const checkAuth = async () => {
      setIsLoading(true);
      try {
        const storedUser = localStorage.getItem('user');
        const accessToken = localStorage.getItem('accessToken');
        
        if (storedUser && accessToken) {
          // Token'ın geçerliliğini kontrol et
          try {
            await axios.post(`${API_BASE_URL}/auth/token/verify/`, {
              token: accessToken
            });
            
            setUser(JSON.parse(storedUser));
            setIsAuthenticated(true);
          } catch (error) {
            // Token geçersiz, refresh token ile yenilemeyi dene
            const newToken = await refreshToken();
            if (!newToken) {
              // Refresh token da geçersiz, kullanıcıyı çıkış yaptır
              logout();
            }
          }
        }
      } catch (error) {
        console.error('Auth check error:', error);
        logout();
      } finally {
        setIsLoading(false);
      }
    };
    
    checkAuth();
  }, []);

  const login = async (username: string, password: string) => {
    setIsLoading(true);
    try {
      console.log('Giriş denemesi:', { username });
      
      const response = await axios.post(`${API_BASE_URL}/auth/token/`, {
        username,
        password,
      });

      console.log('Token yanıtı:', response.data);

      if (response.data.access) {
        localStorage.setItem('accessToken', response.data.access);
        localStorage.setItem('refreshToken', response.data.refresh);
        
        // Kullanıcı bilgilerini al
        const userResponse = await axios.get(`${API_BASE_URL}/users/`, {
          headers: {
            Authorization: `Bearer ${response.data.access}`
          }
        });
        
        console.log('Kullanıcı yanıtı:', userResponse.data);
        
        if (userResponse.data && Array.isArray(userResponse.data)) {
          const foundUser = userResponse.data.find((u: any) => u.email === username);
          if (foundUser) {
            console.log('Kullanıcı bulundu:', foundUser);
            localStorage.setItem('user', JSON.stringify(foundUser));
            setUser(foundUser);
            setIsAuthenticated(true);
          } else {
            console.error('Kullanıcı bulunamadı:', username);
            throw new Error('Kullanıcı bulunamadı');
          }
        } else {
          console.error('Geçersiz kullanıcı yanıtı:', userResponse.data);
          throw new Error('Geçersiz kullanıcı yanıtı');
        }
      }
    } catch (error: any) {
      console.error('Giriş hatası:', error);
      console.error('Hata detayları:', error.response?.data);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    setUser(null);
    setIsAuthenticated(false);
    router.push('/signin');
  };

  const refreshToken = async (): Promise<string | null> => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) return null;

      const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
        refresh: refreshToken
      });

      if (response.data.access) {
        localStorage.setItem('accessToken', response.data.access);
        return response.data.access;
      }
      return null;
    } catch (error) {
      console.error('Token refresh error:', error);
      return null;
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, isAuthenticated, login, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  );
}; 