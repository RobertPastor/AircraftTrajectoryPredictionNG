# Flying costs   

For each aircraft type, the airline provides flying costs.   
This is a factor that multiplied by the flight duration, gives you flying costs.

# Optimization One  
The first optimization computation is based only on flying costs, hence related to flight duration (times costs incurred by duration).   
The result of this optimization gives you for all routes (one way or return), the aircraft type with the lower flying costs.

# Optimization based on Flying Costs and Kerosene Costs
The second optimization adds flying costs (based upon flight duration) and kerosene costs (based upon mass lost during the flight).
The result of this optimization selects the best aircraft based upon a trade-off between flight duration and kerosene costs.


# One way vs Return   
As the one way route is not exactly flown as the return route, and as the same aircraft type will fly both flight legs, then only the maximum of both duration will be used in the optimization.

# Kerosene Costs   
The second optimization includes both flying costs and fuel costs. The result of this optimization retrieves another aircraft type. This means that the aircraft type with the lower flying costs , is not the aircraft type that burns the minimum kerosene, given the BADA performance parameters.

# Crew costs  
Crew costs must still be added.   
To be confirmed that these costs are only dependent upon flight duration.

# Example of an AirlineAircraftRoutesCosts.xls

Aircraft full name	Aircraft ICAO code	Departure Airport	Departure Airport ICAO code	Arrival Airport	Arrival Airport ICAO code	Flight duration (seconds)	Flight Duration (Decimal Hours)	Operational costs (US dollars)	take-off Mass (Kilograms)	Fuel Consumption Mass (Kilograms)	Fuel costs (US dollars)	Operational plus fuel costs (US dollars)
Airbus A319	A319	Atlanta-Hartsfield Jackson Atlanta Intl	KATL	Los Angeles-Los Angeles Intl	KLAX	15153.80	4.21	11533.73	70000.00	8947.78	9596.50	21130.22
Airbus A320	A320	Atlanta-Hartsfield Jackson Atlanta Intl	KATL	Los Angeles-Los Angeles Intl	KLAX	15811.00	4.39	12473.12	77000.00	10647.22	11419.14	23892.27

