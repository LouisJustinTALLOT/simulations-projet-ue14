import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

annees = [2016, 2015 ]
pop_france = [67751838, 67609086]


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
'''
def getConsommation(annee):
    pass

'''
Donne ce qui est perdu définitivement lors de la produciton (raffinement + semi-finished goods)
'''
def getPerduProductionTotal(annee):
    pass

'''
Donne ce qui est perdu définitivement lors de la partie raffinement de la production
'''
def getPerduProductionRaffinement(annee):
    pass

'''
Donne ce qui est perdu définitivement lors de la production des semi-finished goods
'''
def getPerduProductionSemiFinished(annee):
    pass

'''
Donne ce qui part en recyclage primaire (new waste)
'''
def getRecyclagePrimaire(annee):
    pass


'''
Donne le stock présent sur le territoire
'''
def getStock(annee):
    pass


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






'''
Donne tout ce qui entre en production par le recyclage (new-waste et old-waste)
'''
def getRecyclageTotal(annee):
    return getRecyclagePrimaire(annee) + getRecyclageSecondaire(annee)