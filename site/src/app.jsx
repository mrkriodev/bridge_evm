import { Component } from "react";

import Swap from "./swap/swap";
import Menu from "./table/menu";
import Sber from "./img/sber.png";

export default class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            MenuLink: props.MenuLink,
            InjectedProvider: false,
            SuccessProps: false,
            ChainID: null,
            URL: props.URL,
            Accounts: null
        };
    }

    async ConnectMetaMask() {
        return await window.ethereum.request({ method: 'eth_requestAccounts' })
            .catch((error) => {
                if (error.code === 4001) {
                    console.log('Please connect to MetaMask.');
                } else {
                    console.error(error);
                }
            }
        );
    }

    async componentDidMount() {
        let {InjectedProvider, MenuLink, URL, SuccessProps, ChainID} = this.state;
        InjectedProvider = typeof window.ethereum !== 'undefined';

        console.log(`Injected provider is ${InjectedProvider === true ? "supported" : "unsupported"}`);
    
        console.log("Call");
        let AvailableAccounts = await this.ConnectMetaMask();
        console.log("After call");

        this.setState ({
            ChainID: ChainID,
            MenuLink: MenuLink,
            SuccessProps: SuccessProps,
            InjectedProvider: InjectedProvider,
            URL: URL,
            Accounts: AvailableAccounts === null || AvailableAccounts === undefined ? [null] : AvailableAccounts
        });

        let {Accounts} = this.state;
        console.log("Detected accounts:");

        for(let Iter in Accounts) {
            console.log(Accounts[Iter]);
        }

        setInterval(async () => {
            let {InjectedProvider, MenuLink, SuccessProps, URL, Accounts} = this.state;
            
            this.setState ({
                MenuLink: MenuLink,
                SuccessProps: SuccessProps,
                InjectedProvider: InjectedProvider,
                URL: URL,
                Accounts: Accounts,
                ChainID: await window.ethereum.request({ method: 'eth_chainId' })
            });
        }, 1000);
    }

    async SetSuccessProps() {
        let {InjectedProvider, MenuLink, URL, Accounts, ChainID} = this.state;

        this.setState ({
            MenuLink: MenuLink,
            InjectedProvider: InjectedProvider,
            ChainID: ChainID,
            URL: URL,
            Accounts: Accounts,
            SuccessProps: true
        });
    }

    render() {
        let {Accounts, SuccessProps, URL, ChainID, InjectedProvider} = this.state;
        console.log(`Take: ${InjectedProvider}`);

        return (
            <div className = "Page">
                <div>
                    <h1 className = "Logotype">Bridge Provider</h1>
                </div>
                {
                    InjectedProvider ? (
                        SuccessProps ? <Menu URL = {URL}/> : (
                            <>
                                <img src = {Sber} height ="120px" width ="120px" alt = "Sber logo"/>
                                <Swap SuccessProps = {this.SetSuccessProps.bind(this)} MetamaskAddress = {Accounts[0]} InjectedProvider = {InjectedProvider} ChainID = {Number(ChainID, 10)}/>
                            </>
                        )
                    ) :
                    SuccessProps ? <Menu URL = {URL}/> : (
                        <>
                            <img src = {Sber} height ="120px" width ="120px" alt = "Sber logo"/>
                            <Swap SuccessProps = {this.SetSuccessProps.bind(this)} MetamaskAddress = {null} InjectedProvider = {InjectedProvider} ChainID = {111111}/>
                        </>
                    )
                }
            </div>
        );
    }
}