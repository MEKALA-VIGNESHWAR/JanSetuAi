import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Sparkles, 
  ArrowRight, 
  ArrowLeft, 
  CheckCircle2, 
  User, 
  Briefcase, 
  GraduationCap, 
  Building, 
  ShieldCheck,
  AlertCircle
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { OpportunityCard } from '../components/OpportunityCard';

export const QuestionnairePage = ({ onOpenAuthModal }) => {
  const { user, profile, refreshProfile } = useAuth();
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [previewMatches, setPreviewMatches] = useState(null);

  // Form State initialized from user profile if exists
  const [formData, setFormData] = useState({
    fullName: '',
    age: '',
    gender: 'MALE',
    state: 'Telangana',
    district: '',
    areaType: 'RURAL',
    
    // Role & Occupation
    primaryRole: 'FARMER',
    occupation: 'FARMER',
    isStudent: false,
    educationLevel: '12TH',
    courseStream: '',
    collegeType: 'GOVERNMENT',
    
    // Economic
    annualIncome: 120000,
    incomeCategory: 'BPL',
    employmentStatus: 'SELF_EMPLOYED',
    
    // Social
    socialCategory: 'OBC',
    isPwd: false,
    disabilityType: '',
    
    // Special conditions
    maritalStatus: 'MARRIED',
    isWidow: false,
    isSingleWoman: false,
    
    // Farmer
    isFarmer: true,
    ownsLand: true,
    hasLivestock: true,
    landHoldingAcres: 2.5,
    cropType: 'Paddy / Cotton',
    
    // Business
    hasBusiness: false,
    businessType: ''
  });

  useEffect(() => {
    if (profile) {
      setFormData(prev => ({
        ...prev,
        fullName: profile.fullName || prev.fullName,
        age: profile.age || prev.age,
        gender: profile.gender || prev.gender,
        state: profile.state || prev.state,
        district: profile.district || prev.district,
        areaType: profile.areaType || prev.areaType,
        occupation: profile.occupation || prev.occupation,
        primaryRole: profile.primaryRole || profile.occupation || prev.primaryRole,
        educationLevel: profile.educationLevel || prev.educationLevel,
        annualIncome: profile.annualIncome || prev.annualIncome,
        incomeCategory: profile.incomeCategory || prev.incomeCategory,
        socialCategory: profile.socialCategory || prev.socialCategory,
        isPwd: profile.isPwd || prev.isPwd,
        isFarmer: profile.isFarmer || prev.isFarmer,
        hasBusiness: profile.hasBusiness || prev.hasBusiness
      }));
    }
  }, [profile]);

  const handleChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleRoleSelect = (role) => {
    let occ = role;
    let isFarm = role === 'FARMER';
    let isStud = role === 'STUDENT';
    let hasBiz = role === 'ENTREPRENEUR';

    setFormData(prev => ({
      ...prev,
      primaryRole: role,
      occupation: occ,
      isFarmer: isFarm,
      isStudent: isStud,
      hasBusiness: hasBiz
    }));
  };

  const handleComplete = async () => {
    setLoading(true);
    try {
      const payload = {
        ...formData,
        age: formData.age ? parseInt(formData.age, 10) : null,
        annualIncome: formData.annualIncome ? parseInt(formData.annualIncome, 10) : null,
        onboardingStep: 4
      };

      if (user) {
        // Save to user profile
        await api.updateProfile(payload);
        await refreshProfile();
        navigate('/dashboard');
      } else {
        // Guest mode: run instant eligibility rule match preview
        const matches = await api.previewMatch(payload);
        setPreviewMatches(matches);
      }
    } catch (err) {
      console.error(err);
      alert('Error calculating eligibility. Please check fields.');
    } finally {
      setLoading(false);
    }
  };

  const indianStates = [
    "Telangana", "Andhra Pradesh", "Karnataka", "Tamil Nadu", "Maharashtra", 
    "Uttar Pradesh", "Bihar", "Madhya Pradesh", "Rajasthan", "West Bengal", 
    "Gujarat", "Kerala", "Odisha", "Punjab", "Haryana", "Delhi"
  ];

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-8">
          <span className="text-xs font-bold text-brand-600 uppercase tracking-wider inline-flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-brand-500" />
            Citizen Eligibility Questionnaire
          </span>
          <h1 className="text-3xl font-extrabold text-slate-900 mt-1">
            Check Welfare & Scheme Eligibility
          </h1>
          <p className="text-xs text-slate-500 mt-2 max-w-md mx-auto">
            Answer a few quick questions to match your exact citizen profile with central and state government entitlements.
          </p>

          {/* Stepper */}
          <div className="flex items-center justify-center gap-2 mt-6 max-w-sm mx-auto">
            {[1, 2, 3, 4].map((stepNum) => (
              <div 
                key={stepNum} 
                className={`flex-1 h-2 rounded-full transition-all ${
                  step >= stepNum ? 'bg-brand-600' : 'bg-slate-200'
                }`}
              />
            ))}
          </div>
          <p className="text-[11px] font-semibold text-slate-400 mt-2">
            Step {step} of 4: {
              step === 1 ? 'Basic Details' :
              step === 2 ? 'Primary Role' :
              step === 3 ? 'Education & Income' : 'Category & Specific Conditions'
            }
          </p>
        </div>

        {/* Form Card */}
        {!previewMatches ? (
          <div className="bg-white rounded-3xl border border-slate-200 shadow-xl p-6 sm:p-10">
            
            {/* STEP 1: Basic */}
            {step === 1 && (
              <div className="space-y-5 animate-in fade-in duration-200">
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <User className="w-5 h-5 text-brand-600" />
                  Basic Citizen Information
                </h2>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">Full Name</label>
                  <input
                    type="text"
                    value={formData.fullName}
                    onChange={(e) => handleChange('fullName', e.target.value)}
                    placeholder="Enter your name"
                    className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Age (Years) *</label>
                    <input
                      type="number"
                      required
                      min={1}
                      max={120}
                      value={formData.age}
                      onChange={(e) => handleChange('age', e.target.value)}
                      placeholder="e.g. 24"
                      className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Gender *</label>
                    <select
                      value={formData.gender}
                      onChange={(e) => handleChange('gender', e.target.value)}
                      className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                    >
                      <option value="MALE">Male</option>
                      <option value="FEMALE">Female</option>
                      <option value="OTHER">Other</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">State of Residence *</label>
                    <select
                      value={formData.state}
                      onChange={(e) => handleChange('state', e.target.value)}
                      className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                    >
                      {indianStates.map(s => (
                        <option key={s} value={s}>{s}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Area Type *</label>
                    <select
                      value={formData.areaType}
                      onChange={(e) => handleChange('areaType', e.target.value)}
                      className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                    >
                      <option value="RURAL">Rural (Village / Gram Panchayat)</option>
                      <option value="URBAN">Urban (Municipality / City)</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">District</label>
                  <input
                    type="text"
                    value={formData.district}
                    onChange={(e) => handleChange('district', e.target.value)}
                    placeholder="e.g. Hyderabad, Warangal, Medak..."
                    className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                  />
                </div>
              </div>
            )}

            {/* STEP 2: Primary Role */}
            {step === 2 && (
              <div className="space-y-5 animate-in fade-in duration-200">
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Briefcase className="w-5 h-5 text-brand-600" />
                  What best describes you?
                </h2>
                <p className="text-xs text-slate-500">
                  Select your primary occupation or status to filter targeted government initiatives.
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                  {[
                    { id: 'STUDENT', title: 'Student', desc: 'Enrolled in school, college, or university', icon: '🎓' },
                    { id: 'FARMER', title: 'Farmer / Cultivator', desc: 'Engaged in agriculture or allied animal husbandry', icon: '🌾' },
                    { id: 'JOB_SEEKER', title: 'Job Seeker', desc: 'Looking for employment or skill development', icon: '💼' },
                    { id: 'ENTREPRENEUR', title: 'Entrepreneur / MSME', desc: 'Running or planning a business or micro-enterprise', icon: '🏪' },
                    { id: 'EMPLOYEE', title: 'Employed Worker', desc: 'Salaried employee in organized/unorganized sector', icon: '👷' },
                    { id: 'HOMEMAKER', title: 'Homemaker / Single Woman', desc: 'Managing household, widow, or single earner', icon: '🏡' },
                  ].map((item) => (
                    <button
                      type="button"
                      key={item.id}
                      onClick={() => handleRoleSelect(item.id)}
                      className={`p-4 rounded-2xl border text-left flex items-start gap-3 transition-all cursor-pointer ${
                        formData.primaryRole === item.id 
                          ? 'border-brand-600 bg-brand-50/70 ring-2 ring-brand-500 shadow-sm' 
                          : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                      }`}
                    >
                      <span className="text-2xl">{item.icon}</span>
                      <div>
                        <span className="font-bold text-xs text-slate-900 block">{item.title}</span>
                        <span className="text-[11px] text-slate-500 leading-snug">{item.desc}</span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* STEP 3: Education & Economic */}
            {step === 3 && (
              <div className="space-y-5 animate-in fade-in duration-200">
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <GraduationCap className="w-5 h-5 text-brand-600" />
                  Education & Economic Status
                </h2>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Education Level</label>
                    <select
                      value={formData.educationLevel}
                      onChange={(e) => handleChange('educationLevel', e.target.value)}
                      className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                    >
                      <option value="BELOW_10TH">Below 10th</option>
                      <option value="10TH">10th Pass</option>
                      <option value="12TH">12th / Intermediate</option>
                      <option value="DIPLOMA">Diploma / Polytechnic</option>
                      <option value="UNDERGRADUATE">Graduate (BA, B.Sc, B.Tech, etc.)</option>
                      <option value="POSTGRADUATE">Postgraduate (MA, M.Sc, etc.)</option>
                      <option value="PHD">Ph.D. / Doctorate</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Income Category</label>
                    <select
                      value={formData.incomeCategory}
                      onChange={(e) => handleChange('incomeCategory', e.target.value)}
                      className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                    >
                      <option value="BPL">BPL (Below Poverty Line / White Ration Card)</option>
                      <option value="LIG">LIG (Low Income: &lt; ₹3 Lakhs/yr)</option>
                      <option value="MIG">MIG (Middle Income: ₹3 - ₹8 Lakhs/yr)</option>
                      <option value="HIG">HIG (Higher Income: &gt; ₹8 Lakhs/yr)</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">
                    Annual Household Income (₹ INR)
                  </label>
                  <input
                    type="number"
                    value={formData.annualIncome}
                    onChange={(e) => handleChange('annualIncome', e.target.value)}
                    placeholder="e.g. 150000"
                    className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                  />
                  <p className="text-[10px] text-slate-500 mt-1">Most scholarships and welfare benefits use ₹2.5 Lakhs as eligibility cutoff.</p>
                </div>

                {formData.primaryRole === 'STUDENT' && (
                  <div className="p-4 rounded-2xl bg-blue-50/50 border border-blue-200/60 space-y-3">
                    <label className="block text-xs font-bold text-blue-900">Student Specific Details</label>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <span className="text-[11px] text-slate-600 block mb-1">Course / Stream</span>
                        <input
                          type="text"
                          value={formData.courseStream}
                          onChange={(e) => handleChange('courseStream', e.target.value)}
                          placeholder="e.g. B.Tech Computer Science, B.Sc"
                          className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300 bg-white"
                        />
                      </div>
                      <div>
                        <span className="text-[11px] text-slate-600 block mb-1">Institution Type</span>
                        <select
                          value={formData.collegeType}
                          onChange={(e) => handleChange('collegeType', e.target.value)}
                          className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300 bg-white"
                        >
                          <option value="GOVERNMENT">Government College / University</option>
                          <option value="AIDED">Government-Aided</option>
                          <option value="PRIVATE">Private Recognized</option>
                        </select>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* STEP 4: Category & Conditions */}
            {step === 4 && (
              <div className="space-y-5 animate-in fade-in duration-200">
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-brand-600" />
                  Social Category & Specific Conditions
                </h2>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Social Category (Reservation / Caste)</label>
                    <select
                      value={formData.socialCategory}
                      onChange={(e) => handleChange('socialCategory', e.target.value)}
                      className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                    >
                      <option value="GENERAL">General / Open Category</option>
                      <option value="OBC">OBC (Other Backward Classes)</option>
                      <option value="SC">SC (Scheduled Caste)</option>
                      <option value="ST">ST (Scheduled Tribe)</option>
                      <option value="EWS">EWS (Economically Weaker Section)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Marital Status</label>
                    <select
                      value={formData.maritalStatus}
                      onChange={(e) => handleChange('maritalStatus', e.target.value)}
                      className="w-full text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500"
                    >
                      <option value="UNMARRIED">Unmarried / Single</option>
                      <option value="MARRIED">Married</option>
                      <option value="WIDOWED">Widowed</option>
                      <option value="DIVORCED">Divorced / Separated</option>
                    </select>
                  </div>
                </div>

                {/* Conditional Toggles */}
                <div className="space-y-3 pt-2">
                  <label className="flex items-center gap-3 p-3 rounded-xl border border-slate-200 hover:bg-slate-50 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={formData.isPwd}
                      onChange={(e) => handleChange('isPwd', e.target.checked)}
                      className="w-4 h-4 text-brand-600 rounded focus:ring-brand-500"
                    />
                    <div>
                      <span className="text-xs font-bold text-slate-800 block">Person with Disability (PwD / Divyangjan)</span>
                      <span className="text-[10px] text-slate-500">Unlocks special assistive technology grants and enhanced reservation quotas</span>
                    </div>
                  </label>

                  {formData.gender === 'FEMALE' && (
                    <label className="flex items-center gap-3 p-3 rounded-xl border border-slate-200 hover:bg-slate-50 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.isWidow}
                        onChange={(e) => handleChange('isWidow', e.target.checked)}
                        className="w-4 h-4 text-brand-600 rounded focus:ring-brand-500"
                      />
                      <div>
                        <span className="text-xs font-bold text-slate-800 block">Widow / Single Destitute Woman</span>
                        <span className="text-[10px] text-slate-500">Eligible for pension and special state economic assistance</span>
                      </div>
                    </label>
                  )}

                  {formData.primaryRole === 'FARMER' && (
                    <label className="flex items-center gap-3 p-3 rounded-xl border border-slate-200 hover:bg-slate-50 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.ownsLand}
                        onChange={(e) => handleChange('ownsLand', e.target.checked)}
                        className="w-4 h-4 text-brand-600 rounded focus:ring-brand-500"
                      />
                      <div>
                        <span className="text-xs font-bold text-slate-800 block">Owns Agricultural Land (Pattadar Passbook holder)</span>
                        <span className="text-[10px] text-slate-500">Qualifies for direct DBT schemes such as PM-KISAN and Rythu Bandhu</span>
                      </div>
                    </label>
                  )}
                </div>

              </div>
            )}

            {/* Stepper Buttons */}
            <div className="mt-8 pt-5 border-t border-slate-100 flex items-center justify-between">
              {step > 1 ? (
                <button
                  type="button"
                  onClick={() => setStep(step - 1)}
                  className="px-4 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-700 hover:bg-slate-50 flex items-center gap-1.5 cursor-pointer"
                >
                  <ArrowLeft className="w-4 h-4" />
                  Back
                </button>
              ) : <div />}

              {step < 4 ? (
                <button
                  type="button"
                  onClick={() => setStep(step + 1)}
                  className="px-6 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-xs font-bold text-white shadow-md shadow-brand-500/20 flex items-center gap-1.5 cursor-pointer"
                >
                  Next Step
                  <ArrowRight className="w-4 h-4" />
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handleComplete}
                  disabled={loading}
                  className="px-8 py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-xs font-bold text-white shadow-lg shadow-emerald-500/25 flex items-center gap-2 cursor-pointer"
                >
                  <Sparkles className="w-4 h-4" />
                  {loading ? 'Evaluating Eligibility Engine...' : 'Run Eligibility Matching'}
                </button>
              )}
            </div>

          </div>
        ) : (
          /* PREVIEW MATCHES FOR GUEST */
          <div className="space-y-6 animate-in fade-in duration-300">
            <div className="bg-emerald-50 border border-emerald-200 rounded-3xl p-6 text-emerald-950 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <h3 className="font-extrabold text-lg flex items-center gap-2 text-emerald-900">
                  <CheckCircle2 className="w-6 h-6 text-emerald-600" />
                  Matches Found Based on Your Profile!
                </h3>
                <p className="text-xs text-emerald-800 mt-1">
                  We evaluated 70+ government welfare rules against your details.
                </p>
              </div>

              {!user && (
                <button
                  onClick={onOpenAuthModal}
                  className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md whitespace-nowrap cursor-pointer"
                >
                  Save Profile & Track
                </button>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {previewMatches.slice(0, 8).map((match, idx) => (
                <OpportunityCard
                  key={idx}
                  opportunity={match.opportunity}
                  matchScore={match.matchScore}
                  matchStatus={match.matchStatus}
                  passedCriteria={match.passedCriteria}
                  failedCriteria={match.failedCriteria}
                  missingFields={match.missingFields}
                />
              ))}
            </div>

            <div className="text-center pt-6">
              <button
                onClick={() => setPreviewMatches(null)}
                className="text-xs text-brand-600 font-bold hover:underline"
              >
                &larr; Retake Questionnaire with Different Details
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
};
