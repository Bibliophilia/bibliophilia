// GoogleAuthAPI.js

const registerWithGoogle = async (googleResponse) => {
    try {
        if (!googleResponse || !googleResponse.accessToken) {
            throw new Error('Google response or access token is missing');
        }

        const response = await fetch('http://localhost:8000/users/session/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ access_token: googleResponse.accessToken }),
        });

        if (!response.ok) {
            throw new Error('Failed to register with Google');
        }

        const data = await response.json();
        return data; // This can be further processed in the component
    } catch (error) {
        console.error('Error registering with Google:', error.message);
        throw error;
    }
};

export default registerWithGoogle;
