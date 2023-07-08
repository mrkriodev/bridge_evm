import { Component } from "react";
import { FcCheckmark, FcClock } from 'react-icons/fc';

import "./table.css";

export default class Table extends Component {
    render() {
        const {Items} = this.props;

        return (
            <table>
                <thead>
                    <tr>
                        {
                            [
                                "Status",
                                "Time",
                                "From",
                                "Sending Amount & Address",
                                "Receiving Amount & Address",
                                "To"
                            ].map((value, key) => {
                                return (
                                    <td key = {key}>{value}</td>
                                );
                            })
                        }
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