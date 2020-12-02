import numpy as np  
import matplotlib.pyplot as plt
from scipy.integrate import odeint


""" On a le modèle suivant :
c(n) le vecteur consommation à l'année n
s(n) le vecteur stock à l'année n
r(n) le vecteur "quantité récupérée par recyclage" à l'année n

SS(n) la matrice diagonale représentant la quantité sortant du stock à l'année n...
TP(n) qui représente le temps de résidence dans une catégorie du cuivre
PR(n) la matrice diagonale représentant le pourcentage recylé de matériau sortant du stock
RR(n) ... représentant le pourcentage du matériau recyclé qui est valorisé,
          et pas perdu dans les opérations de recyclage
CA(n) la consommation annuelle, en pourcentage de la consompmation de l'année précédente

obtenu_recyclage(n) la quantité obtenue de cuivre sur toutes les catégories, à l'année n
                    c'est la quantité qui nous intéresse, à comparer à 
conso_totale(n) la quantité totale de cuivre consommée, sur toutes les catégories

lu = [1, ..., 1] vecteur ligne permettant de sommer sur les catégories

Les équations sont les suivantes :

r(n) = RR(n) * PR(n) * SS(n) * s(n)
c(n) = CA(n) * CA(n-1)
s(n+1) - s(n) = c(n) - SS(n) * s(n)

"""

NB_CATEGORIES = 4

SS_0 = np.diag([...])
TP_0 = np.diag([...])
PR_0 = np.diag([...])
RR_0 = np.diag([...])
CA_0 = np.diag([...])

lu = np.ones((NB_CATEGORIES))

def somme_vecteur(vec, ligne_unitaire = lu):
    return np.float(np.dot(lu, vec))
