import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

N = 66000000
infectes_dep = 1000
temps = 365
beta = 0.8

b = 1 / 3
c = 0.6
d = 1 / 14
e = 0.001
f = 1 / 7
g = 0.01
h = 0.01
i = 1 / 9
j = 1 / 12
k = 1 / 180
l = 0.05

labels = ["Sains", "Incubation", "Cont. Asympt.", "Cont. Sympt.", "Rea", "Immunisés", "Dcd"]

def fonction(x, t):
    '''
         0     1     2      3      4       5       6
    x = (s(t), i(t), ca(t), cs(t), rea(t), imm(t), dead(t))
    '''

    s = x[0]
    inf = x[1]
    ca = x[2]
    cs = x[3]
    rea = x[4]
    imm = x[5]
    dead = x[6]

    resultat = np.zeros( (7,) )
    resultat[0] = - (beta * s * (  cs + ca )) / N + k * l * imm
    resultat[1] = (beta * s * ( cs + ca)) / N - b * inf
    resultat[2] = c * b * inf - d * ca
    resultat[3] = (1 - c) * b * inf - (e + h) * f * cs - (1 - e - h) * d * cs
    resultat[4] = e * f * cs  - ((1 - g) * j * rea + g * i * rea)
    resultat[5] = d * ca + (1 - e - h) * d * cs + ((1-g) * j * rea) - k*l*imm
    resultat[6] = h * f * cs + (g * i * rea)


    return np.array(resultat)




def resolution():
    ci = np.array( [N - infectes_dep, infectes_dep, 0, 0, 0, 0, 0] )
    t = np.linspace(0,temps,temps)
    y = odeint(fonction,ci,t)
    print(y.shape)
    for donnee in range(7):
        plt.plot(t, y[:,donnee], label = labels[donnee])

    rea = y[:, 4]

    for jour in range(temps):
        print("En réau au jour", jour, ": ", rea[jour])

    print("Résultats finaux:")
    for donnee in range(7):
        print(labels[donnee], " : ", y[-1,donnee])
    
    plt.legend()
    plt.show()

    


resolution()