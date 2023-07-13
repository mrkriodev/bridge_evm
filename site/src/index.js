import React from 'react';
import ReactDOM from 'react-dom/client';

import "./index.css";
import App from "./app";

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <App URL = {process.env.REACT_APP_API_ADDRESS} />
    </React.StrictMode>
);