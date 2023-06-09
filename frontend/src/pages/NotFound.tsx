// components
import Page from '../components/Page';
import { motion } from 'framer-motion';

const NotFound: React.FC = () => {
    return (
        <Page title='404' className='overflow-hidden'>
            <motion.div
                className='relative flex flex-col items-center py-20 font-bold mx-auto w-11/12 xl:w-8/12 bg-primary bg-opacity-10 backdrop-blur-sm rounded-lg p-6 mt-16 border-dashed border-2 border-white text-white'
                initial={{ opacity: 0, scale: 0.4 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{
                    duration: 1,
                    type: 'spring',
                    bounce: 0.2,
                }}
            >
                <motion.h2
                    className='text-4xl'
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.6, delay: 0.4 }}
                >
                    Big'Ol
                </motion.h2>
                <motion.h1
                    className='text-[16rem] leading-[200px]'
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.6 }}
                >
                    404
                </motion.h1>
                <motion.h2
                    className='text-4xl'
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.6, delay: 0.5 }}
                >
                    Error
                </motion.h2>
            </motion.div>
            <motion.h3
                className='mt-2 text-center text-white italic'
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 1, delay: 0.6 }}
            >
                Looks like the page ventured into the anomaly with Octavia
            </motion.h3>
        </Page>
    );
};

export default NotFound;
