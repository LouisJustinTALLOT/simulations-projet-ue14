import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''Comment ça fonctionne ?
 - on calcule en premier lieu les consommations estimées (connu)
 - on lance la simulation :
   - on calcule au fur et à mesure les stocks, ce qui sort du stock et le recyclage de l'année suivante, 
     à l'aide notamment des données de l'année précédente
   - on ajoute au tableau les nouvelles données
   - on recommence
 - on plot les résultats joliment
'''


'''CONSTANTES'''

ANNEE_DEBUT = 2018
ANNEE_FIN = 2050
NB_ANNEES = ANNEE_FIN - (ANNEE_DEBUT - 1)  

RANGE_ANNEES = np.array([a for a in range(ANNEE_DEBUT, ANNEE_FIN+1)])

NB_LIGNES = 23
NB_CAT = 4

NOM_VEHICULES = "Vehicules"
NOM_BAT = "Batiments"
NOM_EQUIP_ELEC = "Equipements Electroniques"
NOM_APP_ELEC = "Appareils Electroniques"

#Consommation annuelle de...
LIGNE_CONSO_VEHICULES = 0
LIGNE_CONSO_BAT = 1
LIGNE_CONSO_EQUIP_ELEC = 2
LIGNE_CONSO_APP_ELEC = 3
#Stock à l'année N de...
LIGNE_STOCK_VEHICULES = 4
LIGNE_STOCK_BAT = 5
LIGNE_STOCK_EQUIP_ELEC = 6
LIGNE_STOCK_APP_ELEC = 7
#Sortie du stock à l'année N de...
LIGNE_SORTIE_STOCK_VEHICULES = 8
LIGNE_SORTIE_STOCK_BAT = 9
LIGNE_SORTIE_STOCK_EQUIP_ELEC = 10
LIGNE_SORTIE_STOCK_APP_ELEC = 11
#Ce qui va au recyclage à l'année N de...
LIGNE_GOREC_VEHICULES = 12
LIGNE_GOREC_BAT = 13
LIGNE_GOREC_EQUIP_ELEC = 14
LIGNE_GOREC_APP_ELEC = 15
#Ce que l'on gagne par recyclage à l'année N de...
LIGNE_GAINED_REC_VEHICULES = 16
LIGNE_GAINED_REC_BAT = 17
LIGNE_GAINED_REC_EQUIP_ELEC = 18
LIGNE_GAINED_REC_APP_ELEC = 19
#Partie production
LIGNE_PERDU_PROD_RAFF = 20
LIGNE_PERDU_PROD_SEMI_FINISHED = 21
LIGNE_RECYCLAGE_PRIMAIRE = 22


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

dict_lignes_conso = {NOM_VEHICULES : LIGNE_CONSO_VEHICULES,
                            NOM_BAT : LIGNE_CONSO_BAT,
                            NOM_EQUIP_ELEC : LIGNE_CONSO_EQUIP_ELEC, 
                            NOM_APP_ELEC : LIGNE_CONSO_APP_ELEC}

dict_lignes_stock = {NOM_VEHICULES : LIGNE_STOCK_VEHICULES,
                            NOM_BAT : LIGNE_STOCK_BAT,
                            NOM_EQUIP_ELEC : LIGNE_STOCK_EQUIP_ELEC, 
                            NOM_APP_ELEC : LIGNE_STOCK_APP_ELEC}

dict_lignes_sortie_stock = {NOM_VEHICULES : LIGNE_SORTIE_STOCK_VEHICULES,
                            NOM_BAT : LIGNE_SORTIE_STOCK_BAT,
                            NOM_EQUIP_ELEC : LIGNE_SORTIE_STOCK_EQUIP_ELEC, 
                            NOM_APP_ELEC : LIGNE_SORTIE_STOCK_APP_ELEC}


dict_lignes_gorec = {NOM_VEHICULES : LIGNE_GOREC_VEHICULES,
                            NOM_BAT : LIGNE_GOREC_BAT,
                            NOM_EQUIP_ELEC : LIGNE_GOREC_EQUIP_ELEC, 
                            NOM_APP_ELEC : LIGNE_GOREC_APP_ELEC}

dict_portion_recyclee = {NOM_VEHICULES : POURCENTAGE_RECYCLE_VEHICULES,
                            NOM_BAT : POURCENTAGE_RECYCLE_BAT,
                            NOM_EQUIP_ELEC : POURCENTAGE_RECYCLE_EQUIP_ELEC, 
                            NOM_APP_ELEC : POURCENTAGE_RECYCLE_APP_ELEC}

dict_lignes_gainedrec = {NOM_VEHICULES : LIGNE_GAINED_REC_VEHICULES,
                            NOM_BAT : LIGNE_GAINED_REC_BAT,
                            NOM_EQUIP_ELEC : LIGNE_GAINED_REC_EQUIP_ELEC, 
                            NOM_APP_ELEC : LIGNE_GAINED_REC_APP_ELEC}

dict_rendement_recyclage = {NOM_VEHICULES : RENDEMENT_RECYCLE_VEHICULES,
                            NOM_BAT : RENDEMENT_RECYCLE_BAT,
                            NOM_EQUIP_ELEC : RENDEMENT_RECYCLE_EQUI_ELEC,
                            NOM_APP_ELEC : RENDEMENT_RECYCLE_APP_ELEC}


dict_temps = {NOM_VEHICULES : TEMPS_VEHICULES,
                            NOM_BAT : TEMPS_BAT,
                            NOM_EQUIP_ELEC : TEMPS_EQUIP_ELEC,
                            NOM_APP_ELEC : TEMPS_APP_ELEC}

'''TABLEAU
Enregistre toutes les données, année après années.
Système d'accès au tableau :
- l'indice de colonne correspond à année courante - année de départ
- la colonne correspond à la donnée intéressante suivant le code des constantes
'''

resultats = np.zeros( (NB_LIGNES, NB_ANNEES) )

# Traçage des résultats :

def tracer_resultats(tableau):
    """Trace un tableau numpy correspondant aux résultats de la simulation"""
    plt.close()

    for no_donnee in range(NB_LIGNES):
        plt.plot(RANGE_ANNEES,tableau[no_donnee,:],'.') # manque un label
        plt.figure()

    plt.show()

## Accesseurs partie production (tout est initialisé avant, on peut y accéder sans pb)

# getConsoTotale

def getConsoCategorie(no_annee, categorie):
    return resultats[dict_lignes_conso[categorie], no_annee]

def getConsoTotale(no_annee):
    # return getConsoVehicules(no_annee) + getConsoBat(no_annee) + getConsoEquipElec(no_annee) + getConsoAppElec(no_annee)
    return sum([getConsoCategorie(no_annee, cat) for cat in liste_categories])

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


def getStockCategorie(no_annee, categorie):
    return resultats[dict_lignes_stock[categorie], no_annee]

def getStock(no_annee): 
    # return getStockVehicules(no_annee) + getStockBat(no_annee) + getStockEquipElec(no_annee) + getStockAppElec(no_annee)
    return sum([getStockCategorie(no_annee, cat) for cat in liste_categories])

## Accesseurs partie après le stock (TODO) :

'''Donne ce qui sort des stocks:
- ce qui va être recyclé (fin de vie, old-waste), somme de toutes les catégories
- ce qui va être perdu définitivement (abandonné, non-recyclé et perdu lors du recyclage)
'''
# getSortieStock
def getSortieStockCategorie(no_annee, categorie):
    try:
        return resultats[dict_lignes_stock[categorie], no_annee - dict_temps[categorie]]
    except:
        return 0.1 * resultats[dict_lignes_stock[categorie], no_annee ] # mettre une valeur typique

def getSortieStock(no_annee):
    # return getSortieStockVehicules(no_annee) + getSortieStockBat(no_annee) + getSortieStockEquipElec(no_annee) + getSortieStockAppElec(no_annee)
    return sum([getSortieStockCategorie(no_annee, cat) for cat in liste_categories])

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
    return getRecyclagePrimaire(no_annee) + sum([getObtenuRecyclageSecondaireCategorie(no_annee, cat) for cat in liste_categories])


def calculerStockAnneeSuivante(no_annee):
    '''Donne le stock présent sur le territoire au 1/1/N+1. Ne modifie pas le taleau
    Concrètement :
    - récupère le stock au 1/1/N
    - ajoute la consommation pendant l'année N
    - enlève ce qui est parti du stock pendant l'année N

    Retourne une colonne avec des données situées aux lignes des stocks 
    et des 0 autre part (comme ça il suffit de le sommer)

    Ne nécessite aucune donnée sur l'année suivante (basé uniquement sur les années no_annee et avant)
    '''
    stock_prec = np.zeros( (NB_LIGNES) )

    for cat in liste_categories :
        stock_prec[dict_lignes_stock[cat]] =  getStockCategorie(no_annee, cat)
        stock_prec[dict_lignes_stock[cat]] += getConsoCategorie(no_annee, cat)
        stock_prec[dict_lignes_stock[cat]] -= getSortieStockCategorie(no_annee, cat)


    return stock_prec


def calculerSortieStock(no_annee):
    '''Donne les données de ce qui sort du stock par catégorie de cette année. Ne modifie pas le tableau
    Concrètement:
    - donne ce qui part du stock par catégorie

    Retourne une colonne avec des données situées aux lignes correspondantes

    Ne nécessite aucune donnée sur l'année en cours (basé uniquement sur les années no_annee - 1 et avant)
    '''
    sortie_stock = np.zeros( (NB_LIGNES) )

    for cat in liste_categories:
        sortie_stock[dict_lignes_sortie_stock[cat]] = getSortieStockCategorie(no_annee, cat)

    return sortie_stock
    


def calculerRecyclage(no_annee):
    '''Donne les données du recyclage fait à l'année N. Ne modifie pas le tableau.
    Concrètement:
    - donne ce qui part au recyclage par catégorie (facteurs d'abandon)
    - donne ce qui est obtenu effectivement par recyclage, par catégorie (rendement)

    Retourne une colonne avec des données situées aux lignes correspondantes

    Nécessite les données sur ce qui sort du stock de l'année en cours
    '''

    recyclage = np.zeros( (NB_LIGNES) )

    for cat in liste_categories:
        recyclage[dict_lignes_gorec[cat]] = getRecyclageSecondaireCategorie(no_annee, cat)
        recyclage[dict_lignes_gainedrec[cat]] = getObtenuRecyclageSecondaireCategorie(no_annee, cat)

    return recyclage



# Les fonctions qui construisent l'année suivante

def doAnneeSuivante(no_annee):
    '''Calcule l'année suivante, donc ajoute à chaque ligne concernée un élément de plus
    Concrètement, on calcule les données de année_actuelle+1 à l'aide des données de année_actuelle

    Modifie le tableau !
    '''

    global resultats

    colonne_stock = calculerStockAnneeSuivante(no_annee)
    resultats[0:NB_LIGNES, no_annee]+=colonne_stock
    colonne_sortie_stock = calculerSortieStock(no_annee + 1)
    resultats[0:NB_LIGNES, no_annee]+=colonne_sortie_stock
    colonnes_recyclage_sec = calculerRecyclage(no_annee + 1)
    resultats[0:NB_LIGNES, no_annee]+=colonnes_recyclage_sec


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
