import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Bookmark, Compass, ArrowRight, Sparkles } from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { OpportunityCard } from '../components/OpportunityCard';

export const SavedSchemesPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [savedSchemes, setSavedSchemes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/schemes');
      return;
    }

    const loadSaved = async () => {
      try {
        const data = await api.getSavedOpportunities();
        setSavedSchemes(data || []);
      } catch (err) {
        console.error('Failed to load saved schemes', err);
      } finally {
        setLoading(false);
      }
    };

    loadSaved();
  }, [user, navigate]);

  const handleBookmarkToggle = (opportunityId, isNowSaved) => {
    if (!isNowSaved) {
      setSavedSchemes(prev => prev.filter(s => s.id !== opportunityId));
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-6">
        
        <div>
          <div className="inline-flex items-center gap-1.5 text-xs font-bold text-amber-600 uppercase tracking-wider mb-1">
            <Bookmark className="w-4 h-4 fill-amber-500" />
            Bookmarked Opportunities
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Saved Schemes & Entitlements
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Schemes you have bookmarked for future reference and application.
          </p>
        </div>

        {loading ? (
          <div className="text-center py-20 text-slate-400 text-xs">
            <Sparkles className="w-8 h-8 text-brand-500 animate-spin mx-auto mb-2" />
            Loading saved bookmarks...
          </div>
        ) : savedSchemes.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-3xl border border-slate-200">
            <Bookmark className="w-12 h-12 text-slate-300 mx-auto mb-2" />
            <h3 className="text-base font-bold text-slate-800">No saved schemes yet</h3>
            <p className="text-xs text-slate-500 mt-1">
              You haven't bookmarked any schemes. Explore the catalog to save opportunities you are interested in.
            </p>
            <Link
              to="/schemes"
              className="mt-4 inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl text-xs font-bold bg-brand-600 text-white shadow-sm"
            >
              Browse Schemes Catalog
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {savedSchemes.map((opp) => (
              <OpportunityCard 
                key={opp.id} 
                opportunity={opp} 
                onBookmarkToggle={handleBookmarkToggle}
              />
            ))}
          </div>
        )}

      </div>
    </div>
  );
};
