import React from 'react';

// components
import Footer from './Footer';

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
    return (
        <>
            <div
                className={`${className} page flex flex-row min-h-screen`}
                style={{
                    backgroundImage: `url(${bg})`,
                    backgroundSize: 'cover',
                }}
            >
                <div className={`sm:w-8/12 mx-auto pb-16 sm:pb-12`}>
                    <div className="flex justify-center sm:justify-between items-center mt-4">
                        <img src={logo} alt="logo" className="w-36" />
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
