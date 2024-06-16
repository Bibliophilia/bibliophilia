
const registerWithGoogle = async (googleResponse) => {
    try {
        window.location.href = 'http://localhost:8000/users/session/login';

    } catch (error) {
        console.error('Error registering with Google:', error.message);
        throw error;
    }
};




// getting user info



const getUserProfile = async () => {
    try {
        const response = await fetch('http://localhost:8000/users/session/get-user', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || 'Failed to fetch user profile');
        }
        return JSON.parse(data.user);  // Parse the user JSON string
    } catch (error) {
        console.error('Error fetching user profile:', error.message);
        throw error;
    }
};


export { registerWithGoogle, getUserProfile };