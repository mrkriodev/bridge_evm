import { Component } from "react";

import Table from "./table";
import "./menu.css";

export default class Menu extends Component {
    constructor(props) {
        super(props);

        this.state = {
            URL: props.URL
        };
    }

    render() {
        const {URL} = this.state;

        return (
            <div className = "Menu">
                <div className = "Header">
                    <div className = "LeftSide">
                        <button>All Records</button>
                        <button>Pending</button>
                    </div>
                </div>
                <Table URL = {URL}/>
            </div>
        );
    }
}