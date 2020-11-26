import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
Comment ça fonctionne ?
 - on calcule en premier lieu les consommations estimées (connu)
 - on lance la simulation :
   - il y a un champ d'année courante
   - on calcule au fur et à mesure les stocks (et autres variables) de l'année suivante, à l'aide notamment des données de l'année précédente
   - on ajoute au tableau les nouvelles données
   - on recommence
 - on plot les résultats joliment
'''


'''
CONSTANTES
'''
ANNEE_DEBUT = 2018
ANNEE_FIN = 2050
ANNEES = ANNEE_FIN - ANNEE_DEBUT

NB_DONNEES = 10
LIGNE_CONSO = 0
LIGNE_STOCK = 1
LIGNE_PERDU_PROD_RAFF = 2
LIGNE_PERDU_PROD_SEMI_FINISHED = 3
LIGNE_RECYCLAGE_PRIMAIRE = 4


POURCENTAGE_PERDU_DEF_RAFFINEMENT_RAPP_CONSO = 1.75
POURCENTAGE_PERDU_DEF_SEMI_FINISHED_RAPP_CONSO = 1.09
POURCENTAGE_NEW_WASTE_RAPP_CONSO = 16.4

annee_actuelle = ANNEE_DEBUT

'''
TABLEAU
Enregistre toutes les données, année après années.
Système d'accès au tableau :
- l'indice de colonne correspond à année courante - année de départ
- la colonne correspond à la donnée intéressante suivant le code des constantes

'''
resultats = np.empty( (NB_DONNEES, ANNEES) )


# Programme principal
'''
Fait tout
'''
def simul():
    initialiser()
    while annee_actuelle < ANNEE_FIN:
        doAnneeSuivante()
    #TODO


# Les fonctions avant de lancer la simulation

'''
Initialise le tableau, avec les données qui peuvent être initialisées avant:
- la consommation
- les pertes définitivites
- ce qui part au recyclage primaire
A faire au départ !
TODO
'''
def initialiser():
    # A FAIRE : on établit la ligne de consommations

    resultats[LIGNE_PERDU_PROD_RAFF] = resultats[LIGNE_CONSO]*POURCENTAGE_PERDU_DEF_RAFFINEMENT_RAPP_CONSO
    resultats[LIGNE_PERDU_PROD_SEMI_FINISHED] = resultats[LIGNE_CONSO]*POURCENTAGE_PERDU_DEF_SEMI_FINISHED_RAPP_CONSO
    resultats[LIGNE_RECYCLAGE_PRIMAIRE] = resultats[LIGNE_CONSO]*POURCENTAGE_NEW_WASTE_RAPP_CONSO


# Les fonctions qui construisent l'année suivante

'''
Calcule l'année suivante, donc ajoute à chaque ligne concernée un élément de plus
Concrètement, on calcule les données de année année_actuelle+1 à l'aide des données de année_actuelle

Modifie le tableau !
'''
def doAnneeSuivante():
    global annee_actuelle
    resultats[LIGNE_STOCK, annee_actuelle - ANNEE_DEBUT] = calculerStockAnneeSuivante()
    #TODO à compléter avec les autres listes à mettre à jour aussi

    annee_actuelle+=1


'''
Donne le stock présent sur le territoire au 1/1/N+1. Ne modifie pas le taleau
Concrètement :
- récupère le stock au 1/1/N
- ajoute la consommation pendant l'année N
- enlève ce qui est parti du stock pendant l'année N

TODO pour dispatcher selon quel type d'objet est dans le stock
'''
def calculerStockAnneeSuivante():
    stock_prec = getStock(annee_actuelle)
    stock_prec+=getConsommation(annee_actuelle)
    stock_prec-=getSortieStock(annee_actuelle)

    return stock_prec


# Accesseur au tableau :

'''
Donne tout ce qui entre en production par le recyclage (new-waste et old-waste)
'''
def getRecyclageTotal(annee):
    return getRecyclagePrimaire(annee) + getRecyclageSecondaire(annee)

## Accesseurs partie production (tout est initialisé avant, on peut y accéder sans pb)

'''
Donne le besoin du pays pour l'année, en intégrant à la fois
- ce qui sera consommé
- ce qui sera perdu définitivement (raffinement + semi-finished goods)
- ce qui partira en recyclage primaire (new-waste)
Ca correspond à ce qui rentre dans le processus de production
'''
def getBesoin(annee):
    return getConsommation(annee) + getPerduProductionTotal(annee) + getRecyclagePrimaire(annee)


def getConsommation(annee):
    return resultats[LIGNE_CONSO, annee - ANNEE_DEBUT]

'''
Donne ce qui est perdu définitivement lors de la production (raffinement + semi-finished goods)
'''
def getPerduProductionTotal(annee):
    return getPerduProductionRaffinement(annee) + getPerduProductionSemiFinished(annee)

'''
Donne ce qui est perdu définitivement lors de la partie raffinement de la production
'''
def getPerduProductionRaffinement(annee):
    return resultats[LIGNE_PERDU_PROD_RAFF, annee_actuelle - ANNEE_DEBUT]

'''
Donne ce qui est perdu définitivement lors de la production des semi-finished goods
'''
def getPerduProductionSemiFinished(annee):
    return resultats[LIGNE_PERDU_PROD_SEMI_FINISHED, annee_actuelle - ANNEE_DEBUT]

'''
Donne ce qui part en recyclage primaire (new waste)
'''
def getRecyclagePrimaire(annee):
    return resultats[LIGNE_RECYCLAGE_PRIMAIRE, annee_actuelle - ANNEE_DEBUT]



## Accesseurs partie stock

def getStock(annee):
    return resultats[LIGNE_STOCK, annee - ANNEE_DEBUT]




## Accesseurs partie après le stock (à TODO)

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