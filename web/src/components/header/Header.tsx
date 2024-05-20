import React, { useState, useEffect } from 'react';
import './Header.css';

export default function Header() {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

    // TODO - isLoggedIn should be set without having to reload page
    useEffect(() => {
        setIsLoggedIn(localStorage.getItem('token') !== null && localStorage.getItem('token') !== "");
    }, []);

    return (
        <header>
            <div className="logo">
                <a href="/">Logo</a>
            </div>
            <div className="login">
                <a href={isLoggedIn ? "/logout" : "/login"}>
                    {isLoggedIn ? "Logout" : "Login"}
                </a>
            </div>
        </header>
    );
}

