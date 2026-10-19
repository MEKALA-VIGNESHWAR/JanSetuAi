import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  Search, 
  Filter, 
  RotateCcw, 
  Compass, 
  ChevronLeft, 
  ChevronRight,
  Building2,
  MapPin,
  Sparkles
} from 'lucide-react';
import { api } from '../services/api';
import { OpportunityCard } from '../components/OpportunityCard';

export const SchemesExplorerPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const [schemes, setSchemes] = useState([]);
  const [totalPages, setTotalPages] = useState(1);
  const [totalElements, setTotalElements] = useState(0);
  const [loading, setLoading] = useState(true);

  // Filters state initialized from URL query params
  const [category, setCategory] = useState(searchParams.get('category') || 'ALL');
  const [type, setType] = useState(searchParams.get('type') || 'ALL');
  const [govtLevel, setGovtLevel] = useState(searchParams.get('govtLevel') || 'ALL');
  const [state, setState] = useState(searchParams.get('state') || 'ALL');
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [page, setPage] = useState(0);

  const categories = [
    { id: 'ALL', label: 'All Categories' },
    { id: 'FARMER', label: 'Farmers & Agri' },
    { id: 'STUDENT', label: 'Students & Education' },
    { id: 'WOMEN', label: 'Women & Maternity' },
    { id: 'ENTREPRENEUR', label: 'MSME & Business' },
    { id: 'JOB_SEEKER', label: 'Jobs & Skills' },
    { id: 'GENERAL', label: 'General Welfare' }
  ];

  const types = [
    { id: 'ALL', label: 'All Types' },
    { id: 'SCHEME', label: 'Welfare Schemes' },
    { id: 'SCHOLARSHIP', label: 'Scholarships' },
    { id: 'SUBSIDY', label: 'Subsidies' },
    { id: 'LOAN', label: 'Credit & Loans' },
    { id: 'TRAINING', label: 'Skill Training' }
  ];

  const states = [
    { id: 'ALL', label: 'All India & States' },
    { id: 'Telangana', label: 'Telangana' },
    { id: 'Andhra Pradesh', label: 'Andhra Pradesh' },
    { id: 'Karnataka', label: 'Karnataka' },
    { id: 'Maharashtra', label: 'Maharashtra' }
  ];

  const fetchSchemes = async () => {
    setLoading(true);
    try {
      const data = await api.getOpportunities({
        category,
        type,
        govtLevel,
        state,
        search,
        page,
        size: 12
      });

      if (data && data.content) {
        setSchemes(data.content);
        setTotalPages(data.totalPages);
        setTotalElements(data.totalElements);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSchemes();
  }, [category, type, govtLevel, state, page]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(0);
    fetchSchemes();
  };

  const handleResetFilters = () => {
    setCategory('ALL');
    setType('ALL');
    setGovtLevel('ALL');
    setState('ALL');
    setSearch('');
    setPage(0);
    setSearchParams({});
  };

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-1.5 text-xs font-bold text-brand-600 uppercase tracking-wider mb-1">
              <Compass className="w-4 h-4" />
              Comprehensive Welfare Catalog
            </div>
            <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
              Government Schemes & Opportunities Explorer
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Browse 70+ verified central and state initiatives with official application guides.
            </p>
          </div>

          <button
            onClick={handleResetFilters}
            className="text-xs font-semibold text-slate-500 hover:text-slate-800 flex items-center gap-1.5 px-3 py-2 rounded-xl bg-white border border-slate-200 shadow-sm w-fit cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reset Filters
          </button>
        </div>

        {/* Filter & Search Bar */}
        <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-sm space-y-4">
          
          {/* Keyword Search */}
          <form onSubmit={handleSearchSubmit} className="flex gap-2">
            <div className="flex-1 relative">
              <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search by scheme name, keywords, benefits (e.g. 'Rythu', 'Kalyana', 'Mudra', 'Aadhaar')..."
                className="w-full text-xs pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-brand-500"
              />
            </div>
            <button
              type="submit"
              className="px-6 py-2.5 rounded-xl text-xs font-bold bg-brand-600 hover:bg-brand-700 text-white transition-colors cursor-pointer"
            >
              Search
            </button>
          </form>

          {/* Quick Category Chips */}
          <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pt-1">
            {categories.map((c) => (
              <button
                key={c.id}
                onClick={() => { setCategory(c.id); setPage(0); }}
                className={`whitespace-nowrap px-3.5 py-1.5 rounded-xl text-xs font-bold border transition-colors cursor-pointer ${
                  category === c.id
                    ? 'bg-brand-600 text-white border-brand-600 shadow-sm'
                    : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                }`}
              >
                {c.label}
              </button>
            ))}
          </div>

          {/* Dropdown Filters (Type, Govt Level, State) */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 border-t border-slate-100 text-xs">
            <div>
              <label className="block text-[11px] font-bold text-slate-500 mb-1">Benefit Type</label>
              <select
                value={type}
                onChange={(e) => { setType(e.target.value); setPage(0); }}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 bg-white"
              >
                {types.map(t => (
                  <option key={t.id} value={t.id}>{t.label}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-bold text-slate-500 mb-1">Government Level</label>
              <select
                value={govtLevel}
                onChange={(e) => { setGovtLevel(e.target.value); setPage(0); }}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 bg-white"
              >
                <option value="ALL">All Levels (Central & State)</option>
                <option value="CENTRAL">Central Government Only</option>
                <option value="STATE">State Government Only</option>
              </select>
            </div>

            <div>
              <label className="block text-[11px] font-bold text-slate-500 mb-1">Target State</label>
              <select
                value={state}
                onChange={(e) => { setState(e.target.value); setPage(0); }}
                className="w-full px-3 py-2 rounded-xl border border-slate-300 bg-white"
              >
                {states.map(s => (
                  <option key={s.id} value={s.id}>{s.label}</option>
                ))}
              </select>
            </div>
          </div>

        </div>

        {/* Results Counter */}
        <div className="flex items-center justify-between text-xs text-slate-500 px-1">
          <span>Found <strong className="text-slate-900 font-bold">{totalElements}</strong> matching schemes</span>
          <span>Page {page + 1} of {Math.max(1, totalPages)}</span>
        </div>

        {/* Schemes Grid */}
        {loading ? (
          <div className="text-center py-20 text-slate-400 text-xs">
            <Sparkles className="w-8 h-8 text-brand-500 animate-spin mx-auto mb-2" />
            Loading opportunities catalog...
          </div>
        ) : schemes.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-3xl border border-slate-200">
            <Compass className="w-12 h-12 text-slate-300 mx-auto mb-2" />
            <h3 className="text-base font-bold text-slate-800">No schemes found matching criteria</h3>
            <p className="text-xs text-slate-500 mt-1">Try relaxing some filters or changing your search terms.</p>
            <button
              onClick={handleResetFilters}
              className="mt-4 px-4 py-2 rounded-xl text-xs font-bold bg-brand-600 text-white cursor-pointer"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {schemes.map((opp) => (
              <OpportunityCard key={opp.id} opportunity={opp} />
            ))}
          </div>
        )}

        {/* Pagination Bar */}
        {totalPages > 1 && (
          <div className="flex items-center justify-center gap-2 pt-6">
            <button
              onClick={() => setPage(Math.max(0, page - 1))}
              disabled={page === 0}
              className="p-2 rounded-xl border border-slate-300 bg-white disabled:opacity-40 text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <span className="text-xs font-bold text-slate-700 px-4 py-2 bg-white rounded-xl border border-slate-200">
              {page + 1} / {totalPages}
            </span>
            <button
              onClick={() => setPage(Math.min(totalPages - 1, page + 1))}
              disabled={page >= totalPages - 1}
              className="p-2 rounded-xl border border-slate-300 bg-white disabled:opacity-40 text-slate-700 hover:bg-slate-50 transition-colors cursor-pointer"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        )}

      </div>
    </div>
  );
};
