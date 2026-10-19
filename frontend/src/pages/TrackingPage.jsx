import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  CheckCircle2, 
  Clock, 
  FileText, 
  ExternalLink, 
  Trash2, 
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Building2
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

export const TrackingPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [trackings, setTrackings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeFilter, setActiveFilter] = useState('ALL');

  useEffect(() => {
    if (!user) {
      navigate('/schemes');
      return;
    }

    const loadTrackings = async () => {
      try {
        const data = await api.getTrackings();
        setTrackings(data || []);
      } catch (err) {
        console.error('Failed to load tracking data', err);
      } finally {
        setLoading(false);
      }
    };

    loadTrackings();
  }, [user, navigate]);

  const handleStatusChange = async (tracking, newStatus) => {
    try {
      await api.trackOpportunity({
        opportunityId: tracking.opportunityId,
        status: newStatus,
        notes: tracking.notes,
        appliedDate: tracking.appliedDate
      });

      setTrackings(prev => prev.map(t => 
        t.id === tracking.id ? { ...t, status: newStatus } : t
      ));
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Remove this scheme from your application tracker?")) return;
    try {
      await api.deleteTracking(id);
      setTrackings(prev => prev.filter(t => t.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'INTERESTED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-100 text-slate-700">Interested</span>;
      case 'DOCUMENTS_COLLECTED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-100 text-blue-800">Docs Collected</span>;
      case 'APPLIED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800">Applied</span>;
      case 'UNDER_REVIEW':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-100 text-purple-800">Under Review</span>;
      case 'APPROVED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">Approved</span>;
      case 'REJECTED':
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-800">Rejected</span>;
      default:
        return <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-slate-100 text-slate-700">{status}</span>;
    }
  };

  const filtered = activeFilter === 'ALL' 
    ? trackings 
    : trackings.filter(t => t.status === activeFilter);

  const counts = {
    INTERESTED: trackings.filter(t => t.status === 'INTERESTED').length,
    DOCUMENTS_COLLECTED: trackings.filter(t => t.status === 'DOCUMENTS_COLLECTED').length,
    APPLIED: trackings.filter(t => t.status === 'APPLIED').length,
    UNDER_REVIEW: trackings.filter(t => t.status === 'UNDER_REVIEW').length,
    APPROVED: trackings.filter(t => t.status === 'APPROVED').length,
  };

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header */}
        <div>
          <div className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-600 uppercase tracking-wider mb-1">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            Citizen Application Tracker
          </div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
            Tracked Scheme Applications
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Keep track of paperwork, submission dates, acknowledgement numbers, and approval statuses.
          </p>
        </div>

        {/* Status Filter Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          {[
            { id: 'ALL', label: 'All Tracked', count: trackings.length },
            { id: 'DOCUMENTS_COLLECTED', label: 'Docs Ready', count: counts.DOCUMENTS_COLLECTED },
            { id: 'APPLIED', label: 'Applied', count: counts.APPLIED },
            { id: 'UNDER_REVIEW', label: 'Under Review', count: counts.UNDER_REVIEW },
            { id: 'APPROVED', label: 'Approved', count: counts.APPROVED },
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveFilter(tab.id)}
              className={`p-3.5 rounded-2xl border text-left transition-all cursor-pointer ${
                activeFilter === tab.id
                  ? 'bg-white border-brand-500 ring-2 ring-brand-500/20 shadow-sm'
                  : 'bg-white/70 border-slate-200 hover:bg-white'
              }`}
            >
              <span className="text-xl font-black text-slate-900 block">{tab.count}</span>
              <span className="text-[11px] font-bold text-slate-500">{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Tracking list */}
        {loading ? (
          <div className="text-center py-20 text-slate-400 text-xs">
            <Sparkles className="w-8 h-8 text-brand-500 animate-spin mx-auto mb-2" />
            Loading your tracked applications...
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-16 bg-white rounded-3xl border border-slate-200">
            <FileText className="w-12 h-12 text-slate-300 mx-auto mb-2" />
            <h3 className="text-base font-bold text-slate-800">No applications in this category</h3>
            <p className="text-xs text-slate-500 mt-1">
              Start tracking any scheme by clicking "Add to Application Tracker" on its details page.
            </p>
            <Link
              to="/schemes"
              className="mt-4 inline-flex items-center gap-1.5 px-5 py-2.5 rounded-xl text-xs font-bold bg-brand-600 text-white shadow-sm"
            >
              Discover Schemes to Apply
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {filtered.map(item => (
              <div 
                key={item.id}
                className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4"
              >
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center gap-2">
                    {getStatusBadge(item.status)}
                    <span className="text-[11px] font-semibold text-slate-500 uppercase">
                      {item.opportunityCategory} • {item.opportunityType}
                    </span>
                  </div>

                  <Link 
                    to={`/schemes/${item.opportunityId}`}
                    className="text-base font-bold text-slate-900 hover:text-brand-600 transition-colors block"
                  >
                    {item.opportunityName}
                  </Link>

                  {item.notes && (
                    <p className="text-xs text-slate-600 bg-slate-50 p-2 rounded-lg border border-slate-100 inline-block">
                      📝 {item.notes}
                    </p>
                  )}

                  {item.appliedDate && (
                    <p className="text-[11px] text-slate-400">
                      Target / Applied Date: {item.appliedDate}
                    </p>
                  )}
                </div>

                {/* Status modifier dropdown & actions */}
                <div className="flex items-center gap-3 self-end md:self-center">
                  <select
                    value={item.status}
                    onChange={(e) => handleStatusChange(item, e.target.value)}
                    className="text-xs font-semibold px-3 py-2 rounded-xl border border-slate-300 bg-white focus:ring-2 focus:ring-brand-500"
                  >
                    <option value="INTERESTED">Interested</option>
                    <option value="DOCUMENTS_COLLECTED">Documents Collected</option>
                    <option value="APPLIED">Applied</option>
                    <option value="UNDER_REVIEW">Under Review</option>
                    <option value="APPROVED">Approved</option>
                    <option value="REJECTED">Rejected</option>
                  </select>

                  {item.applicationUrl && (
                    <a
                      href={item.applicationUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="p-2 text-brand-600 hover:bg-brand-50 rounded-xl transition-colors"
                      title="Open Official Portal"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  )}

                  <button
                    onClick={() => handleDelete(item.id)}
                    className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition-colors cursor-pointer"
                    title="Remove Tracking"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  );
};
