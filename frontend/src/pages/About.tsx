// components
import Page from '../components/Page';
import { motion } from 'framer-motion';

const About: React.FC = () => {
    const abouts = [
        'Do not refresh the page after sending an email',
        'Avoid emailing personal data',
        "Odder = Riskier. But our odd-meter isn't perfect - stay alert!",
        'Analyse is made using  Google Safe Browsing API, OpenAI GPT-3.5 Turbo, and our secret sauce (sike, since it’s open source)',
        "We don't store emails or any info - all deleted after analysis",
        "Admins can peek at emails for 30s, but won't because... well, ethics!",
        'Free? Yup, for now',
        'Favorite series?  TBBT ',
    ];

    return (
        <Page title='About' className='overflow-hidden'>
            <motion.div
                className='relative flex flex-col py-20 mx-auto w-11/12 xl:w-8/12 bg-primary bg-opacity-10 backdrop-blur-sm rounded-lg p-6 mt-16 border-dashed border-2 border-white text-white'
                initial={{ opacity: 0, scale: 0.4 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{
                    duration: 1,
                    type: 'spring',
                    bounce: 0.2,
                }}
            >
                <ul className='list-disc list-inside'>
                    {abouts.map((about, index) => (
                        <motion.li
                            className='text-2xl mb-4 p-1 px-4'
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{
                                duration: 0.6,
                                delay: 0.4 + index * 0.1,
                            }}
                            key={index}
                        >
                            {about}
                        </motion.li>
                    ))}
                </ul>
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

export default About;
