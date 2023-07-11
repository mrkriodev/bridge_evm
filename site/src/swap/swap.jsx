import { Component } from "react";

import { GiArchBridge, GiFox } from "react-icons/gi";
import { FaEthereum } from "react-icons/fa";
import { BsFillArrowRightSquareFill } from "react-icons/bs";
import Sber from "../img/sber.png";

import "./swap.css";

export default class Swap extends Component {
    constructor(props) {
        super(props);

        this.state = {
            To: null,
            Amount: null,
            Success: false,
            ErrorState: null,
            MetamaskAddress: props.MetamaskAddress
        };

        this.ErrorState = "";
    }

    async SetErrorMessage(Message) {
        let {To, Amount, MetamaskAddress} = this.state;
        this.setState ({
            To: To,
            Amount: Amount,
            Success: false,
            ErrorState: Message,
            MetamaskAddress: MetamaskAddress
        });
        
        setTimeout(this.setState.bind(this), 5000, {
            To: To,
            Amount: Amount,
            Success: false,
            ErrorState: null,
            MetamaskAddress: MetamaskAddress
        });
    }

    async HandleSwapClick(MetamaskAddress, To, Amount) {
        console.log(`Preparing for transaction. Arguments are: ${MetamaskAddress} ${To} ${Amount}`);

        if(MetamaskAddress === undefined || MetamaskAddress === null) {
            let Message = `Invalid "From" address: ${MetamaskAddress}`;
            console.log(Message);
            await this.SetErrorMessage(Message);

            return;
        }

        if(To === undefined || To === null) {
            let Message = `Invalid "To" address: ${To}`;
            console.log(Message);
            await this.SetErrorMessage(Message);

            return;
        }

        if(MetamaskAddress === To) {
            let Message = "You can not transfer to yourself";
            console.log(Message);
            await this.SetErrorMessage(Message);

            return;
        }

        if(To.length !== 42) {
            let Message = `"To" has invalid size: ${To.length}`;
            console.log(Message);
            await this.SetErrorMessage(Message);

            return;
        }

        if(MetamaskAddress.length !== 42) {
            let Message = `"From" has invalid size: ${MetamaskAddress.length}`;
            console.log(Message);
            await this.SetErrorMessage(Message);

            return;
        }

        if(Amount === null || Amount === undefined || Amount === 0) {
            let Message = `"Amount" has invalid value: ${Amount}`;
            console.log(Message);
            await this.SetErrorMessage(Message);

            return;
        }

        this.setState ({
            To: To,
            Amount: Amount,
            Success: true,
            ErrorState: "Preparing",
            MetamaskAddress: MetamaskAddress
        });

        // 0x0466B5ccccE6c334331f3fB08a5ff26c29B5E7eA
        let DeniedMessage = "MetaMask Tx Signature: User denied transaction signature.";

        window.ethereum
        .request ({
            method: 'eth_sendTransaction',
            params: [
                {
                    from: MetamaskAddress,
                    to: To,
                    value: (Number(Amount) * Math.pow(10, 18)).toString(16),
                    gasLimit: '0x5028',
                    maxPriorityFeePerGas: '0x3b9aca00',
                    maxFeePerGas: '0x2540be400',
                },
            ]
        })
        .then(TransactionHash => {
            console.log("Successfull tx-n");

            this.setState ({
                To: To,
                Amount: Amount,
                Success: true,
                ErrorState: "Success!",
                MetamaskAddress: MetamaskAddress
            });
        })
        .then(() => {
            this.props.SuccessProps();
        })
        .catch(Error => this.SetErrorMessage(Error.message === DeniedMessage ? "Rejected by user" : Error.message));
    }

    async HandleMetamaskConnect() {
        let AvailableAccounts = await window.ethereum.request ({
            method: 'wallet_requestPermissions',
            params: [{ eth_accounts: {} }]
        })
        .catch(Error => this.SetErrorMessage(Error.message));

        AvailableAccounts = AvailableAccounts === null || AvailableAccounts === undefined ? [null] : AvailableAccounts[0].caveats[0].value[0];
        let {To, Amount, Success, ErrorState} = this.state;
        this.setState ({
            To: To,
            Amount: Amount,
            Success: Success,
            ErrorState: ErrorState,
            MetamaskAddress: AvailableAccounts
        });
    }

    render() {
        let {MetamaskAddress, To, Amount, ErrorState, Success} = this.state;

        return (
            <div className = "SwapMenu">
                <div className = "AllInputs">
                    <div className = "InputFields">
                        <input value = {MetamaskAddress} type = "text" className = "InputField" placeholder = "From" readOnly/>
                        {
                            Success ? <GiArchBridge className = "Bridge" /> : <BsFillArrowRightSquareFill className = "Arrow"/>
                        }
                        <input onChange = {Event => {
                            let {Amount, MetamaskAddress} = this.state;

                            this.setState ({
                                To: Event.target.value,
                                Amount: Amount,
                                MetamaskAddress: MetamaskAddress
                            });
                        }} value = {To === null ? "" : To} type = "text" className = "InputField" placeholder = "To" />
                    </div>
                    <input onChange = {Event => {
                        let {To, MetamaskAddress} = this.state;

                        this.setState ({
                            To: To,
                            Amount: Event.target.value,
                            MetamaskAddress: MetamaskAddress
                        });
                    }} value = {Amount === null ? "" : Amount} type = "number" placeholder = "Amount" className = "AmountInput" />
                </div>
                <p className = { Success ? "ErrorFieldGreen" : "ErrorFieldRed"} >{ErrorState}</p>
                <div className = "Buttons">
                    <button className = "SwapButton" onClick = {this.HandleSwapClick.bind(this, MetamaskAddress, To, Amount)} type = "button">Swap<FaEthereum/></button>
                    <button className = "ConnectMetamaskButton" onClick = {this.HandleMetamaskConnect.bind(this)} type = "button">Connect<GiFox/></button>
                </div>
            </div>
        );
    }
};