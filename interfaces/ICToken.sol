// SPDX-License-Identifier: BSD-3-Clause
pragma solidity ^0.6.12;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

interface ICToken is IERC20 {

    
    event RepayBorrow(address payer, address borrower, uint repayAmount, uint accountBorrows, uint totalBorrows);
    event Borrow(address borrower, uint borrowAmount, uint accountBorrows, uint totalBorrows);
    event Redeem(address redeemer, uint redeemAmount, uint redeemTokens);
    event Mint(address minter, uint mintAmount, uint mintTokens);
    event AccrueInterest(uint cashPrior, uint interestAccumulated, uint borrowIndex, uint totalBorrows);
    event LiquidateBorrow(address liquidator, address borrower, uint repayAmount, address cTokenCollateral, uint seizeTokens);

    function transfer(address dst, uint amount) override external returns (bool);
    function transferFrom(address src, address dst, uint amount) override external returns (bool);
    function approve(address spender, uint amount) override external returns (bool);
    function allowance(address owner, address spender) override external view returns (uint);
    function balanceOf(address owner) override external view returns (uint);
    function balanceOfUnderlying(address owner) external returns (uint);
    function getAccountSnapshot(address account) external view returns (uint, uint, uint, uint);
    function borrowRatePerBlock() external view returns (uint);
    function supplyRatePerBlock() external view returns (uint);
    function totalBorrowsCurrent() external returns (uint);
    function borrowBalanceCurrent(address account) external returns (uint);
    function borrowBalanceStored(address account) external view returns (uint);
    function exchangeRateCurrent() external returns (uint);
    function exchangeRateStored() external view returns (uint);
    function getCash() external view returns (uint);
    function accrueInterest() external returns (uint);
    function seize(address liquidator, address borrower, uint seizeTokens) external returns (uint);

    function mint(uint mintAmount) external returns (uint);
    function redeem(uint redeemTokens) external returns (uint);
    function redeemUnderlying(uint redeemAmount) external returns (uint);
    function borrow(uint borrowAmount) external returns (uint);
    function repayBorrow(uint repayAmount) external returns (uint);
    function repayBorrowBehalf(address borrower, uint repayAmount) external returns (uint);
}