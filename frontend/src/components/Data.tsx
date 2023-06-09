// components
import { motion } from 'framer-motion';

// interfaces
interface DataProps {
    title: string;
    value: string | Array<string>;
}

const Data: React.FC<DataProps> = ({ title, value }) => {
    const isString = typeof value === 'string';

    return (
        <motion.div
            className="flex flex-col gap-0 text-white"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{
                duration: 1,
                type: 'spring',
                bounce: 0.2,
            }}
        >
            <p className="underline text-lg">{title}</p>
            <motion.p
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                key={`data-${value}`}
            >
                {isString && value}
                {!isString &&
                    value.map((v) => (
                        <>
                            {v}
                            <br />
                        </>
                    ))}
            </motion.p>
        </motion.div>
    );
};

export default Data;
