import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Sparkles, 
  User, 
  Bookmark, 
  CheckCircle2, 
  Menu, 
  X, 
  LogOut, 
  Compass, 
  LayoutDashboard,
  Bot
} from 'lucide-react';

export const Navbar = ({ onOpenAiChat, onOpenAuthModal }) => {
  const { user, profile, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200">
      <div className="tricolor-bar w-full"></div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-700 to-brand-500 flex items-center justify-center text-white shadow-md shadow-brand-500/20 group-hover:scale-105 transition-transform">
              <span className="text-xl font-black">JS</span>
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight text-slate-900 group-hover:text-brand-600 transition-colors">
                Jan<span className="text-brand-600">Setu</span> <span className="text-xs px-2 py-0.5 rounded-full bg-saffron-500/10 text-saffron-600 font-semibold border border-saffron-500/20">AI</span>
              </span>
              <p className="text-[10px] text-slate-500 font-medium leading-none tracking-wider uppercase">Citizen Welfare Gateway</p>
            </div>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1">
            <Link
              to="/schemes"
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
                isActive('/schemes') 
                  ? 'bg-brand-50 text-brand-700 font-semibold' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Compass className="w-4 h-4" />
              Find Schemes
            </Link>

            <Link
              to="/questionnaire"
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
                isActive('/questionnaire') 
                  ? 'bg-brand-50 text-brand-700 font-semibold' 
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Sparkles className="w-4 h-4 text-brand-500" />
              Check Eligibility
            </Link>

            {user && (
              <>
                <Link
                  to="/dashboard"
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
                    isActive('/dashboard') 
                      ? 'bg-brand-50 text-brand-700 font-semibold' 
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <LayoutDashboard className="w-4 h-4" />
                  My Matches
                </Link>

                <Link
                  to="/tracking"
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
                    isActive('/tracking') 
                      ? 'bg-brand-50 text-brand-700 font-semibold' 
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  Tracker
                </Link>

                <Link
                  to="/saved"
                  className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5 ${
                    isActive('/saved') 
                      ? 'bg-brand-50 text-brand-700 font-semibold' 
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Bookmark className="w-4 h-4 text-amber-500" />
                  Saved
                </Link>
              </>
            )}
          </nav>

          {/* Right Action buttons */}
          <div className="hidden md:flex items-center gap-3">
            <button
              onClick={onOpenAiChat}
              className="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-sm hover:shadow-md hover:from-blue-700 hover:to-indigo-700 transition-all flex items-center gap-1.5 cursor-pointer"
            >
              <Bot className="w-4 h-4 animate-pulse" />
              AI Assistant
            </button>

            {user ? (
              <div className="flex items-center gap-2 border-l border-slate-200 pl-3">
                <Link
                  to="/dashboard"
                  className="flex items-center gap-2 p-1 rounded-lg hover:bg-slate-100 transition-colors"
                >
                  <div className="w-8 h-8 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center font-bold text-xs border border-slate-300">
                    {profile?.fullName ? profile.fullName.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
                  </div>
                  <div className="text-left hidden lg:block">
                    <p className="text-xs font-semibold text-slate-800 leading-none">
                      {profile?.fullName || user.email.split('@')[0]}
                    </p>
                    <p className="text-[10px] text-emerald-600 font-medium">
                      {profile?.profileCompletion || 0}% Profile
                    </p>
                  </div>
                </Link>
                <button
                  onClick={() => {
                    logout();
                    navigate('/');
                  }}
                  title="Sign out"
                  className="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors cursor-pointer"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <button
                onClick={onOpenAuthModal}
                className="px-4 py-2 rounded-lg text-sm font-medium bg-brand-600 text-white hover:bg-brand-700 transition-colors shadow-sm cursor-pointer"
              >
                Sign In / Register
              </button>
            )}
          </div>

          {/* Mobile menu trigger */}
          <div className="flex md:hidden items-center gap-2">
            <button
              onClick={onOpenAiChat}
              className="p-2 text-brand-600 hover:bg-brand-50 rounded-lg"
              title="AI Assistant"
            >
              <Bot className="w-5 h-5" />
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-slate-600 hover:bg-slate-100 rounded-lg"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 pt-2 pb-6 space-y-1">
          <Link
            to="/schemes"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2.5 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
          >
            Find Schemes
          </Link>
          <Link
            to="/questionnaire"
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2.5 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
          >
            Check Eligibility
          </Link>
          {user ? (
            <>
              <Link
                to="/dashboard"
                onClick={() => setMobileMenuOpen(false)}
                className="block px-3 py-2.5 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
              >
                My Matches & Profile
              </Link>
              <Link
                to="/tracking"
                onClick={() => setMobileMenuOpen(false)}
                className="block px-3 py-2.5 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
              >
                Application Tracker
              </Link>
              <Link
                to="/saved"
                onClick={() => setMobileMenuOpen(false)}
                className="block px-3 py-2.5 rounded-lg text-base font-medium text-slate-700 hover:bg-slate-50"
              >
                Saved Schemes
              </Link>
              <button
                onClick={() => {
                  logout();
                  setMobileMenuOpen(false);
                }}
                className="w-full text-left px-3 py-2.5 rounded-lg text-base font-medium text-red-600 hover:bg-red-50"
              >
                Sign Out
              </button>
            </>
          ) : (
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onOpenAuthModal();
              }}
              className="w-full mt-2 text-center py-2.5 px-4 rounded-lg bg-brand-600 text-white font-medium shadow"
            >
              Sign In / Register
            </button>
          )}
        </div>
      )}
    </header>
  );
};
