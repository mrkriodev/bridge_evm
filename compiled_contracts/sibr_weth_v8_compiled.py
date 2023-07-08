from solcx import install_solc, compile_source

# install_solc(version='latest')
solc_version = '0.8.17'
install_solc(solc_version)

compiled_sibr_weth_v8 = compile_source(
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
        _owner = address(msg.sender);
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

    function _setOwner(address newOner) internal {
        _owner = newOner;
    }
}

contract WETHTokenV8 is IERC20, Ownable {
    //mapping(address => uint) balances;
    
    uint public totalSupply = 0;
    mapping(address => uint) public balanceOf;
    mapping(address => mapping(address => uint)) public allowance;
    string public name = "WETH v8";
    string public symbol = "WETHV8";
    uint8 public decimals = 18;

    event Minted(address indexed recepient, uint value);
    event Reverted(address indexed sender, uint value);
    event Deposit(address indexed sender, uint amount, uint balance);

    constructor() {
    }

    receive() external payable {
        emit Deposit(msg.sender, msg.value, address(this).balance);
    }

    function transfer(address recipient, uint amount) external returns (bool) {
        balanceOf[msg.sender] -= amount;
        if(recipient == address(this)) {
            totalSupply -= amount;
            emit Reverted(msg.sender, amount);
        }
        else {
            balanceOf[recipient] += amount;
        }
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
        if(recipient == address(this)) {
            totalSupply -= amount;
            emit Reverted(msg.sender, amount);
        }
        else {
            balanceOf[recipient] += amount;
        }
        //balanceOf[recipient] += amount;
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
        emit Minted(recipient, amount);
        emit Transfer(address(0), recipient, amount);
    }

    function _burn(uint amount) internal onlyOwner {
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }

    function setOwner(address msContract) external onlyOwner {
        _setOwner(msContract);
    }
}
    ''',
    output_values=['abi', 'bin']
)


# def get_compiled_sc():
#     p = Path(__file__).parents[1]
#     sc_path = os.path.join(os.path.abspath(p.resolve()), "contracts", "weths_v1_minting.sol")
#     print(sc_path)
#
#     sc_as_text = str()
#     with open(sc_path, 'r') as file:
#         sc_as_text = file.read()
#
#     input_str = sc_as_text
#     return input_str