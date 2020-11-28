import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''Comment ça fonctionne ?
 - on calcule en premier lieu les consommations estimées (connu)
 - on lance la simulation :
   - il y a un champ d'année courante
   - on calcule au fur et à mesure les stocks (et autres variables) de l'année suivante, 
     à l'aide notamment des données de l'année précédente
   - on ajoute au tableau les nouvelles données
   - on recommence
 - on plot les résultats joliment
'''


'''CONSTANTES'''

ANNEE_DEBUT = 2018
ANNEE_FIN = 2050
NB_ANNEES = ANNEE_FIN - ANNEE_DEBUT

RANGE_ANNEES = np.array([a for a in range(ANNEE_DEBUT, ANNEE_FIN+1)])

NB_DONNEES = 11
NB_CAT = 4

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

liste_categories = ["Vehicules", "Batiments", "Equipement electronique", "Appareils electroniques"]

dict_categories_stock = {"Vehicules" : LIGNE_STOCK_VEHICULES,
                            "Batiments" : LIGNE_STOCK_BAT,
                            "Equipement electronique" : LIGNE_STOCK_EQUIP_ELEC, 
                            "Appareils electroniques" : LIGNE_STOCK_APP_ELEC}

dict_categories_conso = {"Vehicules" : LIGNE_CONSO_VEHICULES,
                            "Batiments" : LIGNE_CONSO_BAT,
                            "Equipements electroniques" : LIGNE_CONSO_EQUIP_ELEC, 
                            "Appareils electroniques" : LIGNE_CONSO_APP_ELEC}


POURCENTAGE_PERDU_DEF_RAFFINEMENT_RAPP_CONSO = 1.75/100
POURCENTAGE_PERDU_DEF_SEMI_FINISHED_RAPP_CONSO = 1.09/100
POURCENTAGE_NEW_WASTE_RAPP_CONSO = 16.4/100

TEMPS_VEHICULES = 5
TEMPS_BAT = 50
TEMPS_EQUIP_ELEC = 10
TEMPS_APP_ELEC = 3

dict_temps = {}
dict_temps[LIGNE_STOCK_VEHICULES] = TEMPS_VEHICULES
dict_temps[LIGNE_STOCK_BAT] = TEMPS_BAT
dict_temps[LIGNE_STOCK_EQUIP_ELEC] = TEMPS_EQUIP_ELEC
dict_temps[LIGNE_STOCK_APP_ELEC] = TEMPS_APP_ELEC

'''TABLEAU
Enregistre toutes les données, année après années.
Système d'accès au tableau :
- l'indice de colonne correspond à année courante - année de départ
- la colonne correspond à la donnée intéressante suivant le code des constantes

'''

resultats = np.zeros( (NB_DONNEES, NB_ANNEES) )

# Traçage des résultats :

def tracer_resultats(tableau):
    """Trace un tableau numpy correspondant aux résultats de la simulation"""
    plt.close()

    for no_donnee in range(NB_DONNEES):
        plt.plot(tableau[no_donnee,:],RANGE_ANNEES)
        plt.figure()

    plt.show()

## Accesseurs partie production (tout est initialisé avant, on peut y accéder sans pb)

# getConsoTotale
def getConsoVehicules(annee):
    return resultats[LIGNE_CONSO_VEHICULES, annee_actuelle - ANNEE_DEBUT]

def getConsoBat(annee):
    return resultats[LIGNE_CONSO_BAT, annee_actuelle - ANNEE_DEBUT]

def getConsoEquipElec(annee):
    return resultats[LIGNE_CONSO_EQUIP_ELEC, annee_actuelle - ANNEE_DEBUT]

def getConsoAppElec(annee):
    return resultats[LIGNE_CONSO_APP_ELEC, annee_actuelle - ANNEE_DEBUT]

def getConsoTotale(annee):
    return getConsoVehicules(annee) + getConsoBat(annee) + getConsoEquipElec(annee) + getConsoAppElec(annee)

def getConsoTotale(no_annee):
def getLignesConso():
    return resultats[0:NB_CAT,0:NB_ANNEES]


# getPerduProductionTotal
def getPerduProductionRaffinement(no_annee):
    '''Donne ce qui est perdu définitivement lors de la partie raffinement de la production'''
    return resultats[LIGNE_PERDU_PROD_RAFF, no_annee]

def getPerduProductionSemiFinished(no_annee):
    '''Donne ce qui est perdu définitivement lors de la production des semi-finished goods'''
    return resultats[LIGNE_PERDU_PROD_SEMI_FINISHED, no_annee]

def getPerduProductionTotal(no_annee):
    '''Donne ce qui est perdu définitivement lors de la production (raffinement + semi-finished goods)'''
    return getPerduProductionRaffinement(no_annee) + getPerduProductionSemiFinished(no_annee)


# getRecyclagePrimaire
def getRecyclagePrimaire(no_annee):
    '''Donne ce qui part en recyclage primaire (new waste)'''
    return resultats[LIGNE_RECYCLAGE_PRIMAIRE, no_annee]


# getBesoin
def getBesoin(no_annee):
    '''Donne le besoin du pays pour l'année, en intégrant à la fois
    - ce qui sera consommé
    - ce qui sera perdu définitivement (raffinement + semi-finished goods)
    - ce qui partira en recyclage primaire (new-waste)
    Ca correspond à ce qui rentre dans le processus de production
    '''
    return getConsoTotale(no_annee) + getPerduProductionTotal(no_annee) + getRecyclagePrimaire(no_annee)


## Accesseurs partie stock (il faut prendre garde à avoir déjà calculé la valeur correspondante !)

def getStockVehicules(annee):
    return resultats[LIGNE_STOCK_VEHICULES, annee_actuelle - ANNEE_DEBUT]

def getStockBat(annee):
    return resultats[LIGNE_STOCK_BAT, annee_actuelle - ANNEE_DEBUT]

def getStockEquipElec(annee):
    return resultats[LIGNE_STOCK_EQUIP_ELEC, annee_actuelle - ANNEE_DEBUT]

def getStockAppElec(annee):
    return resultats[LIGNE_STOCK_APP_ELEC, annee_actuelle - ANNEE_DEBUT]

def getStock(annee):
    return getStockVehicules(annee) + getStockBat(annee) + getStockEquipElec(annee) + getStockAppElec(annee)

def getStock(no_annee): 

## Accesseurs partie après le stock (à TODO) :

'''Donne ce qui sort des stocks:
- ce qui va être recyclé (fin de vie, old-waste), somme de toutes les catégories
- ce qui va être perdu définitivement (abandonné, non-recyclé et perdu lors du recyclage)
'''
# getSortieStock
def getSortieStockVehicules(annee):
    return resultats[LIGNE_CONSO_VEHICULES, annee - TEMPS_VEHICULES]

def getSortieStockBat(annee):
    return resultats[LIGNE_CONSO_BAT, annee - TEMPS_BAT]

def getSortieStockEquipElec(annee):
    return resultats[LIGNE_CONSO_EQUIP_ELEC, annee - TEMPS_EQUIP_ELEC]

def getSortieStockAppElec(annee):
    return resultats[LIGNE_CONSO_APP_ELEC, annee - TEMPS_APP_ELEC]

def getSortieStockCategorie(no_annee, categorie_stock):

def getSortieStock(no_annee):

def getRecyclageSecondaire(no_annee):
    '''Donne ce qui va partir en recyclage secondaire et donc revenir dans la production'''
    pass


def getAbandonne(no_annee, categorie):
    '''Donne ce qui sort des stocks mais qui est abandonne'''
    pass


def getNonRecycle(no_annee, categorie):
    '''Donne ce qui n'est pas recyclé (mauvaise poubelle)'''
    pass


def getPerduRecyclageSecondaire(no_annee, categorie):
    '''Donne ce qui est perdu lors du recyclage secondaire (rendement)'''
    pass


# Accesseur au tableau :

def getRecyclageTotal(no_annee):
    '''Donne tout ce qui entre en production par le recyclage (new-waste et old-waste)'''
    return getRecyclagePrimaire(no_annee) + getRecyclageSecondaire(no_annee)


def calculerStockAnneeSuivante(no_annee):
    '''Donne le stock présent sur le territoire au 1/1/N+1. Ne modifie pas le taleau
    Concrètement :
    - récupère le stock au 1/1/N
    - ajoute la consommation pendant l'année N
    - enlève ce qui est parti du stock pendant l'année N

    Retourne une colonne avec des données situées aux lignes des stocks et des 0 autre part (comme ça il suffit de le sommer)

    TODO pour dispatcher selon quel type d'objet est dans le stock
    '''
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


# Les fonctions qui construisent l'année suivante

def doAnneeSuivante(no_annee):
    '''Calcule l'année suivante, donc ajoute à chaque ligne concernée un élément de plus
    Concrètement, on calcule les données de année_actuelle+1 à l'aide des données de année_actuelle

    Modifie le tableau !
    '''
    # global annee_actuelle
    global resultats
    #TODO à compléter avec les autres listes à mettre à jour aussi
    colonne_stock = calculerStockAnneeSuivante(no_annee)
    resultats[0:NB_DONNEES, no_annee]+=colonne_stock

    # annee_actuelle+=1


# Les fonctions avant de lancer la simulation

def initialiser(): #TODO
    '''Initialise le tableau, avec les données qui peuvent être initialisées avant:
    - la consommation
    - les pertes définitivites
    - ce qui part au recyclage primaire
    A faire au départ !
    '''
    # A FAIRE : on établit la ligne de consommations

    resultats[LIGNE_PERDU_PROD_RAFF] = getLignesConso().sum(axis=-2)*POURCENTAGE_PERDU_DEF_RAFFINEMENT_RAPP_CONSO
    resultats[LIGNE_PERDU_PROD_SEMI_FINISHED] = getLignesConso().sum(axis=-2)*POURCENTAGE_PERDU_DEF_SEMI_FINISHED_RAPP_CONSO
    resultats[LIGNE_RECYCLAGE_PRIMAIRE] = getLignesConso().sum(axis=-2)*POURCENTAGE_NEW_WASTE_RAPP_CONSO


# Programme principal

def simul():
    '''Réalise la simulation'''
    initialiser()
    for a in range(NB_ANNEES):
        doAnneeSuivante(a)
    #TODO
    tracer_resultats(resultats)
