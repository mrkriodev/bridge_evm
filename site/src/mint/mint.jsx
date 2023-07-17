import { Component } from "react";
import { SiBuymeacoffee } from "react-icons/si";
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
        this.ContractAddress = "0x3A3d22cB1dE38DF3819f0C41261EeaF0141d7871";
        this.ContractABI = ContractJSON.output.abi;
        console.log(this.ContractABI);

        const web3 = new Web3(window.ethereum);

        this.Contract = new web3.eth.Contract (
            this.ContractABI,
            this.ContractAddress
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

        let TransactionHash = await this.Contract.methods.MakeCoffee(To).send ({
            from: FirstAddress
        }).catch(Error => console.error(Error.message));

        if(TransactionHash === null || TransactionHash === undefined) {
            console.log("Transaction failed");
            return;
        }
          
        console.log(TransactionHash.transactionHash);
        return;
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
                <button onClick = {this.ClickHandler.bind(this)} className = "Button">Buy me a Coffee<SiBuymeacoffee className = "Coffee" /></button>
            </div>
        );
    }
}