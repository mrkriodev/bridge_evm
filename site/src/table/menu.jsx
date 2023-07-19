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
let ChangedByFinder = false;

let CachedItems;
let CachedKey;

export default class Menu extends Component {
    constructor(props) {
        super(props);

        this.state = {
            CurrentPage: 1,
            URL: props.URL,
            IsValid: false,
            Items: null,
            Error: null
        };
        this.Sorted = [];
    }

    async componentDidMount() {
        const {URL} = this.state;
        let CachedItems = [
            {success: false},
            {success: true}
        ];

        this.setState ({ ...this.state, Items: CachedItems });
    }

    /*Fetch Data from specific page*/
    async GetPageItems(Page) {

    }

    /*Get Status of specific tr-n*/
    async GetItem(Number) {

    }

    /*Get Total count of tr-s*/
    async GetTotal() {
        
    }

    GenerateArray(From, To) {
        let Result = Array.from({length: To - From});

        for(let Iter = From; Iter < To; Iter += 1) {
            Result[Iter - From] = Iter;
        }
        return Result;
    }

    render() {
        let {CurrentPage} = this.state;

        return (
            <div className = "Menu">
                <div className = "Header">
                    <div className = "LeftSide">
                        <button onClick = {() => {
                            this.props.SetProps(false);
                            console.log("button");
                        }} className = "BackButton"><BsFillArrowLeftSquareFill className = "ArrowMarginer"/> Back</button>
                        <button>All Records</button>
                        <button>Pending</button>
                    </div>
                    <div className = "RightSize">
                        <div className = "SortBy">
                            <button className = "MenuTitle">Sort By</button>
                            <ul className = "MenuDropDown">
                                {
                                    /*Implement sorting*/
                                    SortBy.map((value, key) => {
                                        return <button key = {key} className = "SortByElement">{value}</button>
                                    })
                                }
                            </ul>
                        </div>
                    </div>
                </div>
                <Table Items = {this.state.Items} ChainID = {this.props.ChainID}/>
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
                                this.setState({...this.state, CurrentPage: PagesCount});
                                return;
                            }

                            if(Value < 0) {
                                this.setState({...this.state, CurrentPage: 1});
                                return;
                            }

                            this.setState({...this.state, CurrentPage: Value});
                            ChangedByFinder = true;
                        }}/>
                    </div>

                    <div className = "EnumeratedPages">
                        <button onClick = {() => {
                            this.setState({...this.state, CurrentPage: 1});
                            ChangedByFinder = false;
                        }} className = "ButtonFirstLastPage">first</button>
                        {
                            !ChangedByFinder ? (
                                (PagesCount - CurrentPage + 1) > 6 ? (
                                    this.GenerateArray(CurrentPage, PagesCount + 1).map(Item => {
                                        if(Item === PagesCount) {
                                            return <button onClick = {() => {
                                                this.setState({...this.state, CurrentPage: Item});
                                                ChangedByFinder = false;
                                            }} className = "PageItem">{Item}</button>;
                                        }
                                        if(Item === PagesCount - 3) {
                                            return <p>...,&nbsp;</p>;
                                        }

                                        else if(Item < CurrentPage + 3) {
                                            return <button onClick = {() => {
                                                this.setState({...this.state, CurrentPage: Item});
                                                ChangedByFinder = false;
                                            }} className = "PageItem">{Item},&nbsp;</button>;
                                        }
                                        else if(Item > PagesCount - 3) {
                                            return <button onClick = {() => {
                                                this.setState({...this.state, CurrentPage: Item});
                                                ChangedByFinder = false;
                                            }} className = "PageItem">{Item},&nbsp;</button>;
                                        }

                                        return;
                                    })
                                ) : (
                                    this.GenerateArray(CurrentPage, PagesCount + 1).map(Item => {
                                        if(Item === PagesCount) {
                                            return <button onClick = {() => {
                                                this.setState({...this.state, CurrentPage: Item});
                                                ChangedByFinder = false;
                                            }} className = "PageItem">{Item}</button>;
                                        }
                                        else {
                                            return <button onClick = {() => {
                                                this.setState({...this.state, CurrentPage: Item});
                                                ChangedByFinder = false;
                                            }} className = "PageItem">{Item},&nbsp;</button>;
                                        }
                                    })
                                )
                            ) : (
                                <button onClick = {() => {
                                    ChangedByFinder = true;
                                }} className = "PageItem">{CurrentPage}</button>
                            )
                        }
                        <button onClick = {() => {
                            this.setState({...this.state, CurrentPage: PagesCount});
                            ChangedByFinder = false;
                        }} className = "ButtonFirstLastPage">last</button>
                    </div>
                </div>
            </div>
        );
    }
}