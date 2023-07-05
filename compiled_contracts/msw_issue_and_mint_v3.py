from solcx import install_solc, compile_source

# install_solc(version='latest')
solc_version = '0.8.17'
install_solc(solc_version)

compiled_msw_issue_mint_v3 = compile_source(
    '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

interface WETHSIface{
  function mintAndTransfer(address recipient, uint amount) external;
}


contract MSIssuer {
    event Deposit(address indexed sender, uint amount, uint balance);
    event SubmitTransaction(
        address indexed owner,
        uint indexed txIndex,
        address indexed to,
        uint value,
        bytes data
    );
    event ConfirmTransaction(address indexed owner, uint indexed txIndex);
    event RevokeConfirmation(address indexed owner, uint indexed txIndex);
    event ExecuteTransaction(address indexed owner, uint indexed txIndex);

    event IssueInited(
        address indexed owner,
        uint indexed issueIndex,
        address indexed to,
        uint value
    );
    event IssueSigned(address indexed owner, uint indexed issueIndex);
    //event RevokeSign(address indexed owner, uint indexed issueIndex);
    event IssueProvided(address indexed owner, uint indexed issueIndex);

    address[] public owners;
    mapping(address => bool) public isOwner;
    uint public numConfirmationsRequired;
    uint public numSignsRequired;

    struct Transaction {
        address to;
        uint value;
        bytes data;
        bool executed;
        uint numConfirmations;
    }

    struct Issue {
        address to;
        uint value;
        bool provided;
        uint numSigns;
    }

    address public constant WETHSTokenAddress = address(0x2589330Abe857B4aAc657a73756313606381AaF5);

    // mapping from tx index => owner => bool
    mapping(uint => mapping(address => bool)) public isConfirmed;

    // mapping from tx index => owner => bool
    mapping(uint => mapping(address => bool)) public isSigned;

    Transaction[] public transactions;

    Issue[] public issues;

    modifier onlyOwner() {
        require(isOwner[msg.sender], "not owner");
        _;
    }

    modifier txExists(uint _txIndex) {
        require(_txIndex < transactions.length, "tx does not exist");
        _;
    }

    modifier issueExists(uint _issueIndex) {
        require(_issueIndex < issues.length, "issue does not exist");
        _;
    }

    modifier notExecuted(uint _txIndex) {
        require(!transactions[_txIndex].executed, "tx already executed");
        _;
    }

    modifier notProvided(uint _issueIndex) {
        require(!issues[_issueIndex].provided, "issue already provided");
        _;
    }

    modifier notConfirmed(uint _txIndex) {
        require(!isConfirmed[_txIndex][msg.sender], "tx already confirmed");
        _;
    }

    modifier notSigned(uint _issueIndex) {
        require(!isSigned[_issueIndex][msg.sender], "issue already signed");
        _;
    }

    constructor(address[] memory _owners, uint _numConfirmationsRequired/*, uint _numSignsRequired*/) {
        require(_owners.length > 0, "owners required");
        require(
            _numConfirmationsRequired > 0 &&
                _numConfirmationsRequired <= _owners.length,
            "invalid number of required confirmations"
        );
        /*require(
            _numSignsRequired > 0 &&
                _numSignsRequired <= _owners.length,
            "invalid number of required signs"
        );*/

        for (uint i = 0; i < _owners.length; i++) {
            address owner = _owners[i];

            require(owner != address(0), "invalid owner");
            require(!isOwner[owner], "owner not unique");

            isOwner[owner] = true;
            owners.push(owner);
        }

        numConfirmationsRequired = _numConfirmationsRequired;
        //numSignsRequired = _numSignsRequired;
        numSignsRequired = _numConfirmationsRequired;
    }

    receive() external payable {
        emit Deposit(msg.sender, msg.value, address(this).balance);
    }

    function submitTransaction(
        address _to,
        uint _value,
        bytes memory _data
    ) public onlyOwner {
        uint txIndex = transactions.length;

        transactions.push(
            Transaction({
                to: _to,
                value: _value,
                data: _data,
                executed: false,
                numConfirmations: 0
            })
        );

        emit SubmitTransaction(msg.sender, txIndex, _to, _value, _data);
    }
    
    function initIssue( address _to, uint _value) public onlyOwner {
        uint issueIndex = issues.length;
        issues.push(
            Issue({
                to: _to,
                value: _value,
                provided: false,
                numSigns: 0
            })
        );

        emit IssueInited(msg.sender, issueIndex, _to, _value);
    }

    function confirmTransaction(
        uint _txIndex
    ) public onlyOwner txExists(_txIndex) notExecuted(_txIndex) notConfirmed(_txIndex) {
        Transaction storage transaction = transactions[_txIndex];
        transaction.numConfirmations += 1;
        isConfirmed[_txIndex][msg.sender] = true;

        emit ConfirmTransaction(msg.sender, _txIndex);
    }

    function signIssue(uint _issueIndex) public onlyOwner 
    issueExists(_issueIndex) notProvided(_issueIndex) notSigned(_issueIndex) {
        Issue storage issue = issues[_issueIndex];
        issue.numSigns += 1;
        isSigned[_issueIndex][msg.sender] = true;

        emit IssueSigned(msg.sender, _issueIndex);
    }

    function executeTransaction(
        uint _txIndex
    ) public onlyOwner txExists(_txIndex) notExecuted(_txIndex) {
        Transaction storage transaction = transactions[_txIndex];

        require(
            transaction.numConfirmations >= numConfirmationsRequired,
            "cannot execute tx"
        );

        transaction.executed = true;

        (bool success, ) = transaction.to.call{value: transaction.value}(
            transaction.data
        );
        require(success, "tx failed");

        emit ExecuteTransaction(msg.sender, _txIndex);
    }

    function provideIssue(uint _issueIndex) public onlyOwner issueExists(_issueIndex) notProvided(_issueIndex) {
        Issue storage issue = issues[_issueIndex];
        require(issue.numSigns >= numSignsRequired, "cannot privede issue");
        
        callMintWETHS(issue.to, issue.value);

        issue.provided = true;
        emit IssueProvided(msg.sender, _issueIndex);
    }

    function callMintWETHS(address _to, uint _value) internal {
        WETHSIface WETHSTokenContract = WETHSIface(WETHSTokenAddress);
        WETHSTokenContract.mintAndTransfer(_to, _value);
    }

    function revokeConfirmation(
        uint _txIndex
    ) public onlyOwner txExists(_txIndex) notExecuted(_txIndex) {
        Transaction storage transaction = transactions[_txIndex];

        require(isConfirmed[_txIndex][msg.sender], "tx not confirmed");

        transaction.numConfirmations -= 1;
        isConfirmed[_txIndex][msg.sender] = false;

        emit RevokeConfirmation(msg.sender, _txIndex);
    }

    function getOwners() public view returns (address[] memory) {
        return owners;
    }

    function getTransactionCount() public view returns (uint) {
        return transactions.length;
    }

    function getIssuesCount() public view returns (uint) {return issues.length;}

    function getTransaction(
        uint _txIndex
    )
        public
        view
        returns (
            address to,
            uint value,
            bytes memory data,
            bool executed,
            uint numConfirmations
        )
    {
        Transaction storage transaction = transactions[_txIndex];

        return (
            transaction.to,
            transaction.value,
            transaction.data,
            transaction.executed,
            transaction.numConfirmations
        );
    }

    function getIssue(uint _issueIndex) public view returns (
            address to,
            uint value,
            bool provided,
            uint numSigns
        )
    {
        Issue storage issue = issues[_issueIndex];

        return (
            issue.to,
            issue.value,
            issue.provided,
            issue.numSigns
        );
    }
}
    ''',
    output_values=['abi', 'bin']
)
