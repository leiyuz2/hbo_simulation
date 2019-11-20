# hbo_simulation
API Name: hbo_simulation-API
arn:aws:execute-api:us-west-2:182086822844:pt7m7lfli4/*/*/hbo_simulation
API endpoint: https://9kw17br2vc.execute-api.us-west-2.amazonaws.com/dev/
Currently hbo_simulation-API can only handle homebuyer simulation tool. The HomeBuyer simulation focuses on the homebuyer with not sufficient down payment and compares the potential home buyer outcome between Unison HomeBuyer program and PMI.
Input Structure
Key	Value	Description
home_value	Range between 25,000 to 5,000,000	Integer
Investment_percentage	Restricted to 3 options: 0.05, 0.10, 0.15	Float

Output Structure
Key	Value	Description
Unison_rtn	Example: 1685623	Integer. Median Return for Unison HomeBuyer. 
None_Unison_rtn	Example: 1630441	Integer. Median Return for None-Unison HomeBuyer.
Unison_win	Example: 87	Integer. Probability of Unison HomeBuyer make money. Range from 0 to 100.
None_Unison_win	Example: 74	Integer. Probability of None-Unison HomeBuyer make money. Range from 0 to 100.
Unison_lose_part	Example: 7	Integer. Probability of Unison HomeBuyer lose part of the downpayment. Range from 0 to 100.
None_Unison_lose_part	Example: 9	Integer. Probability of None-Unison HomeBuyer lose part of the downpayment. Range from 0 to 100.
Unison_lose_all	Example: 6	Integer. Probability of Unison HomeBuyer lose all downpayment. Range from 0 to 100.
None_Unison_lose_all	Example: 17	Integer. Probability of None-Unison HomeBuyer lose all downpayment. Range from 0 to 100.
Monthly_Savings	Example: 3676	Integer. Estimated monthly savings of Unison HomeBuyer.
None_Unison_Mortgage_Principal	Example: 4500	Integer. Mortgage amount for None-Unison HomeBuyer. Already in thousands.
Unison_Mortgage_Principal	Example: 4000	Integer. Mortgage amount for Unison HomeBuyer. Already in thousands.

Sample Input and Output
Input
{
  "home_value": 1000000,
  "investment_percentage": 0.1
}
Output
{
  "Unison_rtn": 337125,
  "None_Unison_rtn": 326088,
  "Unison_win": 87,
  "None_Unison_win": 74,
  "Unison_lose_part": 7,
  "None_Unison_lose_part": 9,
  "Unison_lose_all": 6,
  "None_Unison_lose_all": 17,
  "Monthly_Savings": 735,
  "None_Unison_Mortgage_Principal": 900,
  "Unison_Mortgage_Principal": 800
}
