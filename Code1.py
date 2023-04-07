#   pour faire de l'héritage: trouver des méthodes ou attributs
#   en commun
# Faire base de donnée avec les scores et les stratégies
#coucouuu
import numpy as np

class Player(object):
    def __init__(self):
        self.f_point = 0  # nombre de points finaux
        self.skull = 0  # nombre de crane obtenu
        self.nb_city = 3  # nombre initial de ville
        self.wheat = Ressources("wheat")
        self.wood=Ressources("wood")
        self.pottery = Ressources("pottery")
        self.stone=Ressources("stone")
        self.tissus=Ressources("tissus")
        self.arrow=Ressources("arrow")
        self.workers=Ressources("workers")
        self.coins = 0
        self.nb_relance=self.nb_city   # nombre de dee a relancer, doit initialement etre egale au nombre de ville

    def unTour(self):
        '''Simulates a round for the player'''

    def tirage(self):   # voir pour la rendre récursive
        '''Gives a random number to simulate a dee'''
        dee=Dee()
        #self.skull = 0
        self.coins=0    # on remet l'argent à 0 avant chaque lancer
        for k in range(self.nb_relance):    # 1 throw for 1 city
            Dee.throw() #création du dée
            effect = Dee.correspondance()   # on donne l'effet
            # appeler une fonction pour afficher le resultat au joueur
            if effect=="2 Marchandise et 1 Crâne":
                self.pottery+=2
                self.skull+=1
            elif effect=="3 Nourritures":
                self.wheat+=3
            elif effect=="1 Marchandise":
                self.pottery+=1
            elif effect=="3 Ouvriers":
                self.workers+=3
            elif effect=="2 Nourritures ou 2 Ouvriers":
                choice=input("Choose between 2 wheats or 2 workers")
                if choice=="wheats":
                    self.wheat+=2
                else:
                    self.workers+=2
            elif effect=="7 pièces":
                self.coins+=7
        self.nb_relance=input("votre nombre de dee à relancer est:",self.nb_city-self.skull,"combien de relance souhaitez vous faire")
        # dans l'implementation: appeler relance

    def relance(self):
        '''Simulate a new dice roll'''
        for k in range(self.nb_relance):
            self.tirage()


    def score(self):
        '''Updates the score after a round'''

    def choix(self):
        '''player choose what he wants to do at each step'''


class Construction(object):  # classe mère de Monuments et Cités
    def __init__(self, point_max, point_min, cost, status, name):
        self.point_max = point_max  # point max rapportes
        self.point_min = point_min  # point min rapportes
        self.cost = cost  # valeurs necessaires pour acquerir la construction, nombre de cases,ouvrier, monnaie, ressources
        self.status = status  # status acquis ou non
        self.nm = name


class Monuments(Construction):
    def __init__(self):
        super(Monuments, self).__init__()


class Cities(Construction):
    def __init__(self, food):
        super(Cities, self).__init__()
        self.food = food


class Developement(Construction):
    def __init__(self, effet):
        super(Developement, self).__init__()
        self.effet = effet
        self.leadership=False # False veut dire non acheté
        self.irrigation=False
        self.agriculture=False
        self.quarrying=False
        self.medicine=False
        self.coinage=False
        self.caravans=False
        self.religion=False
        self.granaries=False
        self.masonry=False
        self.engineering= False
        self.empire = False


class Ressources(list):
    def __init__(self, name):
        self.quant = 0
        self.nm = name

    def more(self, sup_quant):
        '''Adds a supplementary quantity'''
        return self.quant + sup_quant


class Desaster(object): # on l'appelle a la fin du tour
    def __init__(self):

     def desastereffect(self, number):
        '''Execute effects depending on the number of skulls'''

        if (number == 0) or (number == 1):
            print('No effect')

        elif number == 2:
            #checher si il a le developpement
            print('drought')


        elif number == 3:
            print('Pestilence')

        elif number == 4:
            print('invasion')

        else: # au moins 4 têtes de morts
            print('revolt')






class Dee(object):
    def __init__(self):
        self.__res = 0  # resultat du tirage
        self.gain = 0
        self.effect = "rien"
        self.step = 0

    def throw(self):
        '''Gives a random number to simulate a dee'''
        return np.random.randint(1,7)

    @property
    def res(self):
        return self.__res

    def correspondance(self):
        '''Allows to make the link between the dee's result and its effect '''
        if self.res == 1:
            self.effect = "3 Nourritures"
        if self.res == 2:
            self.effect = "1 Marchandise"
        if self.res == 3:
            self.effect = "2 Marchandise et 1 Crâne"
        if self.res == 4:
            self.effect = "3 Ouvriers"
        if self.res == 5:
            self.effect = "2 Nourritures ou 2 Ouvriers"
        if self.res == 6:
            self.effect = "7 pièces"
        return self.effect

def rollthroughtheages():
    #demander nombre de joueur et pseudos
    #creation plateau de jeux par joueur
    #Joueur 1 commence
    # While PAS DE GAGNANT:

        #lancer dés
        # Afficher en permanence un tableau recapitulatif de la situation
        #choix relancer ou pas
        # Nourrir les villes, SI pas assez de nourriture: tete de mort (=-1 points)
        # SI argent et ressources : proposition choix achat developpement
        # SI ouvrier : propostion construction
        # SI tete de mort: compter les effets malus
        # Défausser les marchandise au - dela de six
        # passer au joueur suivant


