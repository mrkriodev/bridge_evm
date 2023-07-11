import { Component } from "react";

import Swap from "./swap/swap";
import Menu from "./table/menu";
import Sber from "./img/sber.png";

export default class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            MenuLink: props.MenuLink,
            SuccessProps: false,
            URL: props.URL,
            Accounts: null
        };
    }

    async componentDidMount() {
        let {MenuLink, URL, SuccessProps} = this.state;
        let InjectedProvider = typeof window.ethereum !== 'undefined' ? true : false;

        console.log(`Injected provider is ${InjectedProvider === true ? "supported" : "unsupported"}`);
    
        let AvailableAccounts = await window.ethereum.request ({
            method: "eth_requestAccounts",
        }).catch(Error => {
            console.log(`Could not connect to a wallet: ${Error}`);
        })

        this.setState ({
            MenuLink: MenuLink,
            SuccessProps: SuccessProps,
            URL: URL,
            InjectedProvider: InjectedProvider,
            Accounts: AvailableAccounts === null || AvailableAccounts === undefined ? [null] : AvailableAccounts
        });

        let {Accounts} = this.state;
        console.log("Detected accounts:");

        for(let Iter in Accounts) {
            console.log(Accounts[Iter]);
        }

        window.ethereum.on('chainChanged', () => {
            window.location.reload();
        });
    }

    async SetSuccessProps() {
        let {MenuLink, URL, Accounts} = this.state;

        this.setState ({
            MenuLink: MenuLink,
            URL: URL,
            Accounts: Accounts,
            SuccessProps: true
        });
    }

    render() {
        let {InjectedProvider, Accounts, SuccessProps, URL} = this.state;

        return (
            <div className = "Page">
                <div>
                    <h1 className = "Logotype">Bridge Guardian</h1>
                </div>
                {
                    InjectedProvider ? (
                        SuccessProps ? <Menu URL = {URL}/> : (
                            <>
                                <img src = {Sber} height ="160px" width ="160px" alt = "Sber logo"/>
                                <Swap SuccessProps = {this.SetSuccessProps.bind(this)} MetamaskAddress = {Accounts[0]}/>
                            </>
                        )
                    ) :
                    <p>Your browser does not have metamask extension. Install it or log in</p>
                }
            </div>
        );
    }
}