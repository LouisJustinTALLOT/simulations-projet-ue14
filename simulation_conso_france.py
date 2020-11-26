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

NB_DONNEES = 11
LIGNE_CONSO_VEHICULES = 0
LIGNE_CONSO_BAT = 1
LIGNE_CONSO_EQUIP_ELEC = 2
LIGNE_CONSO_APP_ELEC = 3
LIGNE_PERDU_PROD_RAFF = 4
LIGNE_PERDU_PROD_SEMI_FINISHED = 5
LIGNE_RECYCLAGE_PRIMAIRE = 6
LIGNE_STOCK_VEHICULES = 7
LIGNE_STOCK_BAT = 8
LIGNE_STOCK_EQUIP_ELEC = 9
LIGNE_STOCK_APP_ELEC = 10


POURCENTAGE_PERDU_DEF_RAFFINEMENT_RAPP_CONSO = 1.75
POURCENTAGE_PERDU_DEF_SEMI_FINISHED_RAPP_CONSO = 1.09
POURCENTAGE_NEW_WASTE_RAPP_CONSO = 16.4

TEMPS_VEHICULES = 5
TEMPS_BAT = 50
TEMPS_EQUIP_ELEC = 10
TEMPS_APP_ELEC = 3

annee_actuelle = ANNEE_DEBUT

'''
TABLEAU
Enregistre toutes les données, année après années.
Système d'accès au tableau :
- l'indice de colonne correspond à année courante - année de départ
- la colonne correspond à la donnée intéressante suivant le code des constantes

'''
resultats = np.zeros( (NB_DONNEES, ANNEES) )


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
    global resultats
    #TODO à compléter avec les autres listes à mettre à jour aussi
    colonne_stock = calculerStockAnneeSuivante()
    resultats[0:NB_DONNEES, annee_actuelle - ANNEE_DEBUT]+=colonne_stock

    annee_actuelle+=1


'''
Donne le stock présent sur le territoire au 1/1/N+1. Ne modifie pas le taleau
Concrètement :
- récupère le stock au 1/1/N
- ajoute la consommation pendant l'année N
- enlève ce qui est parti du stock pendant l'année N

Retourne une colonne avec des données situées aux lignes des stocks et des 0 autre part (comme ça il suffit de le sommer)

TODO pour dispatcher selon quel type d'objet est dans le stock
'''
def calculerStockAnneeSuivante():
    stock_prec = np.zeros( (NB_DONNEES) )

    stock_prec[LIGNE_STOCK_VEHICULES] = getStockVehicules(annee_actuelle)
    stock_prec[LIGNE_STOCK_BAT] = getStockBat(annee_actuelle)
    stock_prec[LIGNE_STOCK_EQUIP_ELEC] = getStockEquipElec(annee_actuelle)
    stock_prec[LIGNE_STOCK_APP_ELEC] = getStockAppElec(annee_actuelle)

    stock_prec[LIGNE_STOCK_VEHICULES]+=getConsoVehicules(annee_actuelle)
    stock_prec[LIGNE_STOCK_BAT]+=getConsoBat(annee_actuelle)
    stock_prec[LIGNE_STOCK_EQUIP_ELEC]+=getConsoEquipElec(annee_actuelle)
    stock_prec[LIGNE_STOCK_APP_ELEC]+=getConsoAppElec(annee_actuelle)

    stock_prec[LIGNE_STOCK_VEHICULES]-= getSortieStockVehicules(annee_actuelle)
    stock_prec[LIGNE_STOCK_BAT]-= getSortieStockBat(annee_actuelle)
    stock_prec[LIGNE_STOCK_EQUIP_ELEC]-= getSortieStockEquipElec(annee_actuelle)
    stock_prec[LIGNE_STOCK_APP_ELEC]-= getSortieStockAppElec(annee_actuelle)

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
    return getConsoTotale(annee) + getPerduProductionTotal(annee) + getRecyclagePrimaire(annee)


def getConsoTotale(annee):
    return getConsoVehicules(annee) + getConsoBat(annee) + getConsoEquipElec(annee) + getConsoAppElec(annee)


def getConsoVehicules(annee):
    return resultats[LIGNE_CONSO_VEHICULES, annee_actuelle - ANNEE_DEBUT]

def getConsoBat(annee):
    return resultats[LIGNE_CONSO_BAT, annee_actuelle - ANNEE_DEBUT]

def getConsoEquipElec(annee):
    return resultats[LIGNE_CONSO_EQUIP_ELEC, annee_actuelle - ANNEE_DEBUT]

def getConsoAppElec(annee):
    return resultats[LIGNE_CONSO_APP_ELEC, annee_actuelle - ANNEE_DEBUT]

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






## Accesseurs partie stock (il faut prendre garde à avoir déjà calculé la valeur correspondante !)

def getStock(annee):
    return getStockVehicules(annee) + getStockBat(annee) + getStockEquipElec(annee) + getStockAppElec(annee)


def getStockVehicules(annee):
    return resultats[LIGNE_STOCK_VEHICULES, annee_actuelle - ANNEE_DEBUT]

def getStockBat(annee):
    return resultats[LIGNE_STOCK_BAT, annee_actuelle - ANNEE_DEBUT]

def getStockEquipElec(annee):
    return resultats[LIGNE_STOCK_EQUIP_ELEC, annee_actuelle - ANNEE_DEBUT]

def getStockAppElec(annee):
    return resultats[LIGNE_STOCK_APP_ELEC, annee_actuelle - ANNEE_DEBUT]




## Accesseurs partie après le stock (à TODO) :

'''
Donne ce qui sort des stocks:
- ce qui va être recyclé (fin de vie, old-waste), somme de toutes les catégories
- ce qui va être perdu définitivement (abandonné, non-recyclé et perdu lors du recyclage)
'''
def getSortieStock(annee):
    return getSortieStockVehicules(annee) + getSortieStockBat(annee) + getSortieStockEquipElec(annee) + getSortieStockAppElec(annee)


def getSortieStockVehicules(annee):
    return resultats[LIGNE_CONSO_VEHICULES, annee - TEMPS_VEHICULES]

def getSortieStockBat(annee):
    return resultats[LIGNE_CONSO_BAT, annee - TEMPS_BAT]

def getSortieStockEquipElec(annee):
    return resultats[LIGNE_CONSO_EQUIP_ELEC, annee - TEMPS_EQUIP_ELEC]

def getSortieStockAppElec(annee):
    return resultats[LIGNE_CONSO_APP_ELEC, annee - TEMPS_APP_ELEC]




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