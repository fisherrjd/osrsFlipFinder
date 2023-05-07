import React from 'react';
import {Route, Routes} from 'react-router-dom';
import TempHome from './components/PlaceholderHomepage';
import HomePage from './components/HomePage';

import ItemIDHook from './components/ItemIDHook';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/itemdetails/:id" element={<ItemIDHook />} />
        <Route path="*" element={<h1>404 Not Found</h1>} />
      </Routes>
    </div>
  );
}

export default App;
