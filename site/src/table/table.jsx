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
                                "Signs",
                                "From hash",
                                "To hash",
                                "Address",
                                "Amount"
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
                            <td>{value["Status"] === "Pending" ? <FcCheckmark /> : <FcClock />}</td>
                            <td><input className = "Field" value = {value["Signs"]} readOnly/></td>
                            <td><input className = "Field" value = {value["From"]} readOnly/></td>
                            <td><input className = "Field" value = {value["To"]} readOnly/></td>
                            <td><input className = "Field" value = {value["Address"]} readOnly/></td>
                            <td><input className = "Field" value = {value["Amount"] + " ETH"} readOnly/></td>
                        </tr>
                    );
                })}
                </tbody>
            </table>
        );
    }
}