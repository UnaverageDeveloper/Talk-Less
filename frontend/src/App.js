/*
 * Talk-Less Main Application Component
 * Copyright (C) 2024 Talk-Less Contributors
 * 
 * This file is part of Talk-Less.
 * 
 * Talk-Less is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import SummaryList from './components/SummaryList';
import SummaryDetail from './components/SummaryDetail';
import SourceList from './components/SourceList';
import About from './components/About';
import Transparency from './components/Transparency';
import NotFound from './components/NotFound';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<SummaryList />} />
            <Route path="/summary/:id" element={<SummaryDetail />} />
            <Route path="/sources" element={<SourceList />} />
            <Route path="/about" element={<About />} />
            <Route path="/transparency" element={<Transparency />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
