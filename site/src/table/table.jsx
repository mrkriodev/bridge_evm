import { Component } from "react";
import { FcCheckmark, FcClock } from 'react-icons/fc';
import { BsFillArrowRightSquareFill, BsFillArrowLeftSquareFill } from "react-icons/bs";
import { FaEthereum } from "react-icons/fa";
import Sber from "../img/sber.png";

import "./table.css";

export default class Table extends Component {
    render() {
        const {Items} = this.props;
        const SberLogo = <img src = {Sber} alt = "Sber logo" width = "20px" height = "20px" />;

        return (
            <table>
                <thead>
                    <tr>
                        <td className = "TableHeaderName">Status</td>
                        <td className = "TableHeaderName">Address</td>
                        <td className = "TableHeaderName"><FaEthereum/></td>
                        <td></td>
                        <td className = "TableHeaderName">{SberLogo}</td>
                        <td className = "TableHeaderName">Signs</td>
                        <td className = "TableHeaderName">Amount</td>
                    </tr>
                </thead>
                <tbody>
                {Items && Items.map((value, key) => {
                    return (
                        <tr key = {key}>
                            <td key = {key}>{value.success === false ? <FcClock /> : <FcCheckmark />}</td>
                            <td key = {key}><input className = "Field" value = {value.address} readOnly/></td>
                            <td key = {key}><input className = "Field" value = {value.hash_from} readOnly/></td>
                            {
                                value.direction === 1 ? <td key = {key} className = "Arrow"><BsFillArrowLeftSquareFill/></td> : <td key = {key} className = "Arrow"><BsFillArrowRightSquareFill/></td>
                            }
                            <td key = {key}><input className = "Field" value = {value.hash_to} readOnly/></td>
                            <td key = {key}><input className = "Field" value = {value.signs} readOnly/></td>
                            <td key = {key}><input className = "Field" value = {value.amount + " ETH"} readOnly/></td>
                        </tr>
                    );
                })}
                </tbody>
            </table>
        );
    }
}