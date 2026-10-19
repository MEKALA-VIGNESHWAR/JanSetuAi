import React, { useState, useRef, useEffect } from 'react';
import { 
  Bot, 
  X, 
  Send, 
  Sparkles, 
  FileText, 
  CheckCircle2, 
  ArrowRight,
  User
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export const AiChatDrawer = ({ isOpen, onClose }) => {
  const { profile } = useAuth();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Namaste! I am your JanSetu AI Advisor. Ask me anything about government schemes, eligibility requirements, required documents, or how to apply.',
      suggested_schemes: ['PM-KISAN', 'Ayushman Bharat PM-JAY', 'PM Mudra Yojana'],
      action_items: ['Complete your profile for 100% matched results']
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const quickPrompts = [
    "Schemes for small farmers",
    "Scholarships for graduation students",
    "Loans for women entrepreneurs",
    "Health insurance benefits under Ayushman Bharat"
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSend = async (userText) => {
    const query = userText || input;
    if (!query.trim()) return;

    const newMessages = [...messages, { role: 'user', content: query }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const userContext = profile ? {
        state: profile.state,
        occupation: profile.occupation,
        age: profile.age,
        socialCategory: profile.socialCategory
      } : {};

      const response = await api.askAi(query, newMessages, userContext);
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: response.reply,
          suggested_schemes: response.suggested_schemes || [],
          action_items: response.action_items || []
        }
      ]);
    } catch {
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an issue connecting to the knowledge base. Please try asking again shortly.',
          suggested_schemes: [],
          action_items: []
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white shadow-2xl flex flex-col border-l border-slate-200">
          
          {/* Header */}
          <div className="p-4 bg-gradient-to-r from-blue-700 via-indigo-700 to-brand-700 text-white flex items-center justify-between shadow">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-white/20 backdrop-blur flex items-center justify-center text-white border border-white/20">
                <Bot className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-sm font-bold flex items-center gap-1.5">
                  JanSetu AI Advisor
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-400/20 text-emerald-300 font-medium">Online</span>
                </h2>
                <p className="text-[11px] text-blue-100">Intelligent Welfare & Scheme Guidance</p>
              </div>
            </div>

            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Messages Container */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
            {messages.map((m, idx) => (
              <div key={idx} className={`flex gap-2.5 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {m.role === 'assistant' && (
                  <div className="w-7 h-7 rounded-lg bg-brand-600 text-white flex items-center justify-center text-xs flex-shrink-0 mt-0.5">
                    <Bot className="w-4 h-4" />
                  </div>
                )}

                <div className={`max-w-[85%] rounded-2xl p-3.5 text-xs shadow-sm ${
                  m.role === 'user' 
                    ? 'bg-brand-600 text-white rounded-br-none' 
                    : 'bg-white text-slate-800 border border-slate-200 rounded-bl-none'
                }`}>
                  <p className="leading-relaxed whitespace-pre-wrap">{m.content}</p>

                  {/* Scheme suggestions */}
                  {m.suggested_schemes && m.suggested_schemes.length > 0 && (
                    <div className="mt-3 pt-2.5 border-t border-slate-100">
                      <p className="text-[11px] font-bold text-brand-700 mb-1.5 flex items-center gap-1">
                        <Sparkles className="w-3 h-3 text-amber-500" />
                        Relevant Schemes:
                      </p>
                      <div className="flex flex-wrap gap-1.5">
                        {m.suggested_schemes.map((s, sIdx) => (
                          <button
                            key={sIdx}
                            onClick={() => {
                              navigate(`/schemes?search=${encodeURIComponent(s)}`);
                              onClose();
                            }}
                            className="text-[11px] px-2.5 py-1 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200/80 font-medium transition-colors flex items-center gap-1 cursor-pointer"
                          >
                            {s}
                            <ArrowRight className="w-2.5 h-2.5" />
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Action items */}
                  {m.action_items && m.action_items.length > 0 && (
                    <div className="mt-2.5 pt-2 border-t border-slate-100 text-[11px] text-slate-600 space-y-1">
                      <p className="font-semibold text-slate-700 flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Checklist:
                      </p>
                      {m.action_items.map((item, iIdx) => (
                        <p key={iIdx} className="pl-3.5 text-slate-600">
                          • {item}
                        </p>
                      ))}
                    </div>
                  )}
                </div>

                {m.role === 'user' && (
                  <div className="w-7 h-7 rounded-lg bg-slate-300 text-slate-700 flex items-center justify-center text-xs flex-shrink-0 mt-0.5">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex items-center gap-2 text-xs text-slate-500 bg-white p-3 rounded-2xl border border-slate-200 w-fit">
                <Bot className="w-4 h-4 text-brand-600 animate-spin" />
                Searching schemes and eligibility rules...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Prompts */}
          <div className="p-2.5 bg-white border-t border-slate-100 overflow-x-auto flex gap-1.5 no-scrollbar">
            {quickPrompts.map((qp, qIdx) => (
              <button
                key={qIdx}
                onClick={() => handleSend(qp)}
                disabled={loading}
                className="whitespace-nowrap text-[11px] px-2.5 py-1 rounded-full bg-slate-100 hover:bg-brand-50 hover:text-brand-700 text-slate-600 border border-slate-200 transition-colors flex-shrink-0"
              >
                {qp}
              </button>
            ))}
          </div>

          {/* Input Box */}
          <div className="p-3 bg-white border-t border-slate-200 flex items-center gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about schemes, subsidies, loans..."
              className="flex-1 text-xs px-3.5 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
            />
            <button
              onClick={() => handleSend()}
              disabled={loading || !input.trim()}
              className="p-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white transition-colors cursor-pointer"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>

        </div>
      </div>
    </div>
  );
};
