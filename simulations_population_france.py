import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

''''
Comment ça fonctionne ?
 - on calcule en premier lieu les consommations estimées (connu)
 - on lance la simulation : il y a un champ d'année courante, et on calcule au fur et à mesure les stocks de l'année suivante
''''


'''
LISTES
Enregistrent toutes les données, année après années.
Système d'accès aux listes : l'indice dans la liste correspond à annee courante - annee de départ
Listes (TODO à compléter):
- consommations suit l'évolution de la consommation. Calculée avant
- stock suit l'état du stock. Calculé au fur et à mesure


'''
consommations = []
stock = []


'''
CONSTANTES
'''
ANNEE_DEBUT = 2018
STOCK_DEBUT = 50
ANNEE_FIN = 2050


POURCENTAGE_PERDU_DEF_RAFFINEMENT_RAPP_CONSO = 1.75
POURCENTAGE_PERDU_DEF_SEMI_FINISHED_RAPP_CONSO = 1.09
POURCENTAGE_NEW_WASTE_RAPP_CONSO = 16.4

'''
CHAMPS
- annee_actuelle indique que l'on se trouve au 1er janvier de l'année spécifiée.
'''
annee_actuelle = ANNEE_DEBUT

'''
Initialise la liste des consommations annuelles
A faire au départ !
TODO
'''
def initListeConso():
    pass


# Les fonctions principales


'''
Donne le besoin du pays pour l'année, en intégrant à la fois
- ce qui sera consommé
- ce qui sera perdu définitivement (raffinement + semi-finished goods)
- ce qui partira en recyclage primaire (new-waste)
Ca correspond à ce qui rentre dans le processus de production
'''
def getBesoin(annee):
    return getConsommation(annee) + getPerduProductionTotal(annee) + getRecyclagePrimaire(annee)

'''
Donne la consommation nécessaire du pays l'année donnée
Accède a la liste initialisée au départ
TODO
'''
def getConsommation(annee):
    return consommations[annee - ANNEE_DEBUT]


'''
Calcule l'année suivante, donc ajoute à chaque liste concernée un élément de plus
Concrètement, on calcule les données de année année_actuelle+1 à l'aide des données de année_actuelle
'''
def doAnneeSuivante():
    stock.append(calculerStockAnneeSuivante())
    #TODO à compléter avec les autres listes à mettre à jour aussi


    annee_actuelle+=1


'''
Donne le stock présent sur le territoire au 1/1/N+1. Ne modifie pas la liste.
Concrètement :
- récupère le stock au 1/1/N
- ajoute la consommation pendant l'année N
- enlève ce qui est parti du stock pendant l'année N
'''
def calculerStockAnneeSuivante():
    stock_prec = getStock(annee_actuelle)
    stock_prec+=getConsommation(annee_actuelle)
    stock_prec-=getSortieStock(annee_actuelle)

    return stock_prec


# Les fonctions secondaires


'''
Donne ce qui est perdu définitivement lors de la production (raffinement + semi-finished goods)
'''
def getPerduProductionTotal(annee):
    return getPerduProductionRaffinement(annee) + getPerduProductionSemiFinished(annee)

'''
Donne ce qui est perdu définitivement lors de la partie raffinement de la production
'''
def getPerduProductionRaffinement(annee):
    return POURCENTAGE_PERDU_DEF_RAFFINEMENT_RAPP_CONSO*getConsommation(annee)

'''
Donne ce qui est perdu définitivement lors de la production des semi-finished goods
'''
def getPerduProductionSemiFinished(annee):
    return POURCENTAGE_PERDU_DEF_SEMI_FINISHED_RAPP_CONSO*getConsommation(annee)

'''
Donne ce qui part en recyclage primaire (new waste)
'''
def getRecyclagePrimaire(annee):
    return POURCENTAGE_NEW_WASTE_RAPP_CONSO*getConsommation(annee)





'''
Donne tout ce qui entre en production par le recyclage (new-waste et old-waste)
'''
def getRecyclageTotal(annee):
    return getRecyclagePrimaire(annee) + getRecyclageSecondaire(annee)


# La partie suivante est vraiment à TODO, c'est un gros morceau



'''
Donne ce qui sort des stocks:
- ce qui va être recyclé (fin de vie, old-waste)
- ce qui va être perdu définitivement (abandonné, non-recyclé et perdu lors du recyclage)
'''
def getSortieStock(annee):
    pass


'''
Donne ce qui va partir en recyclage secondaire et donc revenir dans la production
'''
def getRecyclageSecondaire(annee):
    pass


'''
Donne ce qui sort des stocks mais qui est abandonne
'''
def getAbandonne(annee):
    pass


'''
Donne ce qui n'est pas recyclé (mauvaise poubelle)
'''
def getNonRecycle(annee):
    pass



'''
Donne ce qui est perdu lors du recyclage secondaire (rendement)
'''
def getPerduRecyclageSecondaire(annee):
    pass