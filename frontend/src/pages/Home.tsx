// react

// css

// functions

// components
import Page from '../components/Page';
import { motion } from 'framer-motion';

// images

const Home: React.FC = () => {
    return (
        <Page className="overflow-hidden">
            <motion.div
                initial={{ opacity: 0, y: 1000 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{
                    duration: 1,
                    type: 'spring',
                    bounce: 0.1,
                    delay: 0.5,
                }}
            >
                <p className="text-white text-center italic mt-2">
                    The oddness analysis takes <strong>~30</strong> seconds
                </p>
                <p className="text-white text-center italic mt-2">
                    ⚠ Do not refresh the page
                </p>
            </motion.div>
        </Page>
    );
};

export default Home;
