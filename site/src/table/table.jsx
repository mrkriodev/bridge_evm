import { Component } from "react";

import { FcCheckmark, FcClock } from 'react-icons/fc';

import "./table.css";

export default class Table extends Component {
    constructor(props) {
        super(props);

        this.state = {
            URL: props.URL,
            Items: props.Items
        };
    }

    async componentDidMount () {
        const Items = await this.loadData();
        this.setState(() => ({ Items }));
    }

    async loadData() {
        const {URL} = this.state; 
        let res = await fetch(URL);
        return res.json();
    }

    render() {
        const {Items} = this.state;
        console.log(Items);

        return (
            <table>
                <thead>
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
                {Items && Items.map((value, key) => {
                    return (
                        <tr key = {key} className = "Item">
                            <td>{value["status"] === "Transfer in" || value["status"] === "Transfer out" ? <FcCheckmark />:<FcClock />}</td>
                            <td>{value["status"]}</td>
                        </tr>
                    );
                })}
                </tbody>
            </table>
        );
    }
}