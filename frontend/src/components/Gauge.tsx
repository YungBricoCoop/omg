// components
import { motion } from 'framer-motion';
import { PuffLoader } from 'react-spinners';

// interface
interface GaugeProps {
    value: number | null;
}

const Gauge: React.FC<GaugeProps> = ({ value }) => {
    const loading = value === null || value === undefined;
    const pathLength = (value || 0) / 100;

    return (
        <motion.div
            key={`gauge-${value}`}
            className='relative flex items-center justify-center w-12 h-12 bg-white bg-opacity-10 rounded-lg'
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{
                duration: 1.5,
                type: 'spring',
                bounce: 0.5,
            }}
        >
            {loading ? (
                <PuffLoader color='#ffffff' size={40} speedMultiplier={0.4} />
            ) : (
                <>
                    <motion.svg
                        width='50'
                        height='50'
                        viewBox='0 0 50 50'
                        fill='none'
                        xmlns='http://www.w3.org/2000/svg'
                    >
                        <motion.rect
                            x='1'
                            y='1'
                            width='48'
                            height='48'
                            rx='10'
                            stroke='white'
                            strokeWidth='2'
                            pathLength={1}
                            initial={{ pathLength: 0 }}
                            animate={{ pathLength }}
                            transition={{ duration: 1 }}
                        />
                    </motion.svg>
                    <p className='absolute text-lg'>{value}</p>
                </>
            )}
        </motion.div>
    );
};

export default Gauge;
