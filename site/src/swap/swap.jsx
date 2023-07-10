import { Component } from "react";

import "./swap.css";

export default class Swap extends Component {
    constructor(props) {
        super(props);

        this.state = {
            MenuLink: props.MenuLink
        };
    }

    render() {
        return (
            <div className = "SwapMenu">
                <div className = "AllInputs">
                    <div className = "InputFields">
                        <input type = "text" className = "InputField" placeholder = "From" />
                        <span></span>
                        <input type = "text" className = "InputField" placeholder = "To" />
                    </div>
                    <input type = "number" placeholder = "Amount" className = "AmountInput" />
                </div>
                <button className = "SwapButton" onclick = "location.href='http://www.example.com'" type = "button">Swap</button>
            </div>
        );
    }
};