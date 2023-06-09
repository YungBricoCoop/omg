// components
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// pages
import Home from '../pages/Home';

const Router: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<Home />} />
            </Routes>
        </BrowserRouter>
    );
};

export default Router;
