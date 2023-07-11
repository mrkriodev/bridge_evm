import React from 'react';
import ReactDOM from 'react-dom/client';

import "./index.css";
import App from "./app";

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        {/* <App URL = "http://92.255.109.253:8081/api/status" /> */}
        <App URL = "http://127.0.0.1:8000/api/status" />
    </React.StrictMode>
);