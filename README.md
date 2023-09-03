# Geographic Analysis of "Bon chaussures" project

In 2022, we started a project at GHBS (GROUPE HOSPITALIER BRETAGNE SUD) to provide professionnal shoes to health staff.
We contracted a patnership with a sport shop to provide running shoes. 
Recent medical studies shows that running shoes are adapted to health staff.

Each health staff were given a voucher to buy a pair of running shoes. 
We constated at the end of the year 2022 that one third of health staff did not used their voucher.
We tried to understand the reasons and decided to analyse if the distance between the home adress of health staff and the sport shop had an impact of the voucher use.

The first step was to get gps location and city code from health staff's home adress. 
The API from the BAN (Base d'adresse nationale) was used to retrieved all gps location and city code.

Two maps was created with plotly.

The first map is a choropleth maps of the use of the voucher by city of health staff's residence.

The second map shows the use ratio of the voucher base on the distance from the sport shop.









