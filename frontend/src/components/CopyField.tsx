// react
import { useState } from 'react';

// components
import { motion } from 'framer-motion';

// interfaces
interface CopyFieldProps {
    className?: string;
    value: string;
    arrow?: number;
    arrowText?: string;
}

// images
import copy from '../assets/copy.png';
import arrow1 from '../assets/arrow1.svg';
import arrow2 from '../assets/arrow2.svg';

const CopyField: React.FC<CopyFieldProps> = ({
    className = '',
    value,
    arrow,
    arrowText,
}) => {
    // states
    const [clicked, setClicked] = useState(false);

    // handlers
    const handleCopy = () => {
        setClicked(true);
        navigator.clipboard.writeText(value);
        setTimeout(() => {
            setClicked(false);
        }, 200);
    };

    return (
        <motion.div
            className={`${className} relative flex justify-between items-center bg-primary bg-opacity-20 backdrop-blur-sm rounded-xl p-1 pl-4 border-2 border-white`}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
        >
            <p className="font-bold">{value}</p>
            <button
                onClick={handleCopy}
                className="bg-primary bg-opacity-80 hover:bg-opacity-100 text-xl px-2 py-2 rounded-xl"
            >
                <motion.img
                    src={copy}
                    alt="copy"
                    className="w-6 h-6"
                    animate={{
                        rotate: clicked ? 10 : 0,
                        scale: clicked ? 1.5 : 1,
                    }}
                    transition={{ duration: 0.1 }}
                />
            </button>
            {arrow === 1 && (
                <>
                    <motion.img
                        className="absolute -left-6 sm:-left-12 -top-12"
                        initial={{ opacity: 0, rotate: 90 }}
                        animate={{ opacity: 1, rotate: 0 }}
                        transition={{
                            duration: 0.4,
                            delay: 0.3,
                            type: 'spring',
                            bounce: 0.5,
                        }}
                        src={arrow1}
                        alt="arrow1"
                    />
                    <motion.p
                        className="absolute -left-6 sm:-left-16 -top-16 sm:-top-20 text-white text-sm sm:text-lg"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.2, delay: 0.3 }}
                    >
                        {arrowText}
                    </motion.p>
                </>
            )}
            {arrow === 2 && (
                <>
                    <motion.img
                        className="absolute left-16 -bottom-20 sm:-left-16 sm:-bottom-16"
                        initial={{ opacity: 0, rotate: 90 }}
                        animate={{ opacity: 1, rotate: 0 }}
                        transition={{
                            duration: 0.4,
                            delay: 0.4,
                            type: 'spring',
                            bounce: 0.5,
                        }}
                        src={arrow2}
                        alt="arrow2"
                    />
                    <motion.p
                        className="absolute text-sm left-0 -bottom-8 sm:-left-40 sm:-bottom-2 text-white sm:text-lg"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.2, delay: 0.4 }}
                    >
                        {arrowText}
                    </motion.p>
                </>
            )}
        </motion.div>
    );
};

export default CopyField;
