import React, { useEffect, useState } from 'react';
import './Style/UserAuth.css';
import image1 from '../ComponentStyles/Img/Authors-Slide/image 4.png';
import image2 from '../ComponentStyles/Img/Authors-Slide/image 5.png';
import image3 from '../ComponentStyles/Img/Authors-Slide/images 1.png';
import image4 from '../ComponentStyles/Img/Authors-Slide/800px-Leon_tolstoi 1.png';
import image5 from '../ComponentStyles/Img/Authors-Slide/ErnestHemingway 1.png';
import image6 from '../ComponentStyles/Img/Authors-Slide/George_Charles_Beresford_-_Virginia_Woolf_in_1902_-_Restoration 1.png';
import image7 from '../ComponentStyles/Img/Authors-Slide/Oscar-Wilde-1882 1.png';
import image8 from '../ComponentStyles/Img/Authors-Slide/Rabindranath_Tagore_in_1909 1.png';
import image9 from '../ComponentStyles/Img/Authors-Slide/ts-eliot-fame-frustration-and-love 1.png';
import image10 from '../ComponentStyles/Img/Authors-Slide/Vasily_Perov_-_Портрет_Ф.М 1.png';
import google_log from '../ComponentStyles/Img/google logo/google logo 3.png';
import {registerWithGoogle} from "../Component-APIs/googleAuthAPI";


const images = [
    image6,
    image1,
    image3,
    image2,
    image8,
    image4,
    image5,
    image7,
    image9,
    image10
];


const LoginPopup = () => {
    const [currentSlide, setCurrentSlide] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentSlide((prevSlide) => (prevSlide + 1) % images.length);
        }, 3000);

        return () => clearInterval(interval);
    }, []);

    const handleLoginWithGoogle = async (googleResponse) => {
        try {
            // Call the registerWithGoogle function with the Google authentication response
            const data = await registerWithGoogle(googleResponse);
            // Optionally, handle the response data here
            console.log("Successfully registered with Google:", data);
        } catch (error) {
            // Handle any errors that occur during registration
            console.error("Failed to register with Google:", error.message);
        }
    };


    return (
        <div className="UserAuthContainer">

            <div className="title-container">
                <p className="title-login">Bibliophilia</p>
                <p className="sub-title-login">“ I have always imagined that Paradise will be a kind of library.” <br/>
                    - Jorge Luis Borges (Argentine writer and poet) </p>


                <img className="google-logo" src={google_log} alt="Google Logo"/>
            </div>


            <div className="sign-in-content">
                <button className="login-with-google-btn" onClick={handleLoginWithGoogle}>Login with Google</button>
            </div>

            <div className="sign-up-content">

                <p className="sign-up-description">You don't have account yet ? Register</p>

            </div>

            <div className="image-content">
                {images.map((image, index) => (
                    <img
                        key={index}
                        src={image}
                        alt={`Slide ${index}`}
                        className={index === currentSlide ? 'slide active' : 'slide behind'}
                        style={{
                            transform: `translateX(${(index - currentSlide) * 100}%)`,
                            transition: 'transform 0.5s ease'
                        }}
                    />
                ))}
            </div>


        </div>
    );
};


export default LoginPopup;

