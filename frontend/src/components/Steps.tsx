import React from 'react';

// components
import { motion } from 'framer-motion';
import { PuffLoader } from 'react-spinners';

interface StepProps {
    steps: string[];
    currentStep: number;
    className?: string;
}

const Steps: React.FC<StepProps> = ({ steps, currentStep, className = '' }) => {
    return (
        <motion.div
            className={`${className} flex justify-between items-center w-full`}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{
                duration: 0.5,
                delay: 0.2,
            }}
        >
            {steps.map((step, index) => {
                const isAfter = index < currentStep;
                const isTwoAfter = index < currentStep - 1;
                const isUpcoming = index === currentStep;

                return (
                    <React.Fragment key={index}>
                        <div className="text-center">
                            <motion.div
                                className={`relative w-6 h-6 rounded-full border-2 border-white
                            }`}
                                initial={{ backgroundColor: '#ffffff00' }}
                                animate={{
                                    backgroundColor: isAfter
                                        ? '#fff'
                                        : '#ffffff00',
                                }}
                                transition={{ duration: 0.5 }}
                            >
                                <p className="absolute top-10 left-1/2 w-32  transform -translate-x-1/2 -translate-y-1/2 text-white text-xs">
                                    {step}
                                </p>
                                {isUpcoming ? (
                                    <PuffLoader
                                        size={20}
                                        color={'#fff'}
                                        loading={isUpcoming}
                                        speedMultiplier={0.4}
                                    />
                                ) : (
                                    <motion.p
                                        className="absolute top-1/2 left-1/2  transform -translate-x-1/2 -translate-y-1/2 text-xs"
                                        initial={{ color: '#ffffff00' }}
                                        animate={{
                                            color: isAfter ? '#000' : '#fff',
                                        }}
                                        transition={{ duration: 0.3 }}
                                    >
                                        {index + 1}
                                    </motion.p>
                                )}
                            </motion.div>
                        </div>
                        {index < steps.length - 1 && (
                            <motion.div
                                className={`flex-grow border-b-2 mx-4 rounded-full`}
                                initial={{ opacity: 0.2, scaleX: 0.8 }}
                                animate={{
                                    opacity: isTwoAfter ? 1 : 0.2,
                                    scaleX: isTwoAfter ? 1 : 0.8,
                                }}
                                transition={{ duration: 0.5 }}
                            ></motion.div>
                        )}
                    </React.Fragment>
                );
            })}
        </motion.div>
    );
};

export default Steps;
