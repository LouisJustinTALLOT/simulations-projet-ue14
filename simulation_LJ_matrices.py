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
          et non perdu dans les opérations de recyclage
CA(n) la consommation annuelle, en pourcentage de la consommation de l'année précédente

obtenu_recyclage(n) la quantité obtenue de cuivre sur toutes les catégories, à l'année n
                    c'est la quantité qui nous intéresse, à comparer à 
conso_totale(n) la quantité totale de cuivre consommée, sur toutes les catégories

lu = [1, ..., 1] vecteur ligne permettant de sommer sur les catégories

Les équations sont les suivantes :

r(n) = RR(n) * PR(n) * SS(n) * s(n)
c(n) = CA(n) * c(n-1)
s(n+1) - s(n) = c(n) - SS(n) * s(n)

"""

NB_CATEGORIES = 4

ANNEE_DEBUT = 2020
ANNEE_FIN = 2050

SS_0 = np.diag([...])
TP_0 = np.diag([...])
PR_0 = np.diag([...])
RR_0 = np.diag([...])
CA_0 = np.diag([...])

lu = np.ones((NB_CATEGORIES))

# Trois dictionnaires pour la mémoïsation dans les fonctions récursives

dico_c = {}
dico_s = {}
dico_r = {}

# on initialise les dictionnaires

dico_c[...] = ...
dico_s[...] = ...
dico_r[...] = ...

def somme_vecteur(vec):
    return np.float(np.dot(lu, vec))

def SS(n):
    """en premier modèle, c'est une fonction constante : 
    dans toutes les catégories, une portion constante du stock devient "hors d'usage" 
    et en sort pour partir en partie au recyclage
    """

    return SS_0

def TP(n):
    """en premier modèle, c'est une fonction constante : 
    le temps de passage est constant dans toutes les catégories"""
    return TP_0

def PR(n):
    """en premier modèle, c'est une fonction constante : 
    on recycle une portion constante des 'biens' "usagés" dans toutes les catégories"""

    return PR_0

def RR(n):
    """en premier modèle, c'est une fonction constante : 
     dans toutes les catégories, on arrive à récupérer un taux constant de cuivre"""

    return RR(0)

def CA(n):
    """en tout premier modèle, c'est une fonction constante : 
    nous considérons la consommation constante dans toutes les catégories"""
    return CA_0

def r(n):
    if n in dico_r:
        return dico_r[n]
    
    res = np.dot(RR(n),np.dot(PR(n),np.dot(SS(n), s(n))))

    dico_r[n] = res # pour la mémoïsation
    return res

def c(n):
    """en premier modèle on considère que la consommation croît d'un
    pourcentage constant tous les ans, donné par CA(n)

    ce pourcentage pourra néanmoins augmenter avec les années
    """
    if n in dico_c:
        return dico_c[n]
    res = np.dot(CA(n), c(n-1))
    dico_c[n] = res
    return res

def s(n):
    """Ici l'expression de s(n) n'est pas dépendante du modèle"""

    if n in dico_s:
        return dico_s[n]
    res = c(n) + np.dot((np.eye(NB_CATEGORIES)-SS(n-1)), s(n-1))
    dico_s[n] = res
    return res


def obtenu_recyclage(n):
    return somme_vecteur(r(n))

def conso_totale(n):
    return somme_vecteur(c(n))


def simulation(annee_fin):
    pass