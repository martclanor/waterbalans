"""

Dit voorbeeld bevat de automatische simulatie van een waterbalans op
EAG-niveau. De volgende drie invoerbestanden worden gebruikt:

- Modelstructuur
- Tijdreeksen
- Parameters

"""

import pandas as pd
import waterbalans as wb
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.interactive(True)

# Set database url connection
wb.pi.setClient(wsdl='http://localhost:8081/FewsPiService/fewspiservice?wsdl')

buckets = pd.read_csv("data\\opp_19578_2501-EAG-1.csv", delimiter=";",
                      decimal=",")
buckets["OppWaarde"] = pd.to_numeric(buckets.OppWaarde)
name = "2501-EAG-01"
id = 1

# Aanmaken van modelstructuur en de bakjes.
e = wb.create_eag(id, name, buckets)

# Lees de tijdreeksen in
reeksen = pd.read_csv("data\\reeks_19578_2501-EAG-1.csv", delimiter=";",
                      decimal=",")
e.add_series(reeksen)

# Simuleer de waterbalans
params = pd.read_csv("data\\param_19578_2501-EAG-1.csv", delimiter=";",
                     decimal=",")
params.rename(columns={"ParamCode": "Code"}, inplace=True)
params["Waarde"] = pd.to_numeric(params.Waarde)

e.simulate(params=params, tmin="2000", tmax="2015-12-31")

# Calculate and plot the fluxes as a bar plot
e.plot.aggregated(tmin="2000", tmax="2010")

# Calculate and plot the chloride concentration
C = e.calculate_chloride_concentration()

plt.show()
