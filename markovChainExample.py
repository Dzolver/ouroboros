import numpy as np
import random as rm

states = ["Sleep","IceCream","Run"]
transitionName = [["SS","SR","SI"],["RS","RR","RI"],["IS","IR","II"]]
transitionMatrix = [[0.2,0.6,0.2],[0.1,0.6,0.3],[0.2,0.7,0.1]]