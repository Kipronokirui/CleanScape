/* eslint-disable no-unused-vars */
import React from 'react'
import { BrowserRouter as Router, Routes, Route, Outlet } from "react-router-dom";
import Navbar from './components/common/Navbar';
import Footer from './components/common/Footer';
import Home from './pages/Home';
import Appointment from './pages/Appointment';
import NotFound from './pages/NotFound';

const AppLayout = () => {
  return (
    <>
      <Navbar />
      <main className={`min-h-screen`}>
        <Outlet />
      </main>
      <Footer />
    </>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" exact element={<Home />} />
          <Route path="/book-appointment" exact element={<Appointment />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App
