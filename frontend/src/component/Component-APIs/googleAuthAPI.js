// GoogleAuthAPI.js

const registerWithGoogle = async (googleResponse) => {
    try {
        window.location.href = 'http://localhost:8000/users/session/login';

    } catch (error) {
        console.error('Error registering with Google:', error.message);
        throw error;
    }
};
{/*
const getUserProfile = async () => {
    try {
        const response = await fetch('http://localhost:8000/users/session/get-user', {
            method: 'GET',
            headers: {
                'accept': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch user profile');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching user profile:', error.message);
        throw error;
    }
};
 */}

export { registerWithGoogle};
