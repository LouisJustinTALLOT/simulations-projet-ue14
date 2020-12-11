import numpy as np  
import matplotlib.pyplot as plt


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

"""
                0         1                   2                          3 
        cat = Véhicules Batiments Equipements_electroménagers Appareils_électroniques
"""
SS_0 = np.diag([0.1,     0.005,            0.1,                        0.3])
TP_0 = np.diag([...])
PR_0 = np.diag([0.9,       0.8,              0.5,                        0.2])
RR_0 = np.diag([0.95,     0.95,             0.9,                        0.5])      
CA_0 = np.diag([1,        1.02,            1.01,                        1.1])

lu = np.ones((NB_CATEGORIES))

# Trois dictionnaires pour la mémoïsation dans les fonctions récursives

dico_c = {}
dico_s = {}
dico_r = {}

# on initialise les dictionnaires

"""
                                 0         1                   2                          3 
                        cat = Véhicules Batiments Equipements_electroménagers Appareils_électroniques
"""
dico_c[ANNEE_DEBUT] = np.array([200_000, 200_000,       20_000,                     2_500               ]).reshape((-1,1))
dico_s[ANNEE_DEBUT] = np.array([1_000_000, 20_000_000,  225_000,                    10_000              ]).reshape((-1,1))
# dico_r[ANNEE_DEBUT] = np.array([...]).reshape((-1,1))

superposition = False

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
    on recycle une portion constante des 'biens' "usagés" dans toutes les catégories
    en deuxième modèle, on évolue de façon affine vers une bien meilleure portion de recyclage
    """
    if not superposition :
    if n-ANNEE_DEBUT <= 15:
        return  np.diag([0.99,0.98,0.95,0.9]) + (15-(n-ANNEE_DEBUT))/15*np.diag([-0.09,-0.18,-0.45,-0.7])
    
    return   np.diag([0.99,     0.98,             0.95,                        0.9])
    return np.diag([0.9, 0.8, 0.5, 0.2])
def RR(n):
    """en premier modèle, c'est une fonction constante : 
     dans toutes les catégories, on arrive à récupérer un taux constant de cuivre
     en deuxième modèle,on arrive à bien mieux recycler et donc perdre beaucoup moins
     """
    if not superposition :
    if n-ANNEE_DEBUT <= 25:
        return np.diag([1.,1.,1.,0.8]) + (25-(n-ANNEE_DEBUT))/25*np.diag([-0.05,-0.05,-0.1,-0.3])

    return np.diag([1.,    1.,            1.,                        0.8])      
    return np.diag([0.95, 0.95, 0.9, 0.5])

def CA(n):
    """en tout premier modèle, c'est une fonction constante : 
    nous considérons la consommation constante dans toutes les catégories
    en deuxième modèle, no considère que la consommation a des limites...
    """
    if not superposition :
    if n-ANNEE_DEBUT <= 15:
        return np.diag([1.,1.0,1.02,1.0]) + (15-(n-ANNEE_DEBUT))/15*np.diag([0,0.02,0,0.1])

    return np.diag([1.,    1.,            1.02,                       1])
    return np.diag([1., 1.02, 1.02, 1.05])

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


def simulation(annee_fin = ANNEE_FIN, sup=False):

    global superposition 
    superposition = sup

    for i in range(ANNEE_DEBUT, annee_fin+1):
        s(i); r(i)
    
    annees = np.arange(ANNEE_DEBUT, annee_fin+1)
    plt.plot(annees,np.vectorize(obtenu_recyclage)(annees), label='recyclé')
    plt.plot(annees,np.vectorize(conso_totale)(annees), label = 'consommé')
    plt.suptitle("Simulation numérique de la consommation et du recyclage annuel en cuivre")
    plt.legend()
    plt.xlabel('Temps en années')
    plt.ylabel('Tonnes de cuivre')
    plt.subplots_adjust(left=0.14, right=0.96, top = 0.92)
    plt.show()

simulation(sup=True)
