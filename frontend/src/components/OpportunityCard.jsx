import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  Bookmark, 
  ArrowRight, 
  CheckCircle, 
  AlertCircle, 
  ShieldCheck, 
  MapPin, 
  Sparkles,
  Building2
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

export const OpportunityCard = ({ 
  opportunity, 
  matchScore, 
  matchStatus, 
  passedCriteria = [], 
  failedCriteria = [],
  missingFields = [],
  onBookmarkToggle 
}) => {
  const { user } = useAuth();
  const [isSaved, setIsSaved] = useState(opportunity.isSaved || false);
  const [saving, setSaving] = useState(false);

  const handleBookmark = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!user) {
      alert("Please sign in to bookmark schemes.");
      return;
    }
    setSaving(true);
    try {
      if (isSaved) {
        await api.unsaveOpportunity(opportunity.id);
        setIsSaved(false);
      } else {
        await api.saveOpportunity(opportunity.id);
        setIsSaved(true);
      }
      if (onBookmarkToggle) onBookmarkToggle(opportunity.id, !isSaved);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const getCategoryColor = (cat) => {
    switch (cat) {
      case 'FARMER': return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'STUDENT': return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'WOMEN': return 'bg-pink-50 text-pink-700 border-pink-200';
      case 'ENTREPRENEUR': return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'JOB_SEEKER': return 'bg-indigo-50 text-indigo-700 border-indigo-200';
      default: return 'bg-slate-50 text-slate-700 border-slate-200';
    }
  };

  const getMatchBadge = () => {
    if (matchScore === undefined && !matchStatus) return null;
    if (matchStatus === 'HIGH_MATCH' || matchScore >= 80) {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
          <Sparkles className="w-3 h-3 text-emerald-600" />
          {matchScore}% Match
        </span>
      );
    }
    if (matchStatus === 'MODERATE_MATCH' || matchScore >= 50) {
      return (
        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-300">
          {matchScore}% Moderate
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-50 text-rose-700 border border-rose-200">
        Review Criteria
      </span>
    );
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 hover:border-brand-400 hover:shadow-lg hover:shadow-brand-500/5 transition-all duration-200 flex flex-col justify-between group overflow-hidden">
      <div className="p-5">
        
        {/* Top Badges */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className={`text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-md border ${getCategoryColor(opportunity.category)}`}>
              {opportunity.category?.replace('_', ' ') || 'SCHEME'}
            </span>

            <span className="text-[11px] font-medium px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 flex items-center gap-1">
              <Building2 className="w-3 h-3" />
              {opportunity.governmentLevel || 'CENTRAL'}
            </span>

            {opportunity.state && (
              <span className="text-[11px] font-medium px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 flex items-center gap-1">
                <MapPin className="w-3 h-3 text-red-500" />
                {opportunity.state}
              </span>
            )}
          </div>

          <button
            onClick={handleBookmark}
            disabled={saving}
            className={`p-2 rounded-xl border transition-colors cursor-pointer ${
              isSaved 
                ? 'bg-amber-50 text-amber-600 border-amber-200' 
                : 'text-slate-400 hover:text-amber-500 hover:bg-slate-50 border-slate-200'
            }`}
            title={isSaved ? "Saved to your list" : "Save scheme"}
          >
            <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-amber-500' : ''}`} />
          </button>
        </div>

        {/* Title */}
        <div className="flex items-start gap-3 mb-2">
          {opportunity.icon && (
            <span className="text-2xl p-2 rounded-xl bg-slate-50 border border-slate-100 shadow-sm">
              {opportunity.icon}
            </span>
          )}
          <div className="flex-1">
            <h3 className="font-bold text-base text-slate-900 group-hover:text-brand-600 transition-colors line-clamp-2">
              {opportunity.name}
            </h3>
            {matchScore !== undefined && (
              <div className="mt-1">
                {getMatchBadge()}
              </div>
            )}
          </div>
        </div>

        {/* Short Description */}
        <p className="text-xs text-slate-600 line-clamp-3 mb-4 leading-relaxed">
          {opportunity.shortDescription || opportunity.description}
        </p>

        {/* Benefits Highlight */}
        {opportunity.benefitAmount && (
          <div className="mb-3 p-2.5 rounded-xl bg-emerald-50/70 border border-emerald-100 text-emerald-900 text-xs font-semibold flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            <span className="line-clamp-1">{opportunity.benefitAmount}</span>
          </div>
        )}

        {/* Match reasons if provided */}
        {passedCriteria.length > 0 && (
          <div className="mb-2 text-[11px] text-emerald-700 bg-emerald-50/50 p-2 rounded-lg border border-emerald-100/70 space-y-1">
            <div className="flex items-center gap-1 font-semibold">
              <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
              Eligible because:
            </div>
            <p className="line-clamp-1 pl-4.5 text-slate-600">
              {passedCriteria[0]}
            </p>
          </div>
        )}

        {failedCriteria.length > 0 && (
          <div className="mb-2 text-[11px] text-rose-700 bg-rose-50/50 p-2 rounded-lg border border-rose-100/70 space-y-1">
            <div className="flex items-center gap-1 font-semibold">
              <AlertCircle className="w-3.5 h-3.5 text-rose-600" />
              Note:
            </div>
            <p className="line-clamp-1 pl-4.5 text-slate-600">
              {failedCriteria[0]}
            </p>
          </div>
        )}

      </div>

      {/* Card Footer */}
      <div className="px-5 py-3.5 bg-slate-50/80 border-t border-slate-100 flex items-center justify-between">
        <span className="text-[11px] text-slate-500 font-medium">
          {opportunity.verificationStatus === 'VERIFIED' ? '✓ Official Verified' : 'Government Scheme'}
        </span>
        <Link
          to={`/schemes/${opportunity.id}`}
          className="text-xs font-bold text-brand-600 hover:text-brand-800 flex items-center gap-1 group/btn"
        >
          View Details
          <ArrowRight className="w-3.5 h-3.5 group-hover/btn:translate-x-1 transition-transform" />
        </Link>
      </div>

    </div>
  );
};
