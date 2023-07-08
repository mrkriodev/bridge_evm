import { Component } from "react";
import Table from "./table";

import "./menu.css";

export default class Menu extends Component {
    constructor(props) {
        super(props);

        this.state = {
            URL: props.URL,
            Items: null,
            IsFetching: true,
            IsValid: true,
            Error: null,
        };
    }

    async componentDidMount() {
        const {URL} = this.state;
        let Response = await fetch(URL);
        let Items = await Response.json();  

        this.setState({
            URL: URL,
            IsFetching: false,
            IsValid: true,
            Items: Items,
            Error: null
        });
    }

    RefreshTransactions(URL) {
        if(this.state.IsValid) {
            return;
        }

        fetch(URL)
        .then(data => data.json())
        .then(data => this.setState ({
            Items: data,
            IsFetcing: false,
            IsValid: true,
            Error: null
        }))
        .catch(error => {
            console.log(error);

            this.setState ({
                Items: null,
                IsFetching: false,
                IsValid: true,
                Error: error
            });
        });
    }

    FilterPendingTransactions() {
        let {URL, Items, IsFetching, Error} = this.state;
        let CachedSize = Items.length;
        Items = Items.filter(Item => Item.status.toLowerCase() === "pending");

        this.setState({
            URL: URL,
            Items: Items,
            IsFetching: IsFetching,
            IsValid: CachedSize === Items.length ? true : false,
            Error: Error
        });
    }

    render() {
        return (
            <div className = "Menu">
                <div className = "Header">
                    <div className = "LeftSide">
                        <button onClick = {this.RefreshTransactions.bind(this, this.state.URL)}>All Records</button>
                        <button onClick = {this.FilterPendingTransactions.bind(this)}>Pending</button>
                    </div>
                </div>
                <Table Items = {this.state.Items}/>
            </div>
        );
    }
}