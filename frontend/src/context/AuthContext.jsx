import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('jansetu_token');
      if (token) {
        try {
          const userData = await api.getCurrentUser();
          setUser(userData);
          const profileData = await api.getProfile();
          setProfile(profileData);
        } catch {
          localStorage.removeItem('jansetu_token');
          setUser(null);
          setProfile(null);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    const res = await api.login({ email, password });
    localStorage.setItem('jansetu_token', res.token);
    setUser({ id: res.userId, email: res.email, role: res.role });
    try {
      const profileData = await api.getProfile();
      setProfile(profileData);
    } catch {
      // profile will load upon update
    }
    return res;
  };

  const register = async (email, password, fullName) => {
    const res = await api.register({ email, password, fullName });
    localStorage.setItem('jansetu_token', res.token);
    setUser({ id: res.userId, email: res.email, role: res.role });
    try {
      const profileData = await api.getProfile();
      setProfile(profileData);
    } catch {
      // profile will load upon update
    }
    return res;
  };

  const logout = () => {
    localStorage.removeItem('jansetu_token');
    setUser(null);
    setProfile(null);
  };

  const refreshProfile = async () => {
    try {
      const updated = await api.getProfile();
      setProfile(updated);
      return updated;
    } catch {
      return null;
    }
  };

  return (
    <AuthContext.Provider value={{ user, profile, loading, login, register, logout, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
