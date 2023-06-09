// components
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// pages
import Home from '../pages/Home';
import About from './About';
import NotFound from './NotFound';

const Router: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<Home />} />
                <Route path='/about' element={<About />} />
                <Route path='*' element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
};

export default Router;
