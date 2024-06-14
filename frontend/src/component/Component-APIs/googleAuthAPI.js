// GoogleAuthAPI.js

const registerWithGoogle = async (googleResponse) => {
    try {
        window.location.href = 'http://localhost:8000/users/session/login';

    } catch (error) {
        console.error('Error registering with Google:', error.message);
        throw error;
    }
};


export { registerWithGoogle};
