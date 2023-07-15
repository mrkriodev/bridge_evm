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

    async ClickHandler() {
        let {FirstAddress, Message, To} = this.state;
        console.log(`this.state.FirstAddress ${FirstAddress} ${Message} ${To}`)
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
                    }}/>
                </div>
                <button onClick = {this.ClickHandler.bind(this)} className = "Button">Buy me a Coffee<SiBuymeacoffee className = "Coffee" /></button>
            </div>
        );
    }
}