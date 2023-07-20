import { Component } from "react";
import { SiBuymeacoffee } from "react-icons/si";
import { BsFillArrowLeftSquareFill } from "react-icons/bs";
import ContractJSON from "./MintContractABI.json";
import Web3 from "web3";
import "./mint.css";


export default class Mint extends Component {
    constructor(props) {
        super(props);

        this.state = {
            FirstAddress: this.props.FirstAddress,
            Message: null,
            To: null,
        };
    }

    async componentDidMount() {
        this.EthereumContractAddress = "0x680E69174388dC802903ac5542c1A4C7b6307c0f";
        this.SiberiumContractAddress = "0x2b5c46787e24300f8A0Ea28071A74e8B5E1c80DF";

        this.ContractABI = ContractJSON.output.abi;

        const web3 = new Web3(window.ethereum);

        this.EthereumContract = new web3.eth.Contract (
            this.ContractABI,
            this.EthereumContractAddress
        );
        this.SiberiumContract = new web3.eth.Contract (
            this.ContractABI,
            this.SiberiumContractAddress
        );
        this.web3 = web3;
    }

    async SetErrorMessage(Message) {
        this.setState ({
            ...this.state, Message: Message
        });

        setTimeout(this.setState.bind(this), 5000, {
            ...this.state, Message: null
        });
    }

    async ClickHandler() {
        let {FirstAddress, To} = this.state;
        console.log(`Preparing transaction with args: ${FirstAddress} ${To}`);

        if(FirstAddress === null || FirstAddress === undefined) {
            let ErrorMessage = `From is ${FirstAddress}`;
            await this.SetErrorMessage(ErrorMessage);
            return;
        }

        if(To === null || To === undefined) {
            let ErrorMessage = `To is ${To}`;
            await this.SetErrorMessage(ErrorMessage);
            return;
        }

        if(To.length !== 42) {
            let ErrorMessage = `To has invalid len ${To.lengt}`;
            await this.SetErrorMessage(ErrorMessage);
            return;
        }

        if(FirstAddress.length !== 42) {
            let ErrorMessage = `From has invalid len ${FirstAddress.lengt}`;
            await this.SetErrorMessage(ErrorMessage);
            return;
        }
        
        let __ChainID = await window.ethereum.request({ method: 'eth_chainId' });
        __ChainID = Number(__ChainID, 10);
        console.log(`Current chain ID: ${__ChainID} type ${typeof __ChainID}`);

        let TransactionHash;
        if(__ChainID === 111000) {
            TransactionHash = await this.EthereumContract.methods.MakeCoffee (
                To,
                "https://ipfs.io/ipfs/QmVogCkh5ezJ9j68tXWcYVPGkWXQU9MBXbtN2h7Uxo5YGU?filename=coffee.json"
            ).send ({
                from: FirstAddress
            }).catch(Error => console.error(Error.message));

        } else if(__ChainID === 5) {
            TransactionHash = await this.EthereumContract.methods.MakeCoffee (
                To,
                "https://ipfs.io/ipfs/QmVogCkh5ezJ9j68tXWcYVPGkWXQU9MBXbtN2h7Uxo5YGU?filename=coffee.json"
            ).send ({
                from: FirstAddress
            }).catch(Error => console.error(Error.message));
            
        } else {
            await this.SetErrorMessage("Invalid network");
            return;
        }

        if(TransactionHash === null || TransactionHash === undefined) {
            console.log("Transaction failed");
            return;
        }
        
        console.log(TransactionHash.transactionHash);
    }

    render() {
        return (
            <div className = "Form">
                <div className = "__InputFields">
                    <input className = "InputField" placeholder = "To" onChange = {Event => {
                        this.setState ({
                            ...this.state, To: Event.target.value
                        });
                    }} />
                </div>
                <div className = "BottomMintButtons">
                    <button onClick = {this.ClickHandler.bind(this)} className = "Button">Buy me a Coffee<SiBuymeacoffee className = "Coffee" /></button>
                    <button className = "MintBackButton" onClick = {() => {
                        this.props.SetCoffee(false);
                    }}><BsFillArrowLeftSquareFill className = "ArrowMarginer"/> Back</button>
                </div>
            </div>
        );
    }
}