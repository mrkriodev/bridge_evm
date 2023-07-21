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
        this.AutoRefreshingItems = [];
    }

    async componentDidMount() {
        await this.LaunchAutoRefreshing();
    }

    async LaunchAutoRefreshing() {
        let {CurrentPage} = this.state;
        let CachedItems = await this.GetPageItems(CurrentPage);
        
        this.setState ({ ...this.state, Items: CachedItems });

        for(let Iter in CachedItems) {
            if(CachedItems[+Iter].status === false) {
                this.AutoRefreshingItems.push ({
                    Item:   setInterval(() => {
                                let {Items} = this.state;

                                Items.forEach((value, key) => {
                                    if(value.status === false) {
                                        this.GetItem(CachedItems[key].id)
                                        .then(Result => value = Result);
                                    }
                                });
                            }, 1000),
                    ID: CachedItems[+Iter].id,
                    Index: +Iter
                });
            }
        }
    }

    async StopRefreshingItems() {
        for(let Iter in this.AutoRefreshingItems) {
            clearInterval(this.AutoRefreshingItems[Iter].Item);
        }
    }

    async componentWillUnmount() {
        await this.StopRefreshingItems();
    }

    async FilterPending() {
        let {Items} = this.state;
        let Indexes = [];

        for(let Iter in this.AutoRefreshingItems) {
            let Item = this.AutoRefreshingItems[+Iter];

            Indexes.push(+Item.Index);
            clearInterval(+Item.Item);
        }
        this.AutoRefreshingItems = [];

        let Iter = 0;
        while (Iter < Items.length) {
            if (Items[Iter].status === true) {
                Items.splice(Iter, 1);
                Iter -= 1;
            }
            
            Iter += 1;
        }
    }

    /*Fetch Data from specific page*/
    async GetPageItems(Page) {
        if(Page === undefined || Page === null) {
            console.log(`Page is ${Page}`);
            return [];
        }
        Page = (Number(Page, 10) - 1) * 20;

        if(Page === undefined || Page === null) {
            console.log(`Page is ${Page}`);
            return [];
        }

        let Response = await fetch (
            `http://92.255.109.253:9011/api/swaps/?limit=20&start=${Page}`,
            {
                method: "GET",
            }
        );
        if(Response !== undefined && Response !== null && Response.status !== 200) {
            console.log(`Error, response ${Response === null || Response === undefined ? "is " + Response : "status is " + Response.status}`)
        }
        Response = await Response.json();
        PagesCount = Math.ceil(Response.length / 20);

        return Response;
    }

    async SetItems(NewItems) {
        if(NewItems === undefined || NewItems === null) {
            console.log(`NewItems is ${NewItems}`);
            return;
        }

        this.setState({...this.state, Items: NewItems});
    }

    /*Get Status of specific tr-n*/
    async GetItem(ID) {
        if(ID === undefined || ID === null) {
            console.log(`ID is ${ID}`);
            return [];
        }
        ID = Number(ID, 10);

        if(ID === undefined || ID === null) {
            console.log(`ID is ${ID}`);
            return [];
        }

        let Item = await fetch (
            `http://92.255.109.253:9011/api/status/${ID}`,
            {
                method: "GET"
            }
        );

        if(Item !== undefined && Item !== null && Item.status !== 200) {
            console.log(`Error, response ${Item === null || Item === undefined ? "is " + Item : "status is " + Item.status}`)
        }

        return await Item.json();
    }

    /*Get Total count of tr-s*/
    async GetTotal() {
        let Response = await fetch (
            `http://92.255.109.253:9011/api/total`,
            {
                method: "GET",
            }
        );

        if(Response !== undefined && Response !== null && Response.status !== 200) {
            console.log(`Error, response ${Response === null || Response === undefined ? "is " + Response : "status is " + Response.status}`)
        }

        return await Response.json();
    }

    GenerateArray(From, To) {
        let Result = Array.from({length: To - From});

        for(let Iter = From; Iter < To; Iter += 1) {
            Result[Iter - From] = Iter;
        }
        return Result;
    }

    async ChangePageHandler(Page) {
        const {CurrentPage} = this.state;

        if(Page === CurrentPage) {
            return;
        }

        await this.StopRefreshingItems();

        this.setState({...this.state, CurrentPage: Page, Items: await this.GetPageItems(Page)});
        ChangedByFinder = false;
    }

    async AllRecordsHandler() {
        await this.StopRefreshingItems();

        this.LaunchAutoRefreshing();
        ChangedByFinder = false;
    }

    async SortByHandler(Value) {
        let {Items} = this.state;
        
        switch(Value) {
            case "By ID":
                Items.sort((a, b) => {
                    return a.id - b.id;
                });
                break;
            case "Accending Amount":
                Items.sort((a, b) => {
                    return a.amount - b.amount;
                });
                break;
            case "Discending Amount":
                Items.sort((a, b) => {
                    return b.amount - a.amount;
                });
                break;
            default:
                console.error("Invalid type of sort");
        }
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
                        <button onClick = {this.AllRecordsHandler.bind(this)}>All Records</button>
                        <button onClick = {this.FilterPending.bind(this)}>Pending</button>
                    </div>
                    <div className = "RightSize">
                        <div className = "SortBy">
                            <button className = "MenuTitle">Sort By</button>
                            <ul className = "MenuDropDown">
                                {
                                    /*Implement sorting*/
                                    SortBy.map((value, key) => {
                                        return <button onClick = {this.SortByHandler.bind(this, value)} key = {key} className = "SortByElement">{value}</button>
                                    })
                                }
                            </ul>
                        </div>
                    </div>
                </div>
                <Table Items = {this.state.Items} ChainID = {this.props.ChainID}/>
                <div className = "BottomMenu">
                    <div className = "FindSpecific">
                        <input placeholder = "Find Specific" type = "number" onChange = {async(Event) => {
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

                            await this.ChangePageHandler(Value);
                            ChangedByFinder = true;
                        }}/>
                    </div>

                    <div className = "EnumeratedPages">
                        <button onClick = {this.ChangePageHandler.bind(this, 1)} className = "ButtonFirstLastPage">first</button>
                        {
                            !ChangedByFinder ? (
                                (PagesCount - CurrentPage + 1) > 6 ? (
                                    this.GenerateArray(CurrentPage, PagesCount + 1).map(Item => {
                                        if(Item === PagesCount) {
                                            return <button onClick = {this.ChangePageHandler.bind(this, Item)} className = "PageItem">{Item}</button>;
                                        }
                                        if(Item === PagesCount - 3) {
                                            return <p>...,&nbsp;</p>;
                                        }

                                        else if(Item < CurrentPage + 3) {
                                            return <button onClick = {this.ChangePageHandler.bind(this, Item)} className = "PageItem">{Item},&nbsp;</button>;
                                        }
                                        else if(Item > PagesCount - 3) {
                                            return <button onClick = {this.ChangePageHandler.bind(this, Item)} className = "PageItem">{Item},&nbsp;</button>;
                                        }

                                        return;
                                    })
                                ) : (
                                    this.GenerateArray(CurrentPage, PagesCount + 1).map(Item => {
                                        if(Item === PagesCount) {
                                            return <button onClick = {this.ChangePageHandler.bind(this, Item)} className = "PageItem">{Item}</button>;
                                        }
                                        else {
                                            return <button onClick = {this.ChangePageHandler.bind(this, Item)} className = "PageItem">{Item},&nbsp;</button>;
                                        }
                                    })
                                )
                            ) : (
                                <button onClick = {() => {
                                    ChangedByFinder = true;
                                }} className = "PageItem">{CurrentPage}</button>
                            )
                        }
                        <button onClick = {this.ChangePageHandler.bind(this, PagesCount)} className = "ButtonFirstLastPage">last</button>
                    </div>
                </div>
            </div>
        );
    }
}