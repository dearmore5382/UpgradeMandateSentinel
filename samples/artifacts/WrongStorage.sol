pragma solidity ^0.8.24;
contract Vault {
    address internal owner;
    uint256 internal balance;
    function deposit(uint256 amount) external { balance += amount; }
    function roundFee(uint256 amount) external pure returns (uint256) { return amount / 100; }
}
