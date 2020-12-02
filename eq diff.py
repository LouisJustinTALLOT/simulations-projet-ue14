

def f(t, x):
    '''
    Renvoie dx/dt(t)
    '''

    resultat = ...

    #Ligne d'évolution du stock de cuivre dans les maisons
    resultat[27] = - 1/(tau_fin_de_vie) * x[27] + (qté de cuivre consommée par an)

def resolv():
    ci = np.array( [..])
    t = np.linspace(...)

    y = odeint(ci, t, f)