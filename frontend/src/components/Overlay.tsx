// images
import grain from '../assets/grain.jpg';

const Overlay: React.FC = () => {
    return (
        <div
            className='fixed inset-0 pointer-events-none z-50 bg-no-repeat bg-fixed mix-blend-screen opacity-50'
            style={{ backgroundImage: `url(${grain})` }}
        />
    );
};

export default Overlay;
