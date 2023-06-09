// react
import { useEffect } from 'react';

// functions
import { getIdFromStorage } from '../utils/utils';
import { useQueryClient } from '@tanstack/react-query';

const useReactQuerySubscription = () => {
    const queryClient = useQueryClient();
    const id = getIdFromStorage();
    useEffect(() => {
        if (!id) return;
        const url = import.meta.env.VITE_HOSTNAME
            ? `wss://${import.meta.env.VITE_HOSTNAME}/ws/${id}`
            : `ws://localhost:8000/ws/${id}`;
        const websocket = new WebSocket(url);
        websocket.onopen = () => {
            console.log('connected');
        };
        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            queryClient.setQueryData(['websocket'], data);
        };

        return () => {
            websocket.close();
        };
    }, [queryClient, id]);
};

export default useReactQuerySubscription;
