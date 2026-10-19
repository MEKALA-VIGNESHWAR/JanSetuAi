import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  Search, 
  ShieldCheck, 
  GraduationCap, 
  Tractor, 
  Briefcase, 
  HeartHandshake, 
  Store, 
  ArrowRight, 
  CheckCircle2, 
  TrendingUp, 
  Users,
  Compass
} from 'lucide-react';
import { api } from '../services/api';
import { OpportunityCard } from '../components/OpportunityCard';

export const HomePage = ({ onOpenAiChat }) => {
  const navigate = useNavigate();
  const [featuredSchemes, setFeaturedSchemes] = useState([]);
  const [stats, setStats] = useState({ totalActiveSchemes: 70, totalCategories: 8, totalStatesCovered: 15 });
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRole, setSelectedRole] = useState('STUDENT');

  useEffect(() => {
    const loadHomeData = async () => {
      try {
        const [schemesRes, statsRes] = await Promise.all([
          api.getOpportunities({ size: 6 }),
          api.getStats()
        ]);
        if (schemesRes?.content) {
          setFeaturedSchemes(schemesRes.content);
        }
        if (statsRes) {
          setStats(statsRes);
        }
      } catch (err) {
        console.error('Failed to load home data', err);
      }
    };
    loadHomeData();
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/schemes?search=${encodeURIComponent(searchQuery.trim())}`);
    } else {
      navigate('/schemes');
    }
  };

  const categories = [
    { id: 'FARMER', label: 'Farmers & Agri', icon: Tractor, color: 'text-emerald-600 bg-emerald-50 border-emerald-200' },
    { id: 'STUDENT', label: 'Students & Education', icon: GraduationCap, color: 'text-blue-600 bg-blue-50 border-blue-200' },
    { id: 'WOMEN', label: 'Women Empowerment', icon: HeartHandshake, color: 'text-pink-600 bg-pink-50 border-pink-200' },
    { id: 'ENTREPRENEUR', label: 'Business & Loans', icon: Store, color: 'text-amber-600 bg-amber-50 border-amber-200' },
    { id: 'JOB_SEEKER', label: 'Job Seekers & Skills', icon: Briefcase, color: 'text-indigo-600 bg-indigo-50 border-indigo-200' },
  ];

  return (
    <div className="min-h-screen bg-slate-50">
      
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-brand-900 via-slate-900 to-slate-900 text-white pt-16 pb-24">
        {/* Glow Effects */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-brand-500/20 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-saffron-500/15 rounded-full blur-3xl pointer-events-none"></div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur border border-white/15 text-xs font-semibold text-blue-200 mb-6">
            <Sparkles className="w-4 h-4 text-saffron-500" />
            Empowering 1.4 Billion Citizens With Direct Entitlements
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight max-w-4xl mx-auto leading-tight">
            Discover Government Schemes You <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-sky-300 to-emerald-400">Actually Qualify For</span>
          </h1>

          <p className="mt-5 text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Stop guessing eligibility. JanSetu AI matches your exact profile against verified central and state welfare criteria in seconds.
          </p>

          {/* Quick Search Bar */}
          <form onSubmit={handleSearchSubmit} className="mt-8 max-w-2xl mx-auto">
            <div className="bg-white p-2 rounded-2xl shadow-xl flex items-center gap-2 border border-slate-200/50">
              <div className="pl-3 text-slate-400">
                <Search className="w-5 h-5" />
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search schemes e.g. 'farmer subsidy', 'post-matric', 'mudra loan'..."
                className="flex-1 text-slate-800 placeholder-slate-400 text-sm focus:outline-none py-2"
              />
              <button
                type="submit"
                className="px-6 py-2.5 rounded-xl font-bold text-xs bg-brand-600 hover:bg-brand-700 text-white transition-all shadow-md cursor-pointer"
              >
                Search
              </button>
            </div>
          </form>

          {/* Action CTAs */}
          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <Link
              to="/questionnaire"
              className="px-6 py-3 rounded-xl font-bold text-sm bg-gradient-to-r from-saffron-500 to-saffron-600 hover:from-saffron-600 hover:to-orange-700 text-white shadow-lg shadow-saffron-500/25 flex items-center gap-2 transition-transform hover:-translate-y-0.5"
            >
              <Sparkles className="w-4 h-4" />
              Check My Eligibility (2 Mins)
            </Link>

            <button
              onClick={onOpenAiChat}
              className="px-6 py-3 rounded-xl font-bold text-sm bg-white/10 hover:bg-white/15 text-white border border-white/20 backdrop-blur flex items-center gap-2 transition-colors cursor-pointer"
            >
              Ask AI Assistant
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          {/* Stats Badges */}
          <div className="mt-14 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-4xl mx-auto text-left">
            <div className="bg-white/5 backdrop-blur border border-white/10 p-4 rounded-2xl">
              <p className="text-2xl sm:text-3xl font-extrabold text-white">70+</p>
              <p className="text-xs text-slate-300 font-medium mt-0.5">Verified Schemes</p>
            </div>
            <div className="bg-white/5 backdrop-blur border border-white/10 p-4 rounded-2xl">
              <p className="text-2xl sm:text-3xl font-extrabold text-white">100%</p>
              <p className="text-xs text-slate-300 font-medium mt-0.5">Official & Free</p>
            </div>
            <div className="bg-white/5 backdrop-blur border border-white/10 p-4 rounded-2xl">
              <p className="text-2xl sm:text-3xl font-extrabold text-white">₹0</p>
              <p className="text-xs text-slate-300 font-medium mt-0.5">No Middlemen</p>
            </div>
            <div className="bg-white/5 backdrop-blur border border-white/10 p-4 rounded-2xl">
              <p className="text-2xl sm:text-3xl font-extrabold text-white">28+</p>
              <p className="text-xs text-slate-300 font-medium mt-0.5">States & Central</p>
            </div>
          </div>

        </div>
      </section>

      {/* Categories Navigator */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8 relative z-20">
        <div className="bg-white rounded-2xl shadow-xl border border-slate-200/80 p-4 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          {categories.map((c) => {
            const Icon = c.icon;
            return (
              <button
                key={c.id}
                onClick={() => navigate(`/schemes?category=${c.id}`)}
                className={`p-3.5 rounded-xl border flex items-center gap-3 transition-all text-left hover:scale-[1.02] cursor-pointer ${c.color}`}
              >
                <div className="p-2 rounded-lg bg-white/80 shadow-sm">
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <span className="font-bold text-xs block leading-tight">{c.label}</span>
                  <span className="text-[10px] opacity-75">Explore &rarr;</span>
                </div>
              </button>
            );
          })}
        </div>
      </section>

      {/* Featured Schemes Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex items-end justify-between mb-8">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-brand-600 uppercase tracking-wider mb-1">
              <TrendingUp className="w-4 h-4" />
              Popular Welfare Initiatives
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
              Featured Government Opportunities
            </h2>
          </div>
          <Link
            to="/schemes"
            className="text-xs font-bold text-brand-600 hover:text-brand-800 flex items-center gap-1 group"
          >
            View all 70+ schemes
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredSchemes.map((opp) => (
            <OpportunityCard key={opp.id} opportunity={opp} />
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-white py-16 border-y border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <span className="text-xs font-bold text-brand-600 uppercase tracking-wider">Simple & Transparent</span>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 mt-1">
              How JanSetu AI Works
            </h2>
            <p className="text-xs text-slate-500 mt-2">
              Three simple steps from discovery to application submission
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 relative">
              <div className="w-10 h-10 rounded-xl bg-brand-600 text-white font-black text-base flex items-center justify-center mb-4 shadow">
                1
              </div>
              <h3 className="font-bold text-base text-slate-900 mb-2">Build Your Progressive Profile</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Provide basic details (age, occupation, education, state, income range). We never ask for sensitive credentials or unnecessary information.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 relative">
              <div className="w-10 h-10 rounded-xl bg-brand-600 text-white font-black text-base flex items-center justify-center mb-4 shadow">
                2
              </div>
              <h3 className="font-bold text-base text-slate-900 mb-2">Automated Rule Engine Match</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Our eligibility engine cross-checks official criteria rules (age brackets, income ceilings, land holdings, social categories) and provides transparency scores.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-200 relative">
              <div className="w-10 h-10 rounded-xl bg-brand-600 text-white font-black text-base flex items-center justify-center mb-4 shadow">
                3
              </div>
              <h3 className="font-bold text-base text-slate-900 mb-2">Apply Directly & Track Progress</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Receive official portal links, document checklists, and application steps. Track your submitted applications in your citizen tracker dashboard.
              </p>
            </div>
          </div>

          <div className="mt-12 text-center">
            <Link
              to="/questionnaire"
              className="inline-flex items-center gap-2 px-8 py-3.5 rounded-xl font-bold text-sm bg-brand-600 hover:bg-brand-700 text-white shadow-lg shadow-brand-500/20 transition-all hover:scale-105"
            >
              Start Your Free Eligibility Check
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

    </div>
  );
};
