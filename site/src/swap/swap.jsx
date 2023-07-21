import { Component } from "react";

import { GiArchBridge, GiFox } from "react-icons/gi";
import { FaEthereum } from "react-icons/fa";
import { BsFillArrowRightSquareFill } from "react-icons/bs";
import { SiBuymeacoffee } from "react-icons/si"
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
        console.log(`Got: ${this.props.InjectedProvider}`);

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

    async HandleSwapClick(MetamaskAddress, Amount) {
        const SiberToEth = "0x6d7e26774aB7cEf9EE9Ca55CB7BA5922605DD182";
        const EthToSiber = "0x0466B5ccccE6c334331f3fB08a5ff26c29B5E7eA";
        let __ChainID = await window.ethereum.request({ method: 'eth_chainId' });
        let Image = <img src = {Sber} alt = "Sber logo" width = "20px" height = "20px" />;
        __ChainID = Number(__ChainID, 10);

        let To;
        if(__ChainID === 111000) {
            To = SiberToEth;

            if(Amount < 0.001) {
                await this.SetErrorMessage (
                    <div className = "CommissionsItem">
                        {Image}                    
                        <BsFillArrowRightSquareFill className = "ColorGray"/>
                        <FaEthereum />
                        <p>requires min</p>
                        <p>0.001</p>
                    </div>
                );
                return;
            }
        } else if (__ChainID === 5) {
            To = EthToSiber;

            if(Amount < 0.09) {
                await this.SetErrorMessage (
                    <div className = "CommissionsItem">
                        <FaEthereum />
                        <BsFillArrowRightSquareFill className = "ColorGray"/>
                        {Image}
                        <p>requires min</p>
                        <p>0.09</p>
                    </div>
                );
                return;
            }
        } else {
            await this.SetErrorMessage("Unknown network");
            return;
        }

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
        let {InjectedProvider} = this.props;
        console.log(`Injected provider is ${InjectedProvider}`)
        if(!InjectedProvider) {
            this.SetErrorMessage("Please install metamask or reload");
            return;
        }

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
        let {MetamaskAddress, Amount, ErrorState, Success} = this.state;
        let Image = <img src = {Sber} alt = "Sber logo" width = "20px" height = "20px" />;
        let {InjectedProvider, ChainID} = this.props;

        return (
            <div className = "SwapMenu">
                <div className = "AllInputs">
                    <div className = "InputFields">
                        <input value = {MetamaskAddress} type = "text" className = "InputField" placeholder = "Connect MetaMask" readOnly/>
                        {
                            Success ? <GiArchBridge className = "Bridge" /> : <BsFillArrowRightSquareFill className = "Arrow"/>
                        }
                        {
                            InjectedProvider ? (ChainID === 111111 || ChainID === 111000? <FaEthereum /> : Image) : Image
                        }
                    </div>
                    <input onChange = {Event => {
                        let {To, MetamaskAddress} = this.state;

                        this.setState ({
                            To: To,
                            Amount: Event.target.value,
                            MetamaskAddress: MetamaskAddress
                        });
                    }} value = {Amount === null ? "" : Amount} type = "number" placeholder = "Amount + 9%" className = "AmountInput" />
                </div>
                <p className = { Success ? "ErrorFieldGreen" : "ErrorFieldRed"} >{ErrorState}</p>
                <div className = "AllButtons">
                    <div className = "Buttons">
                        <button className = "ConnectMetamaskButton" onClick = {this.HandleMetamaskConnect.bind(this)} type = "button">Connect<GiFox/></button>
                        <button className = "SwapButton" onClick = {this.HandleSwapClick.bind(this, MetamaskAddress, Amount)} type = "button">Swap<FaEthereum/></button>
                    </div>
                    <button onClick = {() => {
                        if(MetamaskAddress === null || MetamaskAddress === undefined) {
                            let Message = `Invalid "From" address: ${MetamaskAddress}`;
                            console.log(Message);
                            this.SetErrorMessage(Message);
                            return;
                        }
                
                        this.props.SetBuyCoffee();
                    }} className = "BuyMeCoffee">Buy me a Coffee<SiBuymeacoffee className = "Coffee" /></button>
                </div>
            </div>
        );
    }
};