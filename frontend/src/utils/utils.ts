const getIdFromStorage = () => {
	return localStorage.getItem('omg_id');
}

const setIdToStorage = (id: string | null) => {
	if (!id) {
		localStorage.removeItem('omg_id');
		return;
	}
	localStorage.setItem('omg_id', id);
}

export {
	getIdFromStorage,
	setIdToStorage
}