
# Model Description


## Mathematical model

The model is a linear (mixed-integer) optimisation model for the Jordanian
electricity and water system.

### Definitions

#### Sets


| Symbol | Index | Description                    |
|--------|-------|--------------------------------|
| $T$    | $t$   | Timesteps                      |
| $R$    | $r$   | Renewable units                |
| $C$    | $c$   | Conventional units             |
| $S$    | $S$   | Storage units                  |
| $U$    | $u$   | All supply units ($R \cup C$)  |


#### Variables


| Symbol          | Description                                                |
|-----------------|------------------------------------------------------------|
| $p_{u,t}$       | Power output  unit u at timestep $t$                       |
| $h_{c,t}$       | Fuel consumption of unit c at timestep $t$                 |
| $s^{in}_{s,t}$  | Storage charge of storage $s$ at timestep $t$              |
| $s^{out}_{s,t}$ | Storage discharge  of storage $s$ at timestep $t$          |
| $e_{s,t}$       | Storage level of storage $s$ at timestep $t$               |
| $y_{c,t}$       | Status if unit $c$ is committet  (binary) at timestep $t$  |
| $shortage_t$    | Shortage variable                                          |
| $excess_t$      | Excess variable                                            |


#### Parameter


| Symbol                | Description                            |
|-----------------------|----------------------------------------|
| $p^{max/min}_{u}$     | Normalised maximum production level    |
| $p^{max/min}_{u}$     | Normalised maximum production level    |
| $P^{nom,el}_{u}$      | Nominal power capacity of unit $u$     |
| $E^{nom}_{s}$         | Nominal storage energy capacity        |
| $d^{el}_{t}$          | Electricity demand                     |
| $\eta^{loss}_s$       | Standing loss of storage               |
| $\eta^{in}_s$         | Charge efficiency of storage           |
| $\eta^{out}_s$        | Discharge efficiency of storage        |
| $c^{opex}_u$          | Operational expenditure                |



### Objective function

The model minimises total operational cost of the system.

 $$ \text{min} : \sum_{u \in U} p_u \cdot c^{opex}_u + shortage_t \cdot 3000 \label{eq:objective}$$

### Demand constraint

Demand must equal the sum of supply of all producing units and storage output.

$$ \sum_u p_{u, t} + \sum_s s^{out}_{s,t} - \sum_s s^{in}_{s,t} + shortage_t - excess_t = d^{el}_t \qquad \forall t$$


### Supply constraints and fuel consumption

$$ \cdot P^{nom}_{u} \cdot \underline{p}_{u} \leq p_{u, t} \leq \cdot P^{nom}_{u} \cdot \overline{p}_{u}  \qquad \forall u, t$$

$$ h_{c,t} =  \frac{p_{c,t}}{\eta_{c}} \qquad \forall c,t$$

*Optional*

If P-min constraint is set, operation will be restricted by binary variables:

$$ y_{c, t} \cdot P^{nom}_{c} \cdot \underline{p}_{c} \leq p_{c, t} \leq y_{c, t} \cdot P^{nom}_{c} \cdot \overline{p}_{c}  \qquad \forall c, t$$

For modelling part-load efficiency the following equation applies:

$$ h_{c,t} = y_{c,t} \cdot a_{c,t} + b_{c,t} \cdot p_{c,t} \qquad \forall c,t$$


### Storage equations

$$ e_{s, t} = e_{s, t-1} \cdot \eta^{loss}_s - \frac{s^{out}_{s,t}}{\eta^{out}_{s}}   + s^{in}_{s,t} \cdot \eta^{in}_{s}  \qquad \forall s,t $$

$$ 0 \leq e_{s,t} \leq E^{nom}_{s,t} \qquad \forall s,t  $$
