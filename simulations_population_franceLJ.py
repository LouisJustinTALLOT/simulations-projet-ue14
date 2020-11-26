import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

annees = [2016, 2015 ]
pop_france = [67751838, 67609086]

file = "pop-france.xls"
df = pd.read_excel(file)
print(df.head())

plt.scatter(df['Année'], df["Population"])
plt.show()