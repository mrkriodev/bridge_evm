// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

interface WrapCoinIface{

    function mintAndTransferIssue(address recipient, uint amount, uint issueIndex) external;
    function revertWrapCoinsBack(address recipient, uint amount) external;
}

interface IERC20 {
    function totalSupply() external view returns (uint);

    function balanceOf(address account) external view returns (uint);

    function transfer(address recipient, uint amount) external returns (bool);

    function allowance(address owner, address spender) external view returns (uint);

    function approve(address spender, uint amount) external returns (bool);

    function transferFrom(
        address sender,
        address recipient,
        uint amount
    ) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
}

contract RoundRobin {
    address[] public elements;
    uint[] public coefficients;
    uint private currentIndex;
    bool private hasStarted;
    uint private threshold = 5;
    address private owner;

    event ItemChosen(address item1, address item2);

    constructor(address[] memory initialElements, uint[] memory initialCoefficients) {
        require(initialElements.length == 5, "Initial elements array should have 5 elements");
        require(initialCoefficients.length == 5, "Initial coefficients array should have 5 elements");
        elements = initialElements;
        coefficients = initialCoefficients;
        currentIndex = 0;
        hasStarted = false;
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "RoundRobin: Only the owner can call this function");
        _;
    }

    modifier onlyBeforeStart() {
        require(!hasStarted, "RoundRobin: The selection process has already started");
        _;
    }

    modifier onlyAfterStart() {
        require(hasStarted, "RoundRobin: The selection process has not yet started");
        _;
    }

    function startSelection() public onlyBeforeStart {
        hasStarted = true;
    }

    function setThreshold(uint newThreshold) external onlyOwner onlyBeforeStart {
        threshold = newThreshold;
    }

    function increaseCoefficient(uint elementIndex, uint value) external onlyOwner {
        require(elementIndex < coefficients.length, "RoundRobin: Invalid element index");
        coefficients[elementIndex] += value;
    }

    function chooseTwoItems() external onlyOwner returns (address, address) {
        address item1;
        address item2;
        bool itemSeted = false;
        uint prevIndex = currentIndex;
        if(currentIndex != 0) {
            currentIndex += 1;
        }
        while (!itemSeted) {
            if (currentIndex >= elements.length) {
                // If currentIndex exceeds the array length, wrap around to the beginning
                currentIndex = 0;
            }
            item1 = elements[currentIndex];

            if (coefficients[currentIndex] > threshold) {
                itemSeted = true;
            } else {
                currentIndex += 1;
            }

            if (currentIndex==prevIndex && !itemSeted){
                item1 = elements[0];
                itemSeted = true;
            }
        }
        itemSeted = false;
        prevIndex = currentIndex;
        currentIndex +=1;
        while (!itemSeted) {
            if (currentIndex >= elements.length) {
                // If currentIndex exceeds the array length, wrap around to the beginning
                currentIndex = 0;
            }
            item2 = elements[currentIndex];

            if (coefficients[currentIndex] > threshold) {
                itemSeted = true;
            } else {
                currentIndex += 1;
            }

            if (currentIndex==prevIndex  && !itemSeted){
                item2 = elements[1];
                itemSeted = true;
            }
        }

        emit ItemChosen(item1, item2);
        hasStarted = false;
        return (item1, item2);
    }
}

contract MSIssuerV9v1 {
    RoundRobin private roundRobinContract;
    uint private threshold = 5;
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
    // Event to be emitted when the contract receives tokens
    //event WETHTokensReceived(address indexed from, uint256 amount);
    // Event to be emitted when the contract receives tokens
    event WrapTokensReceived(address indexed from, uint256 amount);
    event ChoosenGuardiansEvent(address indexed guardianOne, address indexed guardianTwo);
    event logstr(string message, uint num);

    address public provider;
    address[] public guardians;
    mapping(address => bool) public isGuardian;
    uint public numConfirmationsRequired;
    uint public numSignsRequired;
    uint public issueRewardPercent = 5;
    uint public signersRewardPercent = 4;
    address public WETHTokenAddress = address(0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6);

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
        //int32 domain;
        uint signersReward;
        bool provided;
        uint numSigns;
    }

    address public constant WrappedTokenAddress = address(0xA72d39Ac1c5BB0abc1A044741947ACC44a23CCe5);

    // mapping from tx index => owner => bool
    mapping(uint => mapping(address => bool)) public isConfirmed;

    // mapping from issue index => owner => bool
    mapping(uint => mapping(address => bool)) public isSigned;

    Transaction[] public transactions;

    Issue[] public issues;

    modifier onlyOwner() {
        require(isGuardian[msg.sender], "not guardian");
        _;
    }

    modifier onlyGuardian() {
        require(isGuardian[msg.sender], "not guardian");
        _;
    }

    modifier onlyProvider() {
         require(msg.sender == provider, "not provider");
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

    constructor(address[] memory _guardians, uint _numConfirmationsRequired, uint _numSignsRequired) {
        require(_guardians.length > 0, "guardians required");
        require(
            _numConfirmationsRequired > 0 &&
                _numConfirmationsRequired <= _guardians.length,
            "invalid number of required confirmations"
        );
        require(
            _numSignsRequired > 0 &&
                _numSignsRequired <= _guardians.length,
            "invalid number of required signs"
        );

        for (uint i = 0; i < _guardians.length; i++) {
            address guardian = _guardians[i];

            require(guardian != address(0), "invalid guardian");
            require(!isGuardian[guardian], "guardian not unique");

            isGuardian[guardian] = true;
            guardians.push(guardian);
        }
        uint[] memory defaultValues = new uint[](5);
        defaultValues[0] = 10;
        defaultValues[1] = 10;
        defaultValues[2] = 1;
        defaultValues[3] = 1;
        defaultValues[4] = 1;
        roundRobinContract = new RoundRobin(_guardians, defaultValues);

        provider = msg.sender;
        numConfirmationsRequired = _numConfirmationsRequired;
        numSignsRequired = _numSignsRequired;
    }

    receive() external payable {
        // \todo restrict deposit to some value
        // \tood check - is it coin ?
        emit Deposit(msg.sender, msg.value, address(this).balance);
    }

    // function depositWETH(uint _amount) external {
    //     IERC20 token = IERC20(WETHTokenAddress);
    //     // Approve the contract to spend the sender's tokens
    //     require(token.approve(address(this), _amount), "Token approval failed");
    //     // Transfer the tokens from the sender to the contract
    //     require(token.transferFrom(msg.sender, address(this), _amount), "Token transfer failed");
    //     // Emit the event
    //     emit WETHTokensReceived(msg.sender, _amount);
    // }

    // function depositWBTC(uint _amount) external {
    // }


    function submitTransaction(
        address _to,
        uint _value,
        bytes memory _data
    ) public onlyProvider {
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

    function initIssue(address _to, uint _value) public onlyProvider {
        // Generate the issueId.
        //issueId = bytes20(keccak256(_to, block.blockhash(block.number - 1)));
        uint issueIndex = issues.length;

        emit logstr("gasleft1", gasleft());
        // Reward the validator for signing a transaction
        uint issueRewardAmount = (_value * issueRewardPercent) / 100;
        uint exactIssueReward = (issueRewardAmount > 100000000000000) ? issueRewardAmount : 100000000000000;
        //uint exactIssueReward = 100000000000000;
        payable(msg.sender).transfer(exactIssueReward);
        emit logstr("gasleft2", gasleft());

        uint shrinkvalue = (_value-exactIssueReward);
        uint m_signerRewardAmount = (shrinkvalue * signersRewardPercent ) / 100;
        uint exactSignersReward = (m_signerRewardAmount > 100000000000000) ? m_signerRewardAmount : 100000000000000;
        exactSignersReward *= numSignsRequired;
        emit logstr("gasleft3", gasleft());
        //uint exactSignersReward = 200000000000000;
        uint toAdrValue = (_value-exactIssueReward-exactSignersReward);

        issues.push(
            Issue({
                to: _to,
                value: toAdrValue,
                signersReward: exactSignersReward,
                provided: false,
                numSigns: 0
            })
        );
        emit IssueInited(msg.sender, issueIndex, _to, toAdrValue);
        emit logstr("gasleft4", gasleft());
        //roundRobinContract.startSelection();
        // Call the chooseTwoItems function from the RoundRobin contract
        (address guardianOne, address guardianTwo) = roundRobinContract.chooseTwoItems();
        emit logstr("gasleft5", gasleft());
        // Emit the BridgeEvent to indicate the chosen items from RoundRobin
        emit ChoosenGuardiansEvent(guardianOne, guardianTwo);
    }

    function confirmTransaction(
        uint _txIndex
    ) public onlyGuardian txExists(_txIndex) notExecuted(_txIndex) notConfirmed(_txIndex) {
        Transaction storage transaction = transactions[_txIndex];
        transaction.numConfirmations += 1;
        isConfirmed[_txIndex][msg.sender] = true;

        emit ConfirmTransaction(msg.sender, _txIndex);
    }

    function signIssue(uint _issueIndex) public onlyGuardian
    issueExists(_issueIndex) notProvided(_issueIndex) notSigned(_issueIndex) {
        Issue storage issue = issues[_issueIndex];
        issue.numSigns += 1;
        isSigned[_issueIndex][msg.sender] = true;

        emit IssueSigned(msg.sender, _issueIndex);
    }

    function executeTransaction(
        uint _txIndex
    ) public onlyProvider txExists(_txIndex) notExecuted(_txIndex) {
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

    function provideIssue(uint _issueIndex) public onlyProvider issueExists(_issueIndex) notProvided(_issueIndex) {
        Issue storage issue = issues[_issueIndex];
        require(issue.numSigns >= numSignsRequired, "cannot provide issue");

        uint needToPay = numSignsRequired;
        for(uint i = 0; ((i < guardians.length) && (needToPay != 0)); i++)
        {
            address g_adr = guardians[i];
            if(isSigned[_issueIndex][g_adr] == true) {
                payable(g_adr).transfer(issue.signersReward/numSignsRequired);
                needToPay -= 1;
            }
        }

        issue.provided = true;
        emit IssueProvided(msg.sender, _issueIndex);
    }

    // this function calls than Issue in SberNet is provided
    function callMintWSIBR(address _to, uint _value, uint issueIndex) public onlyProvider {
        // todo: also add signs from guardians
        WrapCoinIface WETHSTokenContract = WrapCoinIface(WrappedTokenAddress);
        WETHSTokenContract.mintAndTransferIssue(_to, _value, issueIndex);
    }

    // function to revert SIBR back in Siberium Network
    function recvWrapCoinsBack(uint _amountTokens) external {
        // Ensure the contract receives tokens from the sender
        IERC20 token = IERC20(WrappedTokenAddress);

        // Approve the contract to spend the sender's tokens
        require(token.approve(address(this), _amountTokens), "Token approval failed");

        // Transfer the tokens from the sender to the contract
        require(token.transferFrom(msg.sender, address(this), _amountTokens), "Token transfer failed");

        WrapCoinIface WETHSTokenContract = WrapCoinIface(WrappedTokenAddress);
        WETHSTokenContract.revertWrapCoinsBack(msg.sender,  _amountTokens);

        // Emit the event of wrap tokens receive
        emit WrapTokensReceived(msg.sender, _amountTokens);
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
        return guardians;
    }

    function getGuardians() public view returns (address[] memory) {
        return guardians;
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