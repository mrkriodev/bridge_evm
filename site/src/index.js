import React from 'react';
import ReactDOM from 'react-dom/client';

import "./index.css";
import Menu from "./table/menu";

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <div className = "Page">
            <h1 className = "Logotype">Bridge Records</h1>
            <Menu URL = "http://127.0.0.1:8000/api/status" />
        </div>
    </React.StrictMode>
);