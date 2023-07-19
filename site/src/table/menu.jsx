import { Component } from "react";
import { BsFillArrowLeftSquareFill } from "react-icons/bs";
import Table from "./table";

import "./menu.css";

// Do not change items in this list
const SortBy = [
    "By ID",
    "Accending Amount",
    "Discending Amount"
];

let PagesCount = 13;
let CurrentPage = 5;
let ChangedByFinder = false;

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

    GenerateArray(From, To) {
        let Result = Array.from({length: To - From});

        for(let Iter = From; Iter < To; Iter += 1) {
            Result[Iter - From] = Iter;
        }
        return Result;
    }

    render() {
        return (
            <div className = "Menu">
                <div className = "Header">
                    <div className = "LeftSide">
                        <button onClick = {() => {
                            this.props.SetProps(false);
                            console.log("button");
                        }}><BsFillArrowLeftSquareFill/> Back</button>
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
                <Table Items = {this.state.Items} ChainID = {this.props.ChainID} CurrentPage = {CurrentPage}/>
                <div className = "BottomMenu">
                    <div className = "FindSpecific">
                        <input placeholder = "find specific" type = "number" onChange = {(Event) => {
                            let Value = Event.target.value;

                            if(Value.length === 0) { 
                                return;
                            }
                            
                            if(typeof Value === "string") {
                                Value = Number(Value, 10);
                            }

                            if(Value > PagesCount) {
                                CurrentPage = PagesCount;
                                return;
                            }

                            if(Value < 0) {
                                CurrentPage = 1;
                                return;
                            }

                            CurrentPage = Value;
                            ChangedByFinder = true;
                        }}/>
                    </div>

                    <div className = "EnumeratedPages">
                        <button onClick = {() => {
                            CurrentPage = 1;
                            ChangedByFinder = false;
                        }} className = "ButtonFirstLastPage">first</button>
                        {
                            !ChangedByFinder ? (
                                (PagesCount - CurrentPage + 1) > 6 ? (
                                    this.GenerateArray(CurrentPage, PagesCount + 1).map(Item => {
                                        if(Item === PagesCount) {
                                            return <button onClick = {() => {
                                                CurrentPage = Item;
                                                ChangedByFinder = false;
                                            }} className = "PageItem">{Item}</button>;
                                        }
                                        if(Item === PagesCount - 3) {
                                            return <p>...,&nbsp;</p>;
                                        }

                                        else if(Item < CurrentPage + 3) {
                                            return <button onClick = {() => {
                                                CurrentPage = Item;
                                                ChangedByFinder = false;
                                            }} className = "PageItem">{Item},&nbsp;</button>;
                                        }
                                        else if(Item > PagesCount - 3) {
                                            return <button onClick = {() => {
                                                CurrentPage = Item;
                                                ChangedByFinder = false;
                                            }} className = "PageItem">{Item},&nbsp;</button>;
                                        }
                                    })
                                ) : (
                                    this.GenerateArray(CurrentPage, PagesCount + 1).map(Item => {
                                        if(Item === PagesCount) {
                                            return <button onClick = {() => {
                                                CurrentPage = Item;
                                                ChangedByFinder = false;
                                            }} className = "PageItem">{Item}</button>;
                                        }
                                        else {
                                            return <button onClick = {() => {
                                                CurrentPage = Item;
                                                ChangedByFinder = false;
                                            }} className = "PageItem">{Item},&nbsp;</button>;
                                        }
                                    })
                                )
                            ) : (
                                <button onClick = {() => {
                                    CurrentPage = CurrentPage;
                                    ChangedByFinder = true;
                                }} className = "PageItem">{CurrentPage}</button>
                            )
                        }
                        <button onClick = {() => {
                            CurrentPage = PagesCount;
                            ChangedByFinder = false;
                        }} className = "ButtonFirstLastPage">last</button>
                    </div>
                </div>
            </div>
        );
    }
}