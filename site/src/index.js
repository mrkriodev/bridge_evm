import React from 'react';
import ReactDOM from 'react-dom/client';

import "./index.css";
import Table from "./components/table/table";

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <div className = "Page">
            <h1 className = "Logotype" color = "white">Bridge Viewer</h1>
            <Table />
        </div>
    </React.StrictMode>
);