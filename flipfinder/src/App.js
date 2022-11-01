import React from 'react';
import {Route, Routes} from 'react-router-dom';
import PlaceholderHome from './components/PlaceholderHomepage';
import ItemIDHook from './components/ItemIDHook';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<PlaceholderHome />} />
        <Route path="/itemdetails/:id" element={<ItemIDHook />} />
        <Route path="*" element={<h1>404 Not Found</h1>} />
      </Routes>
    </div>
  );
}

export default App;
