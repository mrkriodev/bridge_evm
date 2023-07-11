import { Component } from "react";
import { FcCheckmark, FcClock } from 'react-icons/fc';
import { FaEthereum } from "react-icons/fa";
import Sber from "../img/sber.png";

import "./table.css";

export default class Table extends Component {

    constructor(props) {
        super(props);

        this.state = {
            ChainID: null
        };
    }

    async RefreshChainIDState() {
        this.setState ({
            ChainID: await window.ethereum.request({ method: 'eth_chainId' })
        });
    }

    async componentDidMount() {
        await this.RefreshChainIDState();
    }

    render() {
        const {Items} = this.props;
        const {ChainID} = this.state;
        const SberLogo = <img src = {Sber} alt = "Sber logo" width = "20px" height = "20px" />;

        return (
            <table>
                <thead>
                    <tr>
                        <td className = "TableHeaderName">Status</td>
                        <td className = "TableHeaderName">Address</td>
                        <td className = "TableHeaderName">{ChainID === 111111 ? SberLogo : <FaEthereum/>}</td>
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