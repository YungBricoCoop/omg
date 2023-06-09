// react
import { useEffect } from 'react';

// functions
import useReactQuerySubscription from '../hooks/useReactQuerySocketSub';
import { useQuery } from '@tanstack/react-query';
import { getId } from '../api/api';
import { getIdFromStorage, setIdToStorage } from '../utils/utils';

// components
import Page from '../components/Page';
import CopyField from '../components/CopyField';
import Steps from '../components/Steps';
import Data from '../components/Data';
import Gauge from '../components/Gauge';
import { motion } from 'framer-motion';
import { GridLoader } from 'react-spinners';

const Home: React.FC = () => {
    const sub = useReactQuerySubscription();
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

    const socketD = socketQ.data;

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
            <Steps
                className="w-72 lg:w-4/12 mx-auto mt-20"
                steps={[
                    'Mail received',
                    'Sender, Links, Attachments',
                    'Subject, Body',
                ]}
                currentStep={socketD?.step || 0}
            />
            <motion.div
                className="flex flex-col lg:grid lg:grid-cols-3 gap-4 sm:justify-between mx-auto w-11/12 xl:w-8/12 bg-primary bg-opacity-10 backdrop-blur-sm rounded-lg p-6 mt-16 border-dashed border-2 border-white text-white"
                initial={{ y: 1000 }}
                animate={{ y: 0 }}
                transition={{
                    duration: 1,
                    type: 'spring',
                    bounce: 0.2,
                    delay: 0.3,
                }}
            >
                <div className="flex flex-col gap-4 col-span-2">
                    <div className="flex gap-2 items-center">
                        <Gauge value={socketD?.sender_oddness} />
                        <Data title="Sender" value={socketD?.sender || ''} />
                    </div>
                    <div className="flex gap-2 items-center">
                        <Gauge value={socketD?.subject_oddness} />
                        <Data title="Subject" value={socketD?.subject || ''} />
                    </div>
                    <div className="flex gap-2 items-center">
                        <Gauge value={socketD?.body_oddness} />
                        <Data
                            title="Body"
                            value={
                                socketD?.body
                                    ? `${socketD?.body.substring(0, 100)}...`
                                    : ''
                            }
                        />
                    </div>
                    <div className="flex gap-2 items-center">
                        <Gauge value={socketD?.links_oddness} />
                        <Data
                            title="Links"
                            value={
                                socketD?.links?.map(
                                    (link: any) =>
                                        `${link.link.substring(0, 40)}... (${
                                            link.oddness
                                        })`
                                ) || ''
                            }
                        />
                    </div>
                    <div className="flex gap-2 items-center">
                        <Gauge value={socketD?.attachments_oddness} />
                        <Data
                            title="Attachements"
                            value={
                                socketD?.attachments?.map(
                                    (attachment: any) =>
                                        `${attachment.name.substring(
                                            0,
                                            40
                                        )}... (${attachment.oddness})`
                                ) || ''
                            }
                        />
                    </div>
                </div>
                <div className="flex flex-col justify-center items-center mx-auto w-full sm:w-auto sm:mx-0 bg-tertiary bg-opacity-10 rounded-lg p-12 shadow-xl">
                    {socketD ? (
                        <motion.p
                            className="text-6xl font-bold text-center"
                            initial={{ scale: 0 }}
                            animate={{ scale: 1 }}
                            transition={{
                                duration: 1.5,
                                type: 'spring',
                                bounce: 0.5,
                            }}
                        >
                            {socketD?.oddness || 0}%
                        </motion.p>
                    ) : (
                        <GridLoader
                            color="#fff"
                            loading={!socketD}
                            size={30}
                            speedMultiplier={0.2}
                            className="pb-2"
                        />
                    )}
                    <p className="text-2xl text-center">Oddness</p>
                </div>
            </motion.div>
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
