import matplotlib.pyplot as plt
import numpy as np

## les données

#              0         1                   2                          3 
#       cat = Véhicules Batiments Equipements_electroménagers Appareils_électroniques

liste_ages = np.array([10, 50, 10, 3])
liste_stocks = [1_000_000, 20_000_000,  225_000,10_000]
liste_conso = [200_000, 200_000, 20_000,2_500]

## Premier dessin : histogramme avec les catégories pour les durées de vie


plt.bar(["Véhicules", "Bâtiments", "Equipements\nélectroménagers", "Appareils\nélectroniques" ],
        liste_ages)
plt.xticks(rotation=45)
# plt.show()


## deuxième dessin : les stocks

plt.figure()
plt.bar(["Véhicules", "Bâtiments", "Equipements\nélectroménagers", "Appareils\nélectroniques" ],
        liste_stocks)
plt.xticks(rotation=45)
# plt.show()

