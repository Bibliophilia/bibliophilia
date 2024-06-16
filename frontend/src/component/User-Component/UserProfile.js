
import { getUserProfile } from '../Component-APIs/googleAuthAPI';
import React, { useEffect, useState } from 'react';
import '../User-Component/Style/UserProfile.css'

const UserProfile = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                const userData = await getUserProfile();
                setUser(userData);
                setLoading(false);
            } catch (error) {
                console.error('Failed to fetch user profile:', error);
                setLoading(false);
            }
        };

        fetchUserProfile();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!user) {
        return <div>Error loading user profile.</div>;
    }

    return (
        <div className="UserProfile">
            <div className="profile-container">
                <img src={user.picture || '/path/to/default/profile.png'} alt="User Profile" className="profile-pic" />
                <h1>{user.name}</h1>
                <p>Email: {user.email}</p>
            </div>
        </div>
    );
};

export default UserProfile;
