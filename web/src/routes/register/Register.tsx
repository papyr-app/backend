import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { RegisterUser } from '@customTypes/user';
import api from '@api/index';
import './Register.scss';

export default function Register() {
    const [formData, setFormData] = useState<RegisterUser>({} as RegisterUser);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        const { name, value } = e.target;
        setFormData((prevFormData) => ({
            ...prevFormData,
            [name]: value,
        }));
    };

    async function handleRegister(e: React.FormEvent){
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            await api.auth.register(formData);
            navigate('/login');
        } catch (err) {
            setError('Registration failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='register-container'>
            <h2>Register</h2>
            <form className='form' onSubmit={handleRegister}>
                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="email">Email:</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="firstName">First Name:</label>
                    <input
                        type="text"
                        id="firstName"
                        name="firstName"
                        value={formData.first_name}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="lastName">Last Name:</label>
                    <input
                        type="text"
                        id="lastName"
                        name="lastName"
                        value={formData.last_name}
                        onChange={handleChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                    />
                </div>
                {error && <div className='error-message'>{error}</div>}
                <div className="form-group">
                    <button className='button-primary' type="submit" disabled={loading}>
                        {loading ? 'Registering...' : 'Register'}
                    </button>
                </div>
            </form>

            <div>
                <p>Already have an account? <a href="/login">Login</a></p>
            </div>
        </div>
    );
};
