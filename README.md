# 1996-Arbitrage-Model
(in progess, see code for proof of concept)
##Context
In the world's currency market there exist an exchange rate between two currencies. It is always true that if you covert currency _A_ to currency _B_ you will end up with less money that what you started with. The implication here is that the product of exchange rates between any pair of countries is less than one. 
Under very particular circumstances we can create a chain of conversions that results in a net gain. This is known as arbitrage. A simple linear programming model can be used to find the exact exchanges needed where this sitution exist. 
##Data
Consider the table of exchange rates from the Wall Street Journal on Nov 10, 1996. 

|   | USD | Yen | Mark | Franc |
| - | --- | --- | ---- | ----- |
|USD|     |111.52|1.4987|5.852|
|Yen|.008966|   |.013493|.045593|
|Mark|.6659|73.964|   |3.3823|
|Franc|.1966|21.933|.29507|   |

