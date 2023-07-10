import React from 'react';
import ReactDOM from 'react-dom/client';

import "./index.css";
import App from "./app";

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App MenuLink = "92.255.109.253" URL = "http://92.255.109.253/api/status" />
    </React.StrictMode>
);