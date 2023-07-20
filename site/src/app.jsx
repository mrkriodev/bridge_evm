import { Component } from "react";

import Swap from "./swap/swap";
import Mint from "./mint/mint";
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
            Accounts: null,
            BuyCoffee: false
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
        let {InjectedProvider, MenuLink, URL, SuccessProps, ChainID, BuyCoffee} = this.state;
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
            BuyCoffee: BuyCoffee,
            URL: URL,
            Accounts: AvailableAccounts === null || AvailableAccounts === undefined ? [null] : AvailableAccounts
        });

        let {Accounts} = this.state;
        console.log("Detected accounts:");

        for(let Iter in Accounts) {
            console.log(Accounts[Iter]);
        }

        setInterval(async () => {
            let {InjectedProvider, MenuLink, SuccessProps, URL, Accounts, BuyCoffee} = this.state;
            
            this.setState ({
                MenuLink: MenuLink,
                SuccessProps: SuccessProps,
                InjectedProvider: InjectedProvider,
                BuyCoffee: BuyCoffee,
                URL: URL,
                Accounts: Accounts,
                ChainID: await window.ethereum.request({ method: 'eth_chainId' })
            });
        }, 1000);
    }

    async SetProps(Mode) {
        console.log(`Props are: ${Mode} ${typeof Mode}`);
        this.setState ({...this.state, SuccessProps: Mode });
    }

    async SetSuccessProps() {
        this.setState ({...this.state, SuccessProps: true });
    }

    async SetBuyCoffee() {
        console.log("Im called");
        this.setState ({
            ...this.state, BuyCoffee: true
        });
    }

    render() {
        let {Accounts, SuccessProps, URL, ChainID, InjectedProvider, BuyCoffee} = this.state;

        return (
            <div className = "Page">
                <div>
                    <h1 className = "Logotype">Bridge Provider</h1>
                </div>
                {/* {
                    InjectedProvider ? (
                        SuccessProps ? <Menu URL = {URL} SetProps = {this.SetProps.bind(this)}/> : (
                            BuyCoffee ? <Mint FirstAddress = {Accounts[0]} SetCoffee = {Mode => {
                                this.setState({...this.state, BuyCoffee: Mode});
                            }}/> : (
                                <>
                                    <img src = {Sber} height ="120px" width ="120px" alt = "Sber logo"/>
                                    <Swap SetBuyCoffee = {this.SetBuyCoffee.bind(this)} SuccessProps = {this.SetSuccessProps.bind(this)} MetamaskAddress = {Accounts[0]} InjectedProvider = {InjectedProvider} ChainID = {Number(ChainID, 10)}/>
                                </>
                            )
                        )
                    ) :
                    SuccessProps ? <Menu URL = {URL} SetProps = {this.SetProps.bind(this)}/> : (
                        <>
                            <img src = {Sber} height ="120px" width ="120px" alt = "Sber logo"/>
                            <Swap SetBuyCoffee = {this.SetBuyCoffee.bind(this)} SuccessProps = {this.SetSuccessProps.bind(this)} MetamaskAddress = {null} InjectedProvider = {InjectedProvider} ChainID = {111111}/>
                        </>
                    )
                } */}
                <Menu URL = {URL} />
            </div>
        );
    }
}