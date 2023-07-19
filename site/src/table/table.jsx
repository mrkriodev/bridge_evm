import { Component } from "react";
import { FcCheckmark, FcClock } from 'react-icons/fc';
import { BsFillArrowRightSquareFill, BsFillArrowLeftSquareFill } from "react-icons/bs";
import { FaEthereum } from "react-icons/fa";
import Sber from "../img/sber.png";

import "./table.css";

export default class Table extends Component {
    render() {
        const {Items, ChainID} = this.props;
        const SberLogo = <img src = {Sber} alt = "Sber logo" width = "20px" height = "20px" />;

        // {
        //     "status": false,
        //     "signs": 0,
        //     "direction": 1,
        //     "amount": 1123,
        //     "address": "",
        //     "hash_to": "",
        //     "hash_from": ""
        // }

        return (
            <table>
                <thead>
                    <tr>
                        <td className = "TableHeaderName">Status</td>
                        <td className = "TableHeaderName">Address</td>
                        <td className = "TableHeaderName">{ChainID === 111111 ? SberLogo : <FaEthereum/>}</td>
                        <td></td>
                        <td className = "TableHeaderName">{ChainID === 111111 ? <FaEthereum/> : SberLogo}</td>
                        <td className = "TableHeaderName">Signs</td>
                        <td className = "TableHeaderName">Amount</td>
                    </tr>
                </thead>
                <tbody>
                {Items && Items.map((value, key) => {
                    return (
                        <tr key = {key}>
                            <td key = {key}>{value["Status"] === "Pending" ? <FcCheckmark /> : <FcClock />}</td>
                            <td key = {key}><input className = "Field" value = {value["Address"]} readOnly/></td>
                            <td key = {key}><input className = "Field" value = {value["From"]} readOnly/></td>
                            {
                                value["Direction"] === 1 ? <td key = {key} className = "Arrow"><BsFillArrowLeftSquareFill/></td> : <td key = {key} className = "Arrow"><BsFillArrowRightSquareFill/></td>
                            }
                            <td key = {key}><input className = "Field" value = {value["To"]} readOnly/></td>
                            <td key = {key}><input className = "Field" value = {value["Signs"]} readOnly/></td>
                            <td key = {key}><input className = "Field" value = {value["Amount"] + " ETH"} readOnly/></td>
                        </tr>
                    );
                })}
                </tbody>
            </table>
        );
    }
}