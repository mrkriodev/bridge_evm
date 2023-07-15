import { Component } from "react";
import { SiBuymeacoffee } from "react-icons/si"
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

    async SetErrorMessage(Message) {
        this.setState ({
            ...this.state, Message: Message
        });

        setTimeout(this.setState.bind(this), 5000, {
            ...this.state, Message: null
        });
    }

    async ClickHandler() {
        let {FirstAddress, Message, To} = this.state;
        console.log(`Preparing transaction with args: ${FirstAddress} ${Message} ${To}`);

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

        To = Number(To, 10);
        if(isNaN(To)) {
            let ErrorMessage = `To is not a number`;
            await this.SetErrorMessage(ErrorMessage);
            return;
        }

        if(FirstAddress.length !== 42) {
            let ErrorMessage = `From has invalid len ${FirstAddress.lengt}`;
            await this.SetErrorMessage(ErrorMessage);
            return;
        }

        
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
                    <span className = "Border" />
                    <input className = "InputField" placeholder = "Message" onChange = {Event => {
                        this.setState ({
                            ...this.state, Message: Event.target.value
                        });
                    }} />
                </div>
                <button onClick = {this.ClickHandler.bind(this)} className = "Button">Buy me a Coffee<SiBuymeacoffee className = "Coffee" /></button>
            </div>
        );
    }
}