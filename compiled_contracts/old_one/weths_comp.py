from solcx import install_solc, compile_source

# install_solc(version='latest')
solc_version = '0.8.17'
install_solc(solc_version)

compiled_weths = compile_source(
    '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

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

contract Ownable
{
    // Variable that maintains owner address
    address private _owner;

    // Sets the original owner of contract when it is deployed
    constructor()
    {
        _owner = 0xCe8647A0d0220c387f028D58f84A1C8A90D2450c; //sibr testnet
    }

    // Publicly exposes who is the owner of this contract
    function owner() public view returns(address)
    {
        return _owner;
    }

    // onlyOwner modifier that validates only   if caller of function is contract owner, otherwise not
    modifier onlyOwner()
    {
        require(isOwner(),
        "Function accessible only by the owner !!");
        _;
    }

    // function for owners to verify their ownership. Returns true for owners otherwise false
    function isOwner() public view returns(bool)
    {
        return msg.sender == _owner;
    }
}

contract WETHSToken is IERC20, Ownable {
    //mapping(address => uint) balances;

    uint public totalSupply = 0;
    mapping(address => uint) public balanceOf;
    mapping(address => mapping(address => uint)) public allowance;
    string public name = "WETHS v1";
    string public symbol = "WETHS";
    uint8 public decimals = 18;

    constructor() {
        // balanceOf[msg.sender] = totalSupply;
    }

    function transfer(address recipient, uint amount) external returns (bool) {
        balanceOf[msg.sender] -= amount;
        balanceOf[recipient] += amount;
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    function approve(address spender, uint amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(
        address sender,
        address recipient,
        uint amount
    ) external returns (bool) {
        allowance[sender][msg.sender] -= amount;
        balanceOf[sender] -= amount;
        balanceOf[recipient] += amount;
        emit Transfer(sender, recipient, amount);
        return true;
    }

    function mintAndTransfer(address recipient, uint amount) external onlyOwner {
        _mint(recipient, amount);
    }

    //function _mint(uint amount) external {
    function _mint(address recipient, uint amount) internal {
        //balanceOf[msg.sender] += amount;
        balanceOf[recipient] += amount;
        totalSupply += amount;
        //emit Transfer(address(0), msg.sender, amount);
        emit Transfer(address(0), recipient, amount);
    }

    function _burn(uint amount) internal onlyOwner {
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }
}
    ''',
    output_values=['abi', 'bin']
)
