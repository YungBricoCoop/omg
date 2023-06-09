export const BASE_URL = import.meta.env.VITE_HOSTNAME ? `https://${import.meta.env.VITE_HOSTNAME}` : 'http://localhost:8000';

const getId = async () => {
	return fetch(`${BASE_URL}/id`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
		},
	}).then((res) => res.json());
};

export { getId }