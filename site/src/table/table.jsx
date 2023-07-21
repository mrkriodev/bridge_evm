import { Component } from "react";
import { FcCheckmark, FcClock } from 'react-icons/fc';
import { BsFillArrowRightSquareFill, BsFillArrowLeftSquareFill } from "react-icons/bs";
import { FaEthereum } from "react-icons/fa";
import Sber from "../img/sber.png";

import "./table.css";

export default class Table extends Component {
    constructor(props) {
        super(props);

        this.state = {
            GlobalKey: 1
        };
    }

    render() {
        let {GlobalKey} = this.state;
        const {Items} = this.props;
        const SberLogo = <img src = {Sber} alt = "Sber logo" width = "20px" height = "20px" />;

        return (
            <table>
                <thead>
                    <tr>
                        <td>Status</td>
                        <td>Address</td>
                        <td><FaEthereum/></td>
                        <td></td>
                        <td>{SberLogo}</td>
                        <td>Signs</td>
                        <td>Amount</td>
                    </tr>
                </thead>
                <tbody>
                {Items && Items.map(value => {
                    return (
                        <tr key = {GlobalKey++} className = "TableRow">
                            <td key = {GlobalKey++}>{value.status === false ? <FcClock /> : <FcCheckmark />}</td>
                            <td key = {GlobalKey++}><input className = "Field" value = {value.address} readOnly/></td>
                            <td key = {GlobalKey++}><input className = "Field" value = {value.hash_from} readOnly/></td>
                            {
                                value.direction === 1 ? <td key = {GlobalKey++} className = "Arrow"><BsFillArrowLeftSquareFill/></td> : <td key = {GlobalKey++} className = "Arrow"><BsFillArrowRightSquareFill/></td>
                            }
                            <td key = {GlobalKey++}><input className = "Field" value = {value.hash_to} readOnly/></td>
                            <td key = {GlobalKey++}><input className = "Field" value = {value.signs} readOnly/></td>
                            <td key = {GlobalKey++}><input className = "Field" value = {value.amount + " ETH"} readOnly/></td>
                        </tr>
                    );
                })}
                </tbody>
            </table>
        );
    }
}