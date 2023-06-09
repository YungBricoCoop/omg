import React from 'react';

// components
import Overlay from './Overlay';
import Footer from './Footer';

// functions
import { useNavigate } from 'react-router-dom';

// images
import bg from '../assets/bg.png';
import logo from '../assets/logo.svg';

// interfaces
interface PageProps {
    children: React.ReactNode;
    title?: string;
    className?: string;
}

const Page: React.FC<PageProps> = ({
    children,
    title = '',
    className = '',
}) => {
    // navigate
    const navigate = useNavigate();

    // handlers
    const handleGoHome = () => {
        navigate('/');
    };

    return (
        <>
            <Overlay />
            <div
                className={`${className} page flex flex-row min-h-screen`}
                style={{
                    backgroundImage: `url(${bg})`,
                    backgroundSize: 'cover',
                }}
            >
                <div className={`sm:w-8/12 mx-auto pb-16 sm:pb-12`}>
                    <div className="flex justify-center sm:justify-between items-center mt-4">
                        <button
                            className="focus:outline-none focus:scale-105 hover:scale-105 transition-transform"
                            onClick={handleGoHome}
                        >
                            <img src={logo} alt="logo" className="w-36" />
                        </button>
                        {Boolean(title) && (
                            <h1 className="text-3xl font-bold text-white">
                                {title}
                            </h1>
                        )}
                    </div>
                    ;{children}
                </div>
            </div>
            <Footer />
        </>
    );
};

export default Page;
