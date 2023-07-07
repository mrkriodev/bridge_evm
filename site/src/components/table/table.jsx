import React, { Component } from "react";
import "./table.css";

export default class Table extends Component {
    constructor(props) {
        super(props);
        
        this.state = {
            url: "http://localhost:8000/api/status",
            items: null
        };
    }
  
    async componentDidMount () {
        const items = await this.loadData();
        this.setState(() => ({ items: items }));
    }

    async loadData () {
        const { url } = this.state;
        const resp = await fetch(url, {
            method: "GET",
            headers: {
                "content-type": "application/json",
                "Access-Control-Request-Method": "GET"
            },
            mode: 'no-cors'
        });
        return resp.json();
    }

    render() {
        const { items } = this.state;
        //console.log(items);
      
        return (
            <table>
                <thead className = "Header">
                    <tr>
                        <td>Status</td>
                        <td>Time</td>
                        <td>From</td>
                        <td>Sending Amount & Address</td>
                        <td>Receiving Amount & Address</td>
                        <td>To</td>
                    </tr>
                </thead>
                <tbody>
                    {items && items.map((value, key) => {
                        return (
                            <tr key={key}>
                                <td>{value}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        );
    }
}