import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { AiChatDrawer } from './components/AiChatDrawer';
import { AuthModal } from './pages/AuthModal';

import { HomePage } from './pages/HomePage';
import { SchemesExplorerPage } from './pages/SchemesExplorerPage';
import { SchemeDetailsPage } from './pages/SchemeDetailsPage';
import { QuestionnairePage } from './pages/QuestionnairePage';
import { DashboardPage } from './pages/DashboardPage';
import { SavedSchemesPage } from './pages/SavedSchemesPage';
import { TrackingPage } from './pages/TrackingPage';

export function App() {
  const [aiChatOpen, setAiChatOpen] = useState(false);
  const [authModalOpen, setAuthModalOpen] = useState(false);

  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
          <Navbar 
            onOpenAiChat={() => setAiChatOpen(true)}
            onOpenAuthModal={() => setAuthModalOpen(true)}
          />

          <main className="flex-1">
            <Routes>
              <Route path="/" element={<HomePage onOpenAiChat={() => setAiChatOpen(true)} />} />
              <Route path="/schemes" element={<SchemesExplorerPage />} />
              <Route path="/schemes/:id" element={<SchemeDetailsPage onOpenAiChat={() => setAiChatOpen(true)} />} />
              <Route path="/questionnaire" element={<QuestionnairePage onOpenAuthModal={() => setAuthModalOpen(true)} />} />
              <Route path="/dashboard" element={<DashboardPage onOpenAiChat={() => setAiChatOpen(true)} />} />
              <Route path="/saved" element={<SavedSchemesPage />} />
              <Route path="/tracking" element={<TrackingPage />} />
            </Routes>
          </main>

          <Footer />

          {/* Global AI Chat Drawer */}
          <AiChatDrawer 
            isOpen={aiChatOpen} 
            onClose={() => setAiChatOpen(false)} 
          />

          {/* Global Auth Modal */}
          <AuthModal 
            isOpen={authModalOpen} 
            onClose={() => setAuthModalOpen(false)} 
          />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
