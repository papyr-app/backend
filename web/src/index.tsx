import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Outlet } from 'react-router-dom';
import Header from '@components/header/Header';
import Home from '@routes/home/Home';
import Login from '@routes/login/Login';
import Logout from '@routes/logout/Logout';
import Register from '@routes/register/Register';
import PageNotFound from '@routes/page_not_found/PageNotFound';
import Workspace from '@routes/workspace/Workspace';
import UploadDocument from '@routes/upload_document/UploadDocument';
import GrantAccess from '@routes/grant_access/GrantAccess';
import reportWebVitals from './reportWebVitals';
import './global.scss';

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);
root.render(
    <React.StrictMode>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<><Header /><Outlet /></>}>
                    <Route path="/" element={<Home />} />
                    <Route path="/document/new" element={<UploadDocument />} />
                    <Route path="/document/:documentId" element={<Workspace />} />
                    <Route path="/share" element={<GrantAccess />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/logout" element={<Logout />} />
                    <Route path="*" element={<PageNotFound />} />
                </Route>
            </Routes>
        </BrowserRouter>
    </React.StrictMode>
);

reportWebVitals();
