import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldCheck, Heart, ExternalLink, HelpCircle } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="bg-slate-900 text-slate-400 text-sm mt-20 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold text-sm">
                JS
              </div>
              <span className="text-lg font-bold text-white tracking-tight">JanSetu AI</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Empowering Indian citizens to access government entitlements, subsidies, and scholarships transparently with verifiable criteria and AI assistance.
            </p>
            <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-950/40 border border-emerald-800/40 px-3 py-1.5 rounded-lg w-fit">
              <ShieldCheck className="w-4 h-4" />
              100% Free & Open Public Service
            </div>
          </div>

          <div>
            <h4 className="text-white text-xs font-semibold uppercase tracking-wider mb-4">Discovery Portals</h4>
            <ul className="space-y-2 text-xs">
              <li><Link to="/schemes?category=FARMER" className="hover:text-white transition-colors">Farmer & Agriculture Schemes</Link></li>
              <li><Link to="/schemes?category=STUDENT" className="hover:text-white transition-colors">Student Scholarships & Grants</Link></li>
              <li><Link to="/schemes?category=WOMEN" className="hover:text-white transition-colors">Women Empowerment & Maternity</Link></li>
              <li><Link to="/schemes?category=ENTREPRENEUR" className="hover:text-white transition-colors">Mudra Loans & MSME Subsidies</Link></li>
              <li><Link to="/schemes?state=Telangana" className="hover:text-white transition-colors">Telangana State Initiatives</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-white text-xs font-semibold uppercase tracking-wider mb-4">Citizens Tools</h4>
            <ul className="space-y-2 text-xs">
              <li><Link to="/questionnaire" className="hover:text-white transition-colors">Eligibility Matching Engine</Link></li>
              <li><Link to="/tracking" className="hover:text-white transition-colors">Application Progress Tracker</Link></li>
              <li><Link to="/saved" className="hover:text-white transition-colors">Saved Scheme Bookmarks</Link></li>
              <li><a href="https://myscheme.gov.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-white transition-colors">MyScheme National Portal <ExternalLink className="w-3 h-3" /></a></li>
              <li><a href="https://scholarships.gov.in" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-white transition-colors">National Scholarship Portal <ExternalLink className="w-3 h-3" /></a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-white text-xs font-semibold uppercase tracking-wider mb-4">Integrity & Transparency</h4>
            <p className="text-xs text-slate-400 mb-3">
              All schemes are verified against official gazettes, department portals, and Government of India sources.
            </p>
            <div className="text-xs text-slate-500 space-y-1">
              <p>Government of India & State Welfare Programs</p>
              <p>Direct Benefit Transfer (DBT) Compatible</p>
            </div>
          </div>

        </div>

        <div className="pt-8 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© {new Date().getFullYear()} JanSetu AI. Built for Digital India and citizen empowerment.</p>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1 text-slate-400">
              Made with <Heart className="w-3.5 h-3.5 text-red-500 fill-red-500" /> for Indian Citizens
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
};
