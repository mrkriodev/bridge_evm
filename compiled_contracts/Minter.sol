pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "hardhat/console.sol";

contract CoffeeNFTMinter is ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    constructor() ERC721 ("CoffeeNFT", "Coffee")
    { }

    function MakeCoffee(address Receiver) public {
        uint256 newItemId = _tokenIds.current();

        _safeMint(Receiver, newItemId);
        
        tokenURI(newItemId);

        _tokenIds.increment();
    }

    function tokenURI(uint256 _tokenId) public view override returns (string memory) {
        require(_exists(_tokenId));
        console.log("An NFT w/ ID %s has been minted to %s", _tokenId, msg.sender);

        return "https://ipfs.io/ipfs/QmWx2DKYhwKeBn5Ugi7NfAA4Zie6q4J3R7UeRH9TLCfS19?filename=coffee.json";
    }
}