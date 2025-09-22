import { Routes, Route } from 'react-router-dom'; 
import EmployeeList from './components/Employee';   
import SearchEmployee from './components/Search';   
import ChatComponent from './components/InputArea';  
import AddEmployeeForm from './components/AddEmployee';  
import Home from './components/Home';
import NotFound from './components/404';

import './App.css';   

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/home" element={<Home />} />
      <Route path="/employees" element={<EmployeeList />} />
      <Route path="/search" element={<SearchEmployee />} />
      <Route path="/chat" element={<ChatComponent />} />
      <Route path="/add" element={<AddEmployeeForm />} />
      {/* Catch-all route for 404 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
