const API_BASE = '/api';
const AI_BASE = '/ai-api';

const getAuthHeaders = () => {
  const token = localStorage.getItem('jansetu_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  };
};

export const api = {
  // Auth
  register: async (data) => {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.message || 'Registration failed');
    }
    return res.json();
  },

  login: async (data) => {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.message || 'Invalid email or password');
    }
    return res.json();
  },

  getCurrentUser: async () => {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Not authenticated');
    return res.json();
  },

  // Citizen Profile
  getProfile: async () => {
    const res = await fetch(`${API_BASE}/profile`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to load citizen profile');
    return res.json();
  },

  updateProfile: async (profileData) => {
    const res = await fetch(`${API_BASE}/profile`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(profileData)
    });
    if (!res.ok) throw new Error('Failed to update profile');
    return res.json();
  },

  // Opportunities
  getOpportunities: async (params = {}) => {
    const query = new URLSearchParams();
    if (params.category && params.category !== 'ALL') query.append('category', params.category);
    if (params.type && params.type !== 'ALL') query.append('type', params.type);
    if (params.govtLevel && params.govtLevel !== 'ALL') query.append('govtLevel', params.govtLevel);
    if (params.state && params.state !== 'ALL') query.append('state', params.state);
    if (params.search) query.append('search', params.search);
    if (params.page !== undefined) query.append('page', params.page);
    if (params.size) query.append('size', params.size);

    const res = await fetch(`${API_BASE}/opportunities?${query.toString()}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to fetch opportunities');
    return res.json();
  },

  getOpportunityById: async (id) => {
    const res = await fetch(`${API_BASE}/opportunities/${id}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Opportunity not found');
    return res.json();
  },

  getOpportunityBySlug: async (slug) => {
    const res = await fetch(`${API_BASE}/opportunities/slug/${slug}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Opportunity not found');
    return res.json();
  },

  getCategories: async () => {
    const res = await fetch(`${API_BASE}/opportunities/categories`);
    return res.ok ? res.json() : [];
  },

  getStats: async () => {
    const res = await fetch(`${API_BASE}/opportunities/stats`);
    return res.ok ? res.json() : { totalActiveSchemes: 70, totalCategories: 8, totalStatesCovered: 15 };
  },

  // Eligibility Rule Matching
  getMatchedSchemes: async () => {
    const res = await fetch(`${API_BASE}/match/schemes`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to evaluate scheme matches');
    return res.json();
  },

  previewMatch: async (profileDto) => {
    const res = await fetch(`${API_BASE}/match/preview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profileDto)
    });
    if (!res.ok) throw new Error('Failed to preview matches');
    return res.json();
  },

  // Saved Bookmarks
  getSavedOpportunities: async () => {
    const res = await fetch(`${API_BASE}/saved`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to load saved schemes');
    return res.json();
  },

  saveOpportunity: async (id) => {
    const res = await fetch(`${API_BASE}/saved/${id}`, {
      method: 'POST',
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to save scheme');
    return res.json();
  },

  unsaveOpportunity: async (id) => {
    const res = await fetch(`${API_BASE}/saved/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to remove saved scheme');
    return res.json();
  },

  // Application Tracking
  getTrackings: async () => {
    const res = await fetch(`${API_BASE}/tracking`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to load tracking data');
    return res.json();
  },

  trackOpportunity: async (data) => {
    const res = await fetch(`${API_BASE}/tracking`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error('Failed to update tracking');
    return res.json();
  },

  deleteTracking: async (id) => {
    const res = await fetch(`${API_BASE}/tracking/${id}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error('Failed to delete tracking');
    return res.json();
  },

  // Feedback
  submitFeedback: async (feedback) => {
    const res = await fetch(`${API_BASE}/feedback/submit`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(feedback)
    });
    if (!res.ok) throw new Error('Failed to submit feedback');
    return res.json();
  },

  // AI Service
  askAi: async (message, history = [], userContext = {}) => {
    try {
      const res = await fetch(`${AI_BASE}/api/ai/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, history, user_context: userContext })
      });
      if (!res.ok) throw new Error('AI service error');
      return await res.json();
    } catch {
      // Fallback response if AI service is starting
      return {
        reply: "I am JanSetu AI. You can discover 70+ government schemes in agriculture, student scholarships, women empowerment, and enterprise loans through our platform.",
        suggested_schemes: ["PM-KISAN", "Ayushman Bharat", "Mudra Yojana"],
        action_items: ["Complete your citizen profile for automated eligibility scoring"]
      };
    }
  }
};
