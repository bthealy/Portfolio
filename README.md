# Fuzzy Logic Stock market Trader
Course - CS657 Intelligent Systems

## Programming Problem
**PDF format supplied in files** 
Suppose that you are to design a fuzzy expert system for stock trading. The inputs to the fuzzy system are the current stock price of the company XYZ, i.e. XYZ(i) on day i, the n day moving average TMA(i)=1/(n+1) ∑_(i-n)^i▒〖XYZ(i)〗, and an indicator called MAD (moving average divergence), and i is the current day. The fuzzy sets for the stock price XYZ(i)  and TMA(i)  are VL (very low) LO (low), MD (medium) and HI (high) and VH (very high).  Similarly the fuzzy sets for the MAD are N (negative), Z (zero) and P (positive).   The outputs are BM (buy many), BF (buy few), DT (do not trade), SF (sell few) and SM (sell many). Suppose that there is a correlation between the price of XYZ(i+1) and the MAD(i) indicator such that when MAD is positive today the stock price is expected to rise the next day with a high probability, and when MAD is negative, the stock price is expected to fall the next day with a high probability. When the indicator does not show a noticeable trend, the next day stock price has no correlation with the MAD. Finally the price of next day XYZ(i+1)  is usually (but not always) proportional to its past n days moving average, where n is typically 10 to 20 (you decided the value of n).

However, there are sometimes exceptions to above general rules due to political events and psychological mood of the market, e.g. political situation such as, U.S., Russia, China, Ukraine; corporate scandals and fraud, Homeland Security Department raising the alarm level, change in earning forecast, etc.  The news about these events often produces random fluctuations in stock prices, which we will model as random numbers.  Thus the stock share price and MAD, at the open of the i-th day trading are modeled as 
XYZ(i)=10+2.8 sin⁡(2πi/19)+0.9 cos⁡(2πi/19)+ζ(i)+0.014i

MAD(i)=0.6 cos(0.4i)-sin⁡(0.5i)+η(i)

where i=1,2,...,360 is the day number, ζ(i)=0.6r(i)  ×(i%3) , η(i)=0.5r(i) ×(i%3),   and r(i)  is a random number between –1 and +1.

Design a fuzzy trading with 3 inputs and one output, to maximize your profit (or minimize your loss).  Note that the fuzzy system has only last nine days prices and today’s price, and today’s MAD and has no knowledge of future prices or future MAD given by the above equations.   Simulate the system assuming that you can trade no more than once a day at the market open.  You have $10,000 to invest, and the maximum number of stock share buy or sell each time is 600.  

Write a short report (2-3 pages) about your work.  In this report indicate how you solved the problem, reasoning behind your solutions, results and discussion of findings and conclusions.  In your report show plots of the number of shares bought/sold, daily profit/loss and accumulated profit/loss as a function of days.

## Solution
See Report.pdf
https://github.com/bthealy/Portfolio/blob/main/Report.pdf

This solution was completed using MATLAB's Fuzzy Logic Toolbox.
