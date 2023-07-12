import { Component } from "react";
import Table from "./table";

import "./menu.css";

// Do not change items in this list
const SortBy = [
    "By ID",
    "Accending Amount",
    "Discending Amount"
];

let CachedItems;
let CachedKey;

export default class Menu extends Component {
    constructor(props) {
        super(props);

        this.state = {
            URL: props.URL,
            IsValid: false,
            Items: null,
            Error: null
        };
        this.Sorted = [];
    }

    async RefreshTransactions(URL) {
        fetch(URL)
        .then(data => data.json())
        .then(data => {
            this.setState({
                URL: URL,
                IsValid: true,
                Items: data,
                Error: null
            });

            CachedItems = {
                URL: URL,
                IsValid: true,
                Items: data,
                Error: null
            };
        })
        .catch(error => {
            console.log(error);

            if(CachedItems == null) {
                return;
            }
            let {__URL, __IsValid, __Items, __Error} = CachedItems;

            this.setState ({
                URL: __URL,
                IsValid: __IsValid,
                Items: __Items,
                Error: __Error
            });
        });

        return;
    }

    async componentDidMount() {
        const {URL} = this.state;
        await this.RefreshTransactions(URL);
    }
    
    async FilterPendingTransactions() {
        let {URL, Items, Error} = this.state;
        if(Items == null && Error != null) {
            this.setState ({
                URL: URL,
                Items: CachedItems,
                Error: null
            });
        }

        if(Items == null) {
            return;
        }

        Items = Items.filter(Item => Item.Status.toLowerCase() !== "pending");

        this.setState({
            URL: URL,
            Items: Items,
            Error: null
        });
    }

    async SortByTransactions(__key) {
        if(__key === CachedKey) {
            return;
        }
        CachedKey = __key;

        let {URL, Items} = this.state;
        if(Items == null && Error != null) {
            this.setState ({
                URL: URL,
                Items: CachedItems,
                Error: null
            });
        }

        if(Items == null) {
            return;
        }

        switch(__key) {
            case 0:
                console.log("ID");
                Items.sort((first, second) => {
                    return first.ID - second.ID;
                })
                break;

            case 1:
                console.log("Accending Amount");
                Items.sort((first, second) => {
                    return first.Amount - second.Amount;
                });
                break;

            case 2:
                console.log("Discending Amount");
                Items.sort((first, second) => {
                    return second.Amount - first.Amount;
                });
                break;

            default:
                console.log("unknown type of sort");
        }

        this.setState({
            URL: URL,
            Items: Items,
            Error: null,
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
                    <div className = "RightSize">
                        <div className = "SortBy">
                            <button className = "MenuTitle">Sort By</button>
                            <ul className = "MenuDropDown">
                                {
                                    SortBy.map((value, key) => {
                                        return <button onClick = {this.SortByTransactions.bind(this, key)} key = {key} className = "SortByElement">{value}</button>
                                    })
                                }
                            </ul>
                        </div>
                    </div>
                </div>
                <Table Items = {this.state.Items} ChainID = {this.props.ChainID}/>
            </div>
        );
    }
}