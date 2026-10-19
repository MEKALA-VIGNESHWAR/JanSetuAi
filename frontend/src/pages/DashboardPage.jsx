import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  User, 
  CheckCircle2, 
  AlertCircle, 
  Bookmark, 
  Edit3, 
  TrendingUp, 
  Compass,
  ArrowRight,
  ShieldCheck,
  Building2,
  MapPin
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { OpportunityCard } from '../components/OpportunityCard';

export const DashboardPage = ({ onOpenAiChat }) => {
  const { user, profile } = useAuth();
  const navigate = useNavigate();

  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('ALL'); // ALL, HIGH, PENDING

  useEffect(() => {
    if (!user) {
      navigate('/questionnaire');
      return;
    }

    const loadMatches = async () => {
      try {
        const data = await api.getMatchedSchemes();
        setMatches(data || []);
      } catch (err) {
        console.error('Failed to load matched schemes', err);
      } finally {
        setLoading(false);
      }
    };

    loadMatches();
  }, [user, navigate]);

  const highMatches = matches.filter(m => m.isEligible && m.matchScore >= 75);
  const reviewMatches = matches.filter(m => m.missingFields && m.missingFields.length > 0 && m.isEligible);
  const displayMatches = activeTab === 'HIGH' ? highMatches : (activeTab === 'REVIEW' ? reviewMatches : matches);

  const completion = profile?.profileCompletion || 0;

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Welcome & Citizen Profile Header Banner */}
        <div className="bg-gradient-to-r from-brand-900 via-blue-900 to-indigo-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
          <div className="absolute right-0 bottom-0 translate-x-12 translate-y-12 w-64 h-64 bg-brand-500/10 rounded-full blur-2xl"></div>

          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
            <div>
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 backdrop-blur text-xs font-semibold text-blue-200 mb-3 border border-white/10">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                Verified Citizen Dashboard
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
                Namaste, {profile?.fullName || user?.email.split('@')[0]}!
              </h1>
              <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-xl">
                Here are your personalized government entitlements matched using our deterministic eligibility engine.
              </p>

              {/* Citizen tags */}
              <div className="flex flex-wrap items-center gap-2 mt-4 text-xs font-medium">
                {profile?.occupation && (
                  <span className="px-3 py-1 rounded-lg bg-white/10 backdrop-blur border border-white/15">
                    Role: {profile.occupation}
                  </span>
                )}
                {profile?.state && (
                  <span className="px-3 py-1 rounded-lg bg-white/10 backdrop-blur border border-white/15 flex items-center gap-1">
                    <MapPin className="w-3 h-3 text-red-400" />
                    {profile.state}
                  </span>
                )}
                {profile?.socialCategory && (
                  <span className="px-3 py-1 rounded-lg bg-white/10 backdrop-blur border border-white/15">
                    Category: {profile.socialCategory}
                  </span>
                )}
              </div>
            </div>

            {/* Profile Completion Meter */}
            <div className="bg-white/10 backdrop-blur border border-white/15 p-5 rounded-2xl flex items-center gap-4 min-w-[240px]">
              <div className="relative w-16 h-16 flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    className="text-white/20"
                    strokeWidth="3.5"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path
                    className="text-emerald-400"
                    strokeDasharray={`${completion}, 100`}
                    strokeWidth="3.5"
                    strokeLinecap="round"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                </svg>
                <span className="absolute font-black text-sm text-white">{completion}%</span>
              </div>
              <div>
                <p className="text-xs font-bold text-white">Profile Strength</p>
                <p className="text-[11px] text-slate-300">
                  {completion >= 80 ? 'Optimal for matching' : 'Complete for more matches'}
                </p>
                <Link
                  to="/questionnaire"
                  className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-300 hover:text-emerald-200 mt-1"
                >
                  <Edit3 className="w-3 h-3" /> Update Profile
                </Link>
              </div>
            </div>

          </div>
        </div>

        {/* Quick Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-500">High Probability Matches</p>
              <p className="text-2xl font-extrabold text-emerald-600 mt-1">{highMatches.length}</p>
              <p className="text-[11px] text-slate-400">All mandatory criteria satisfied</p>
            </div>
            <div className="p-3 rounded-xl bg-emerald-50 text-emerald-600">
              <CheckCircle2 className="w-6 h-6" />
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-500">Need Confirmation</p>
              <p className="text-2xl font-extrabold text-amber-600 mt-1">{reviewMatches.length}</p>
              <p className="text-[11px] text-slate-400">Has 1-2 unfilled fields</p>
            </div>
            <div className="p-3 rounded-xl bg-amber-50 text-amber-600">
              <AlertCircle className="w-6 h-6" />
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex items-center justify-between">
            <div>
              <p className="text-xs font-semibold text-slate-500">Total Evaluated</p>
              <p className="text-2xl font-extrabold text-brand-600 mt-1">{matches.length}</p>
              <p className="text-[11px] text-slate-400">Against active schemes</p>
            </div>
            <div className="p-3 rounded-xl bg-blue-50 text-brand-600">
              <Compass className="w-6 h-6" />
            </div>
          </div>
        </div>

        {/* Matches Section with Filter Tabs */}
        <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
            <div>
              <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-brand-600" />
                Your Scheme Recommendations
              </h2>
              <p className="text-xs text-slate-500 mt-0.5">
                Schemes scored according to criteria match with your citizen profile.
              </p>
            </div>

            {/* Tabs */}
            <div className="flex items-center p-1 bg-slate-100 rounded-xl text-xs font-bold">
              <button
                onClick={() => setActiveTab('ALL')}
                className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
                  activeTab === 'ALL' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                All Schemes ({matches.length})
              </button>
              <button
                onClick={() => setActiveTab('HIGH')}
                className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
                  activeTab === 'HIGH' ? 'bg-white text-emerald-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                High Match ({highMatches.length})
              </button>
              <button
                onClick={() => setActiveTab('REVIEW')}
                className={`px-3 py-1.5 rounded-lg transition-colors cursor-pointer ${
                  activeTab === 'REVIEW' ? 'bg-white text-amber-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Needs Review ({reviewMatches.length})
              </button>
            </div>
          </div>

          {loading ? (
            <div className="text-center py-20 text-slate-400 text-xs">
              <Sparkles className="w-8 h-8 text-brand-500 animate-spin mx-auto mb-2" />
              Running real-time rule engine matching...
            </div>
          ) : displayMatches.length === 0 ? (
            <div className="text-center py-16 bg-slate-50 rounded-2xl border border-slate-200">
              <p className="text-sm font-semibold text-slate-700">No schemes found in this category</p>
              <p className="text-xs text-slate-500 mt-1">Try switching tabs or refining your profile answers.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {displayMatches.map((m, idx) => (
                <OpportunityCard
                  key={idx}
                  opportunity={m.opportunity}
                  matchScore={m.matchScore}
                  matchStatus={m.matchStatus}
                  passedCriteria={m.passedCriteria}
                  failedCriteria={m.failedCriteria}
                  missingFields={m.missingFields}
                />
              ))}
            </div>
          )}

        </div>

      </div>
    </div>
  );
};
