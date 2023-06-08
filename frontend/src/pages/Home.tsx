// react
import { useEffect } from 'react';

// css

// functions
import useReactQuerySubscription from '../hooks/useReactQuerySocketSub';
import { useQuery } from '@tanstack/react-query';
import { getId } from '../api/api';
import { getIdFromStorage, setIdToStorage } from '../utils/utils';

// components
import Page from '../components/Page';
import CopyField from '../components/CopyField';
import { motion } from 'framer-motion';

// images

const Home: React.FC = () => {
    const id = getIdFromStorage();

    // queries
    const socketQ = useQuery(
        ['websocket'],
        () => {
            return null as any;
        },
        {
            refetchOnWindowFocus: false,
            enabled: id !== null,
        }
    );

    const idQ = useQuery(['id'], getId, {
        refetchOnWindowFocus: false,
        enabled: !id,
    });

    // effects
    useEffect(() => {
        if (!idQ.data) return;
        setIdToStorage(idQ.data);
    }, [idQ.data]);

    return (
        <Page className="overflow-hidden">
            <div className="flex flex-col mx-auto gap-4 mt-12 font-mono w-80 sm:w-96 text-white text-2xl">
                <CopyField
                    value="omg@elwan.ch"
                    arrow={1}
                    arrowText="Transfer to"
                />
                <CopyField
                    value={getIdFromStorage() || ''}
                    arrow={2}
                    arrowText="Use as subject"
                />
            </div>
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
