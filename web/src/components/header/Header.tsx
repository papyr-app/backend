import React from 'react';

export default function Header() {
    function LoginLogout() {
        const token = localStorage.getItem('token');
        if (token) {
            return <a href="/logout">Logout</a>
        } else {
            return <a href="/login">Login</a>
        }
    }

    return (
        <header>
            <div className="logo">
                <a href="/">Logo</a>
            </div>
            <div className="content">
                <p>Some content here</p>
            </div>
            <div className="login">
                {LoginLogout()}
            </div>
        </header>
    )
}
