import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

annees = [2016, 2015 ]
pop_france = [67751838, 67609086]

file = "pop-france.xls"
df = pd.read_excel(file)
# print(df.head())

# plt.scatter(df['Année'], df["Population"])
# plt.show()    
# print(repr(df["Année"]))
# print("")
# print(df.columns.drop("Année"))
# print("")
y = df.Population
X = np.array(df["Année"]).reshape(-1, 1)
modeleRegLin = LinearRegression()
# print(X)

futur = np.array([[a] for a in range(2021,2051)])
# print(futur)
modeleRegLin.fit(np.array(df["Année"])[-5:].reshape(-1, 1),df["Population"][-5:])
# print(modeleRegLin.get_params())
# print(modeleRegLin.coef_)
# print(modeleRegLin.inte
#rcept_)
# print(modeleRegLin.coef_)
plt.plot(np.array(df["Année"]).reshape(-1, 1),df["Population"],'.')
# plt.figure()
plt.plot(futur, modeleRegLin.predict(futur),'.')
plt.show()

# print(sk.metrics)
# print(r2_score(y,modeleRegLin.predict(X)))