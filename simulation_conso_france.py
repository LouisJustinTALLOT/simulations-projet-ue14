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

NOM_VEHICULES = "Vehicules"
NOM_BAT = "Batiments"
NOM_EQUIP_ELEC = "Equipements Electroniques"
NOM_APP_ELEC = "Appareils Electroniques"

LIGNE_CONSO_VEHICULES = 0
LIGNE_CONSO_BAT = 1
LIGNE_CONSO_EQUIP_ELEC = 2
LIGNE_CONSO_APP_ELEC = 3
LIGNE_PERDU_PROD_RAFF = 4
LIGNE_PERDU_PROD_SEMI_FINISHED = 5
LIGNE_RECYCLAGE_PRIMAIRE = 6
# catégories de consommation
LIGNE_STOCK_VEHICULES = 7
LIGNE_STOCK_BAT = 8
LIGNE_STOCK_EQUIP_ELEC = 9
LIGNE_STOCK_APP_ELEC = 10

POURCENTAGE_PERDU_DEF_RAFFINEMENT_RAPP_CONSO = 1.75/100
POURCENTAGE_PERDU_DEF_SEMI_FINISHED_RAPP_CONSO = 1.09/100
POURCENTAGE_NEW_WASTE_RAPP_CONSO = 16.4/100

TEMPS_VEHICULES = 5
TEMPS_BAT = 50
TEMPS_EQUIP_ELEC = 10
TEMPS_APP_ELEC = 3

POURCENTAGE_RECYCLE_VEHICULES = 90/100
POURCENTAGE_RECYCLE_BAT = 95/100
POURCENTAGE_RECYCLE_EQUIP_ELEC = 70/100
POURCENTAGE_RECYCLE_APP_ELEC = 60/100

RENDEMENT_RECYCLE_VEHICULES = 70/100
RENDEMENT_RECYCLE_BAT = 60/100
RENDEMENT_RECYCLE_EQUI_ELEC = 80/100
RENDEMENT_RECYCLE_APP_ELEC = 75/100



liste_categories = [NOM_VEHICULES, NOM_BAT, NOM_EQUIP_ELEC, NOM_APP_ELEC]

dict_categories_stock = {NOM_VEHICULES : LIGNE_STOCK_VEHICULES,
                            NOM_BAT : LIGNE_STOCK_BAT,
                            NOM_EQUIP_ELEC : LIGNE_STOCK_EQUIP_ELEC, 
                            NOM_APP_ELEC : LIGNE_STOCK_APP_ELEC}

dict_categories_conso = {NOM_VEHICULES : LIGNE_CONSO_VEHICULES,
                            NOM_BAT : LIGNE_CONSO_BAT,
                            NOM_EQUIP_ELEC : LIGNE_CONSO_EQUIP_ELEC, 
                            NOM_APP_ELEC : LIGNE_CONSO_APP_ELEC}



dict_portion_recyclee = {NOM_VEHICULES : POURCENTAGE_RECYCLE_VEHICULES, NOM_BAT : POURCENTAGE_RECYCLE_BAT, NOM_EQUIP_ELEC : POURCENTAGE_RECYCLE_EQUIP_ELEC, NOM_APP_ELEC : POURCENTAGE_RECYCLE_APP_ELEC}
dict_rendement_recyclage = {NOM_VEHICULES : RENDEMENT_RECYCLE_VEHICULES, NOM_BAT : RENDEMENT_RECYCLE_BAT, NOM_EQUIP_ELEC : RENDEMENT_RECYCLE_EQUI_ELEC, NOM_APP_ELEC : RENDEMENT_RECYCLE_APP_ELEC}

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
        plt.plot(tableau[no_donnee,:],RANGE_ANNEES) # manque un label
        plt.figure()

    plt.show()

## Accesseurs partie production (tout est initialisé avant, on peut y accéder sans pb)

# getConsoTotale

def getConsoCategorie(no_annee, categorie_conso):
    return resultats[categorie_conso, no_annee]

def getConsoTotale(no_annee):
    # return getConsoVehicules(no_annee) + getConsoBat(no_annee) + getConsoEquipElec(no_annee) + getConsoAppElec(no_annee)
    return sum([getConsoCategorie(no_annee, cat[1]) for cat in dict_categories_conso.items()])

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


def getStockCategorie(no_annee, categorie_stock):
    return resultats[categorie_stock, no_annee]

def getStock(no_annee): 
    # return getStockVehicules(no_annee) + getStockBat(no_annee) + getStockEquipElec(no_annee) + getStockAppElec(no_annee)
    return sum([getStockCategorie(no_annee, cat[1]) for cat in dict_categories_stock.items()])

## Accesseurs partie après le stock (TODO) :

'''Donne ce qui sort des stocks:
- ce qui va être recyclé (fin de vie, old-waste), somme de toutes les catégories
- ce qui va être perdu définitivement (abandonné, non-recyclé et perdu lors du recyclage)
'''
# getSortieStock
def getSortieStockCategorie(no_annee, categorie_stock):
    return resultats[categorie_stock, no_annee - dict_temps[categorie_stock]]

def getSortieStock(no_annee):
    # return getSortieStockVehicules(no_annee) + getSortieStockBat(no_annee) + getSortieStockEquipElec(no_annee) + getSortieStockAppElec(no_annee)
    return sum([getSortieStockCategorie(no_annee, cat[1]) for cat in dict_categories_stock.items()])

def getRecyclageSecondaireCategorie(no_annee,categorie):
    '''Donne ce qui va partir en recyclage secondaire, à partir de ce qui sort des stocks (facteurs d'abandon/mauvaise poubelle)'''
    return dict_portion_recyclee[categorie] * getSortieStockCategorie(no_annee, categorie)


def getObtenuRecyclageSecondaireCategorie(no_annee, categorie):
    '''Donne ce qui est obtenu lors du recyclage secondaire (rendement), et qui va donc directement repartir dans les stocks'''
    return dict_rendement_recyclage[categorie] * getRecyclageSecondaireCategorie(no_annee, categorie)


# Accesseur au tableau :
"""A mettre par categorie"""
def getRecyclageTotal(no_annee):
    '''Donne tout ce qui entre en production par le recyclage (new-waste, et old-waste toutes catégories confondues)'''
    return getRecyclagePrimaire(no_annee) + sum([getObtenuRecyclageSecondaireCategorie(no_annee, cat[1]) for cat in dict_categories_stock.items()])


def calculerStockAnneeSuivante(no_annee):
    '''Donne le stock présent sur le territoire au 1/1/N+1. Ne modifie pas le taleau
    Concrètement :
    - récupère le stock au 1/1/N
    - ajoute la consommation pendant l'année N
    - enlève ce qui est parti du stock pendant l'année N

    Retourne une colonne avec des données situées aux lignes des stocks 
    et des 0 autre part (comme ça il suffit de le sommer)

    TODO pour dispatcher selon quel type d'objet est dans le stock
    '''
    stock_prec = np.zeros( (NB_DONNEES) )

    for nom_cat in liste_categories :
        stock_prec[dict_categories_stock[nom_cat]] =  getStockCategorie(no_annee, dict_categories_stock[nom_cat])
        stock_prec[dict_categories_stock[nom_cat]] += getConsoCategorie(no_annee, dict_categories_conso[nom_cat])
        stock_prec[dict_categories_stock[nom_cat]] -= getSortieStockCategorie(no_annee, dict_categories_stock[nom_cat])


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
