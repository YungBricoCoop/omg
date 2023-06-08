import React from 'react';
import ReactDOM from 'react-dom/client';
import Router from './pages/Router';
import './css/index.css';

// react query
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
        <QueryClientProvider client={queryClient}>
            <Router />
        </QueryClientProvider>
    </React.StrictMode>
);
