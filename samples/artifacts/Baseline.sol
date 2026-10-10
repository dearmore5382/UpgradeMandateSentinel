pragma solidity ^0.8.24;
contract Vault {
    uint256 internal balance;
    function deposit(uint256 amount) external { balance += amount; }
}
