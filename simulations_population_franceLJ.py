import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn as sk

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
modeleRegLin = sk.linear_model.LinearRegression()
print(X)
futur = []
modeleRegLin.fit(np.array(df["Année"]).reshape(-1, 1),df["Population"])
# print(modeleRegLin.get_params())
# print(modeleRegLin.coef_)
# print(modeleRegLin.intercept_)
# print(modeleRegLin.coef_)
# plt.plot(np.array(df["Année"]).reshape(-1, 1),df["Population"],'.')
# plt.show()

print(sk.metrics)