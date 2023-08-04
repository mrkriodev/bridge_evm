// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

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

    function startSelection() external onlyBeforeStart {
        hasStarted = true;
    }

    function setThreshold(uint newThreshold) external onlyOwner onlyBeforeStart {
        threshold = newThreshold;
    }

    function increaseCoefficient(uint elementIndex, uint value) external onlyOwner {
        require(elementIndex < coefficients.length, "RoundRobin: Invalid element index");
        coefficients[elementIndex] += value;
    }

    function chooseTwoItems() external onlyAfterStart returns (address, address) {
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