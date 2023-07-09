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
                                "Sending",
                                "Receiving",
                                "To"
                            ].map((value, key) => {
                                return (
                                    <td className = "TableHeaderName" key = {key}>{value}</td>
                                );
                            })
                        }
                    </tr>
                </thead>
                <tbody>
                {Items && Items.map((value, key) => {
                    return (
                        <tr key = {key} className = "Items">
                            <td>{value["Status"] === "Transfer in" || value["Status"] === "Transfer out" ? <FcCheckmark />:<FcClock />}</td>
                            <td>{value["Status"]}</td>
                            <td>{value["From"]}</td>
                            <td>{value["Sending"]}</td>
                            <td>{value["Receiving"]}</td>
                            <td>{value["To"]}</td>
                        </tr>
                    );
                })}
                </tbody>
            </table>
        );
    }
}