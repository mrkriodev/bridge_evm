pragma solidity ^0.8.17;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract CoffeeNFTMinter is ERC721URIStorage {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    constructor() ERC721 ("CoffeeNFT", "Coffee")
    { }

    function MakeCoffee(address Receiver, string memory TokenURI) public {
        uint256 newItemId = _tokenIds.current();

        _safeMint(Receiver, newItemId);
        
        _setTokenURI(newItemId, TokenURI);

        _tokenIds.increment();
    }
}
