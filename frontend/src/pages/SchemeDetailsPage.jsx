import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  ExternalLink, 
  Bookmark, 
  CheckCircle2, 
  ShieldCheck, 
  FileText, 
  Building2, 
  MapPin, 
  Clock, 
  AlertTriangle, 
  Bot, 
  Share2,
  Calendar,
  Layers,
  ChevronRight
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

export const SchemeDetailsPage = ({ onOpenAiChat }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isSaved, setIsSaved] = useState(false);
  const [trackingStatus, setTrackingStatus] = useState('INTERESTED');
  const [trackingNotes, setTrackingNotes] = useState('');
  const [trackingSaved, setTrackingSaved] = useState(false);
  
  // Feedback Modal
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  const [feedbackType, setFeedbackType] = useState('ELIGIBILITY_CHANGED');
  const [feedbackDesc, setFeedbackDesc] = useState('');
  const [feedbackSuccess, setFeedbackSuccess] = useState(false);

  useEffect(() => {
    const loadScheme = async () => {
      try {
        const data = await api.getOpportunityById(id);
        setScheme(data);
        setIsSaved(data.isSaved || false);
        if (data.applicationStatus) {
          setTrackingStatus(data.applicationStatus);
          setTrackingSaved(true);
        }
      } catch (err) {
        console.error('Failed to load scheme', err);
      } finally {
        setLoading(false);
      }
    };
    loadScheme();
  }, [id]);

  const handleToggleSave = async () => {
    if (!user) {
      alert("Please sign in to save schemes.");
      return;
    }
    try {
      if (isSaved) {
        await api.unsaveOpportunity(scheme.id);
        setIsSaved(false);
      } else {
        await api.saveOpportunity(scheme.id);
        setIsSaved(true);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleTrackSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      alert("Please sign in to track scheme applications.");
      return;
    }
    try {
      await api.trackOpportunity({
        opportunityId: scheme.id,
        status: trackingStatus,
        notes: trackingNotes,
        appliedDate: new Date().toISOString().split('T')[0]
      });
      setTrackingSaved(true);
      alert('Application tracking updated successfully!');
    } catch (err) {
      console.error(err);
    }
  };

  const handleFeedbackSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.submitFeedback({
        opportunityId: scheme.id,
        feedbackType,
        description: feedbackDesc
      });
      setFeedbackSuccess(true);
      setTimeout(() => {
        setFeedbackOpen(false);
        setFeedbackSuccess(false);
        setFeedbackDesc('');
      }, 1500);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-slate-400 text-xs">
        Loading verified scheme details...
      </div>
    );
  }

  if (!scheme) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4">
        <h2 className="text-lg font-bold text-slate-800">Scheme Not Found</h2>
        <Link to="/schemes" className="text-xs text-brand-600 font-bold mt-2 hover:underline">
          &larr; Back to all schemes
        </Link>
      </div>
    );
  }

  // Parse required documents if stored as JSON or string
  let parsedDocuments = [];
  try {
    if (scheme.requiredDocuments) {
      parsedDocuments = typeof scheme.requiredDocuments === 'string' && scheme.requiredDocuments.startsWith('[')
        ? JSON.parse(scheme.requiredDocuments)
        : [scheme.requiredDocuments];
    }
  } catch {
    parsedDocuments = [scheme.requiredDocuments];
  }

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-6">
        
        {/* Breadcrumb / Back button */}
        <Link
          to="/schemes"
          className="inline-flex items-center gap-1.5 text-xs font-bold text-slate-600 hover:text-brand-600 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to schemes catalog
        </Link>

        {/* Main Header Banner */}
        <div className="bg-white rounded-3xl border border-slate-200 shadow-md p-6 sm:p-8">
          
          <div className="flex flex-col md:flex-row md:items-start justify-between gap-6">
            <div className="space-y-3 flex-1">
              
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs font-bold px-3 py-1 rounded-lg bg-brand-50 text-brand-700 border border-brand-200 uppercase tracking-wider">
                  {scheme.category?.replace('_', ' ') || 'SCHEME'}
                </span>
                <span className="text-xs font-medium px-2.5 py-1 rounded-lg bg-slate-100 text-slate-600 flex items-center gap-1">
                  <Building2 className="w-3.5 h-3.5" />
                  {scheme.governmentLevel} GOVERNMENT
                </span>
                {scheme.state && (
                  <span className="text-xs font-medium px-2.5 py-1 rounded-lg bg-slate-100 text-slate-600 flex items-center gap-1">
                    <MapPin className="w-3.5 h-3.5 text-red-500" />
                    {scheme.state}
                  </span>
                )}
                <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  {scheme.verificationStatus || 'VERIFIED'}
                </span>
              </div>

              <div className="flex items-start gap-4">
                {scheme.icon && (
                  <div className="text-3xl p-3 rounded-2xl bg-slate-50 border border-slate-100 shadow-sm flex-shrink-0">
                    {scheme.icon}
                  </div>
                )}
                <div>
                  <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 leading-tight">
                    {scheme.name}
                  </h1>
                  {scheme.officialSource && (
                    <p className="text-xs text-slate-500 mt-1 font-medium">
                      Administered by: {scheme.officialSource}
                    </p>
                  )}
                </div>
              </div>

            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2.5 flex-wrap sm:flex-nowrap">
              <button
                onClick={handleToggleSave}
                className={`px-4 py-2.5 rounded-xl border text-xs font-bold flex items-center gap-1.5 transition-colors cursor-pointer ${
                  isSaved
                    ? 'bg-amber-50 text-amber-700 border-amber-300'
                    : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                }`}
              >
                <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-amber-500' : ''}`} />
                {isSaved ? 'Saved' : 'Save Scheme'}
              </button>

              {scheme.applicationUrl && (
                <a
                  href={scheme.applicationUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold text-xs shadow-md shadow-brand-500/20 flex items-center gap-1.5 transition-all"
                >
                  Apply on Official Portal
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>
          </div>

          {/* Benefits Callout */}
          {scheme.benefitAmount && (
            <div className="mt-6 p-4 rounded-2xl bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200 text-emerald-950 flex items-center gap-3">
              <div className="p-2 rounded-xl bg-emerald-600 text-white shadow-sm flex-shrink-0">
                <CheckCircle2 className="w-5 h-5" />
              </div>
              <div>
                <p className="text-[11px] font-bold text-emerald-800 uppercase tracking-wider">Entitlement Benefit</p>
                <p className="text-sm font-extrabold text-emerald-950 mt-0.5">{scheme.benefitAmount}</p>
              </div>
            </div>
          )}

        </div>

        {/* Content Columns */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Main Info (2 Cols) */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Overview & Description */}
            <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 space-y-4">
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <FileText className="w-5 h-5 text-brand-600" />
                Scheme Overview
              </h2>
              <p className="text-xs sm:text-sm text-slate-700 leading-relaxed whitespace-pre-line">
                {scheme.description}
              </p>

              {scheme.benefits && (
                <div className="pt-4 border-t border-slate-100">
                  <h3 className="text-xs font-bold text-slate-900 mb-2">Key Entitlements & Coverage:</h3>
                  <p className="text-xs text-slate-600 leading-relaxed whitespace-pre-line">
                    {scheme.benefits}
                  </p>
                </div>
              )}
            </div>

            {/* Eligibility Criteria Breakdown */}
            <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 space-y-4">
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-emerald-600" />
                Eligibility Criteria & Requirements
              </h2>
              
              {scheme.eligibilitySummary && (
                <p className="text-xs text-slate-700 font-medium bg-slate-50 p-3 rounded-xl border border-slate-200/60">
                  {scheme.eligibilitySummary}
                </p>
              )}

              {/* Dynamic Rule items */}
              {scheme.eligibilityRules && scheme.eligibilityRules.length > 0 ? (
                <div className="space-y-2.5 pt-2">
                  <h4 className="text-xs font-bold text-slate-800">Rule Engine Checks:</h4>
                  {scheme.eligibilityRules.map((rule, rIdx) => (
                    <div 
                      key={rIdx} 
                      className="p-3 rounded-xl border border-slate-200 flex items-start gap-3 bg-white"
                    >
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
                      <div className="text-xs">
                        <span className="font-bold text-slate-800">
                          {rule.description || `${rule.ruleField} ${rule.ruleOperator} ${rule.ruleValue}`}
                        </span>
                        <span className="block text-[11px] text-slate-500 mt-0.5">
                          {rule.isMandatory ? 'Mandatory Rule' : 'Optional Criterion'} • Field: {rule.ruleField}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : null}

              {/* Age / Gender Constraints */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 text-xs">
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <span className="text-slate-500 block text-[11px]">Age Restriction:</span>
                  <span className="font-bold text-slate-800">
                    {scheme.minAge || scheme.maxAge ? `${scheme.minAge || 0} to ${scheme.maxAge || 100} Years` : 'No Age Limits'}
                  </span>
                </div>
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <span className="text-slate-500 block text-[11px]">Gender:</span>
                  <span className="font-bold text-slate-800">{scheme.genderRestriction || 'All Genders'}</span>
                </div>
              </div>
            </div>

            {/* Application Steps */}
            {scheme.applicationSteps && (
              <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 space-y-4">
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Layers className="w-5 h-5 text-indigo-600" />
                  How to Apply (Official Process)
                </h2>
                <div className="text-xs text-slate-700 leading-relaxed whitespace-pre-line bg-slate-50 p-4 rounded-2xl border border-slate-200/60">
                  {scheme.applicationSteps}
                </div>
              </div>
            )}

          </div>

          {/* Right Sidebar (1 Col) */}
          <div className="space-y-6">
            
            {/* Required Documents Checklist */}
            <div className="bg-white rounded-3xl border border-slate-200 p-6 space-y-3.5">
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-brand-600" />
                Required Documents
              </h3>
              <p className="text-[11px] text-slate-500">Keep these originals and photocopies ready before applying:</p>

              <div className="space-y-2 pt-1">
                {parsedDocuments.length > 0 ? (
                  parsedDocuments.map((doc, dIdx) => (
                    <div key={dIdx} className="flex items-center gap-2 text-xs text-slate-700 p-2 rounded-lg bg-slate-50 border border-slate-100">
                      <span className="w-1.5 h-1.5 rounded-full bg-brand-500"></span>
                      <span>{doc}</span>
                    </div>
                  ))
                ) : (
                  <>
                    <div className="flex items-center gap-2 text-xs text-slate-700 p-2 rounded-lg bg-slate-50">
                      <span className="w-1.5 h-1.5 rounded-full bg-brand-500"></span>
                      Aadhaar Card (Identity & Address Proof)
                    </div>
                    <div className="flex items-center gap-2 text-xs text-slate-700 p-2 rounded-lg bg-slate-50">
                      <span className="w-1.5 h-1.5 rounded-full bg-brand-500"></span>
                      Bank Passbook (Aadhaar Seeded)
                    </div>
                    <div className="flex items-center gap-2 text-xs text-slate-700 p-2 rounded-lg bg-slate-50">
                      <span className="w-1.5 h-1.5 rounded-full bg-brand-500"></span>
                      Income / Caste Certificate (if applicable)
                    </div>
                  </>
                )}
              </div>
            </div>

            {/* Application Progress Tracker Box */}
            <div className="bg-white rounded-3xl border border-slate-200 p-6 space-y-3.5">
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                Track In My Dashboard
              </h3>
              <p className="text-[11px] text-slate-500">Record your submission status to stay organized:</p>

              <form onSubmit={handleTrackSubmit} className="space-y-3 text-xs">
                <div>
                  <label className="block text-[11px] font-bold text-slate-600 mb-1">Status</label>
                  <select
                    value={trackingStatus}
                    onChange={(e) => setTrackingStatus(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 bg-white"
                  >
                    <option value="INTERESTED">Interested / Planning</option>
                    <option value="DOCUMENTS_COLLECTED">Documents Collected</option>
                    <option value="APPLIED">Applied / Submitted</option>
                    <option value="UNDER_REVIEW">Under Department Review</option>
                    <option value="APPROVED">Approved & Sanctioned</option>
                  </select>
                </div>

                <div>
                  <label className="block text-[11px] font-bold text-slate-600 mb-1">Notes / Acknowledgement No.</label>
                  <input
                    type="text"
                    value={trackingNotes}
                    onChange={(e) => setTrackingNotes(e.target.value)}
                    placeholder="e.g. Ack No: TS2026/9871"
                    className="w-full px-3 py-2 rounded-xl border border-slate-300"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-black text-white font-bold text-xs cursor-pointer transition-colors"
                >
                  {trackingSaved ? 'Update Tracking Status' : 'Add to Application Tracker'}
                </button>
              </form>
            </div>

            {/* Discrepancy & AI Advisor triggers */}
            <div className="space-y-2">
              <button
                onClick={onOpenAiChat}
                className="w-full py-3 px-4 rounded-2xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-sm cursor-pointer"
              >
                <Bot className="w-4 h-4" />
                Ask AI Advisor About This Scheme
              </button>

              <button
                onClick={() => setFeedbackOpen(true)}
                className="w-full py-2.5 px-4 rounded-2xl border border-slate-200 hover:bg-slate-50 text-slate-600 font-semibold text-xs flex items-center justify-center gap-1.5 cursor-pointer"
              >
                <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
                Report Inaccurate Info or Broken Link
              </button>
            </div>

          </div>

        </div>

      </div>

      {/* Discrepancy Feedback Modal */}
      {feedbackOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-200">
            <h3 className="text-base font-bold text-slate-900 mb-1">Report Discrepancy</h3>
            <p className="text-xs text-slate-500 mb-4">
              Help us maintain 100% integrity across government schemes.
            </p>

            {feedbackSuccess ? (
              <div className="p-4 rounded-2xl bg-emerald-50 text-emerald-800 text-xs text-center font-bold">
                ✓ Thank you! Your report has been submitted for verification.
              </div>
            ) : (
              <form onSubmit={handleFeedbackSubmit} className="space-y-3.5 text-xs">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Issue Type</label>
                  <select
                    value={feedbackType}
                    onChange={(e) => setFeedbackType(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300"
                  >
                    <option value="ELIGIBILITY_CHANGED">Eligibility criteria has changed</option>
                    <option value="LINK_BROKEN">Official portal link is broken/down</option>
                    <option value="SCHEME_INACTIVE">Scheme is discontinued or expired</option>
                    <option value="INCORRECT_INFO">Incorrect benefit or document listed</option>
                    <option value="OTHER">Other inquiry</option>
                  </select>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Details & Official Source URL</label>
                  <textarea
                    rows={3}
                    required
                    value={feedbackDesc}
                    onChange={(e) => setFeedbackDesc(e.target.value)}
                    placeholder="Describe the discrepancy or paste the updated official government gazette link..."
                    className="w-full px-3 py-2 rounded-xl border border-slate-300"
                  />
                </div>

                <div className="flex items-center justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setFeedbackOpen(false)}
                    className="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 cursor-pointer"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white font-bold cursor-pointer"
                  >
                    Submit Report
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

    </div>
  );
};
