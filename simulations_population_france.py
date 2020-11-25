import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


'''
LISTES
'''
consommations = []


'''
CONSTANTES
'''
POURCENTAGE_PERDU_DEF_RAFFINEMENT_RAPP_CONSO = 1.75
POURCENTAGE_PERDU_DEF_SEMI_FINISHED_RAPP_CONSO = 1.09
POURCENTAGE_NEW_WASTE_RAPP_CONSO = 16.4



'''
Initialise la liste des consommations annuelles
A faire au départ !
TODO
'''
def initListeConso():
    pass




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
    pass

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
Donne le stock présent sur le territoire
TODO
'''
def getStock(annee):
    pass


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