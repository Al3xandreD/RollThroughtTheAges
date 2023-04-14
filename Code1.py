#   pour faire de l'héritage: trouver des méthodes ou attributs
#   en commun
# Faire base de donnée avec les scores et les stratégies

# ajouter securité sur les inputs
# ajouter option 7 decalage
# ajouter specificité developpement
# anglais/fr
# recursif ?
# checkez fin de tour, si les joueurs doivent finir de jouer ou pas

#je rajoute
import numpy as np


class Player(object):
    def __init__(self, nom):
        self.nm = nom
        self.f_point = 0  # nombre de points finaux
        self.skull = 0  # nombre de crane obtenu
        self.nb_city = 3  # nombre initial de ville
        self.max_relance = 2  # on ne peux relancer que 2 fois
        self.souhait_nb_relance = self.nb_city  # nombre de dee a relancer, doit initialement etre egale au nombre de ville

        # variable liées aux ressources
        self.wheat = Ressources("wheat", 7, 3)
        self.wood = Ressources("wood", 0, 0)
        self.pottery = Ressources("pottery", 2, 0)
        self.stone = Ressources("stone", 1, 0)
        self.cloth = Ressources("clothe", 3, 0)
        self.arrow = Ressources("arrow", 4, 0)
        self.workers = Ressources("workers", 5, 0)
        self.coins = Ressources("coins", 6, 0)
        self.plateau = [self.wheat, self.wood, self.stone, self.pottery, self.cloth, self.arrow, self.coins,
                        self.workers]
        self.gestionressource = [self.wood, self.stone, self.pottery, self.cloth, self.arrow]
        self.memoireR = 0

        # attributs liés aux developpements
        self.leadership = Developement(2, 2, 10, 1, False, "Leadership", "Relance 1 dée")  # False veut dire non acheté
        self.irrigation = Developement(2, 2, 10, 1, False, "Irrigation", "Pas touché par la sécheresse")
        self.agriculture = Developement(3, 3, 15, 1, False, "Agriculture", "+1 nourriture par dé nourriture")
        self.quarrying = Developement(3, 3, 15, 1, False, "Carrière", "+1 pierre si collecte pierre")
        self.medicine = Developement(3, 3, 15, 1, False, "Medecine", "Pas affecté par la peste")
        self.coinage = Developement(4, 3, 20, 1, False, "Finance", "+12 pieces par dé pièces")
        self.caravans = Developement(4, 3, 20, 1, False, "Caravans", "Plus besoin de defausser")
        self.religion = Developement(6, 6, 20, 1, False, "Religion", "La revolte affecte les adversaires")
        self.granaries = Developement(6, 6, 30, 1, False, "Granary", "vente d'une nouriture pour 4 pieces")
        self.masonry = Developement(6, 6, 30, 1, False, "Masonry", "+1 ouvrier par dé ouvrier")
        self.engineering = Developement(6, 6, 40, 1, False, "Engineering", "remplace 1 pierre pour 3 ouvriers")
        self.architecture = Developement(8, 6, 50, 1, False, "Architecture", "+1 point par monument")
        self.empire = Developement(8, 6, 60, 1, False, "Empire", "+1 point par cité")
        self.liste_developpement = [self.leadership, self.irrigation, self.agriculture, self.quarrying, self.medicine,
                                    self.coinage, self.caravans, self.religion, self.granaries, self.masonry,
                                    self.engineering, self.architecture, self.empire]
        self.nb_dev = 0

        # attributs liés aux cités
        self.city_sup1 = Construction(1, 1, 3, 0, False, "Roubaix")
        self.city_sup2 = Construction(1, 1, 4, 0, False, "Paris")
        self.city_sup3 = Construction(1, 1, 5, 0, False, "New-York")
        self.city_sup4 = Construction(1, 1, 6, 0, False, "Singapour")
        self.liste_cite = [self.city_sup1, self.city_sup2, self.city_sup3, self.city_sup4]

        # attributs liés aux monuments
        self.pyramide = Monument(1, 0, 3, 0, False, "Pyramide", False, False)
        self.stonehedge = Monument(2, 1, 5, 0, False, "StoneHedge", False, False)
        self.temple = Monument(4, 2, 7, 0, False, "Temple", False, False)
        self.garden = Monument(8, 4, 11, 0, False, "Garden", False, False)
        self.gpyramide = Monument(12, 6, 15, 0, False, "Great Pyramide", False, False)
        self.greatwall = Monument(10, 5, 13, 0, False, "Great Wall", False, False)
        self.obelisque = Monument(6, 3, 9, 0, False, "Obelisque", False, False)
        self.liste_monuments = [self.pyramide, self.stonehedge, self.temple, self.garden, self.gpyramide,
                                self.greatwall, self.obelisque]
        self.nb_monument = 0

    def nb_monument_accessible(self, nb_joueur):
        '''Gives acces to a certain number of monuments according to the nuber of player'''

        for monument in self.liste_monuments:
            if nb_joueur == 2 and monument.nm == ("Pyramide" or "StoneHedge" or "Obelisque" or "Great Wall"):
                monument.acces = True
                return 4
            elif nb_joueur == 3 and monument.nm == (
                    "Pyramide" or "StoneHedge" or "Obelisque" or "Great Wall" or "Temple" or "Great Pyramide"):
                monument.acces = True
                return 6
            else:
                monument.acces = True
                return 7

    def alimenter(self):
        '''Permet d'alimenter les villes'''
        self.wheat.quant -= self.nb_city

    def unTour(self):
        '''Simulates a round for the player'''
        self.tirage()  # on lance les dees
        self.alimenter()  # on alimente
        if self.wheat.quant < 0:
            self.f_point -= self.wheat  # on perd des points lorsque l'on ne peut plus alimenter les villes
            print("Vous n'avez pas nourri {} villes".format(-self.wheat.quant))
        self.desastereffect()  # on impose les desastre

        if self.workers.quant > 0:
            constru = input("Ou souhaitez vous placer vos ouvriers? cite/monument")
            while self.workers.quant > 0:
                # achat cite
                if constru == "cite":
                    nom_cite = input("quel est le nom de la cité?")
                    for construction in self.liste_cite:  # on construit si possible
                        if construction.test_construction() == True and construction.nm == nom_cite:  # on acquiert
                            self.workers.quant, self.nb_city = construction.construire(self.workers.quant, self.nb_city)
                # achat monument
                else:
                    nom_monument = input("quel est le nom du monument?")
                    for monument in self.liste_monuments:
                        if monument.test_construction() == True and monument.nm == nom_monument and monument.acces == True:  # test d'aqcuisition
                            self.workers, self.nb_monument = monument.construire(self.workers.quant,
                                                                                 self.nb_monument)  # on acquiert
                            if monument.fisrt_buy == True:  # attribution du nombre de point en fonction de l'ordre d'acquisition
                                self.f_point += monument.point_max
                            else:
                                self.f_point += monument.point_min
                                # Ajouter le bon nombre de points si la construciton est nouvelle et regarder si c'est le permier ou pas

        # achat developpement
        print('Vous avez')
        S = 0
        for ressource in self.plateau:
            S += ressource.quant
            print('{} {}'.format(ressource.quant, ressource.nm))
        print('/n soit {} ressources'.format(S))
        print('Vous avez aussi {}'.format(self.coins.quant))
        S2 = self.coins.quant
        if S + S2 > 0:
            nom_dev = input('Quel développement souhaitez vous acheter ?')
            for developp in self.liste_developpement:
                prix = developp.cost
                if developp.test_construction(S + S2, prix) and developp.nm == nom_dev:  # on acquiert
                    print('Vous utilisez vos pièces')
                    prix -= self.coins.quant
                    self.coins.quant = 0
                    print("il reste à payer {}".format(prix))
                    while prix > 0:
                        n = input('Quel ressource souhaitez vous utiliser ?')
                        for ressource in self.gestionressource:
                            if ressource.nm == n:
                                dec = self.gestionressource[ressource.ordre].decalage
                                if dec > 0:
                                    def suite(k, U1):  # fonction récursives
                                        if k == 0:
                                            return 0
                                        elif k == 1:
                                            return U1
                                        else:
                                            return U1 * k + suite(k - 1, U1)

                                    prix -= suite(dec, ressource.ordre)
                                    self.gestionressource[ressource.ordre].decalage = 0
                                else:
                                    print(" tu n'as plus de cette ressources")
                    print('Vous avez obtenu le développement {}'.format(developp.nm))
                    developp.status = True
                    self.f_point += developp.point_max  # ajout des points
                elif developp.test_construction(S) == False:
                    print(" Vous n'avez pas assez de ressources OU vous avez déjà acheté le développement")

    def gestion(self, n):
        if n == 0:
            return 'gestion(0)'
        signe = n // abs(n)
        if signe > 0:
            for i in range(n):
                self.gestionressource[i % 5].decalage += 1
            self.memoireR = n % 5 - 1
        else:
            # cette partie sert a retirer si le joueur veut relancer
            debut = self.memoireR
            print((debut, debut + n, -1))
            for u in range(debut, debut + n, -1):
                self.gestionressource[u % 5].decalage -= 1
            self.memoireR = (debut + n) % 5

        for j in range(1, 6):
            def suite(k, U1):  # fonction récursives
                if k == 0:
                    return 0
                elif k == 1:
                    return U1
                else:
                    return U1 * k + suite(k - 1, U1)

            self.gestionressource[j - 1].quant = suite(self.gestionressource[j - 1].decalage, j)

    def tirage(self):  # a tester
        '''Gives a random number to simulate a dee
        Management of the dee throw and re-throw'''

        print("Je tire")
        dee = Dee()  # création d'un dee
        list_dee = [0, 0, 0, 0, 0, 0]  # pour faire l'affichage des dees au joueur
        # autre idée: faire liste avec chacun des valeurs correspond a un dé

        self.skull = 0
        self.coins.quant = 0  # on remet l'argent à 0 avant chaque lancer
        self.workers.quant = 0  # on remet a 0 car on stock pas les travailleurs
        relance = 'OUI'
        while relance == "OUI" and self.max_relance >= 0:  # on veut relancer
            for k in range(self.souhait_nb_relance):  # 1 throw for 1 city
                dee.throw()  # on lance le dee
                list_dee[dee.res - 1] += 1
                effect = dee.correspondance()  # on donne l'effet
                print(effect)
                # permet de simuler l'état avec l'effet du dée
                if effect == "2 Marchandises et 1 Crâne":
                    self.gestion(2)
                    self.skull += 1
                elif effect == "3 Nourritures":
                    self.wheat.quant += 3
                elif effect == "1 Marchandise":
                    self.gestion(1)
                elif effect == "3 Ouvriers":
                    self.workers.quant += 3
                elif effect == "2 Nourritures ou 2 Ouvriers":
                    choice = input("Choose between 2 wheats or 2 workers")
                    if choice == "wheats":
                        WHEAT = True
                        self.wheat.quant += 2
                    else:
                        self.workers.quant += 2
                        WHEAT = False
                elif effect == "7 pièces":
                    self.coins.quant += 7

            # affichage des résultats
            print(' Vous avez eu')
            for i in range(6):
                print('{} dés {}'.format(list_dee[i], i + 1))
            print(' Ce qui vous fait ')
            for ressource in self.plateau:
                print('{} {}'.format(ressource.quant, ressource.nm))
            print('{} skulls'.format(self.skull))

            # gestion de la relance
            if self.max_relance == 0:  # on inverse pas
                print("Nombre de lancer de dés maximal atteint")
                self.max_relance = 2
                break
            relance = input("voulez-vous relancer au moins un dé: OUI/NON")

            if relance == "OUI":  # on inverse pas
                list_relance = [0, 0, 0, 0, 0, 0]
                for d in range(6):  # pour tous les dees de tirées
                    if d != 2:  # si c'est pas un crane
                        for j in range(1, list_dee[d] + 1):
                            choix = input(
                                "Voulez vous relancer le {} ème dé  avec la valeur {} OUI/NON".format(j, d + 1))
                            if choix == 'OUI':
                                list_relance[d] += 1

                for i in range(6):  # on revient a une liste de dé avec que ceux valide
                    list_dee[i] -= list_relance[i]

                # ajustement des effets ( on inverse)

                for index, val in enumerate(list_relance):
                    for j in range(val):
                        fauxdee = Dee()
                        fauxdee.res_setter = index + 1
                        effect = fauxdee.correspondance()
                        if effect == "2 Marchandises et 1 Crâne":
                            self.pottery.quant -= 2
                            # a changer
                        elif effect == "3 Nourritures":
                            self.wheat.quant -= 3
                        elif effect == "1 Marchandise":
                            self.pottery.quant -= 1
                        elif effect == "3 Ouvriers":
                            self.workers.quant -= 3
                        elif effect == "2 Nourritures ou 2 Ouvriers":
                            if WHEAT == True:
                                self.wheat.quant -= 2
                            else:
                                self.workers.quant -= 2
                        elif effect == "7 pièces":
                            self.coins.quant -= 7
                self.souhait_nb_relance = sum(list_relance)

                self.max_relance -= 1

        print("vous avez fini votre tour")
        self.max_relance = 2

    def desastereffect(self):
        '''Execute effects depending on the number of skulls'''

        if (self.skull == 0) or (self.skull == 1):
            None
        elif self.skull == 2:
            if self.irrigation.status == True:
                print('You have irrigation')
                print('No effect')

            else:
                print('You have a drought, -2 points')
                self.f_point -= 2

        elif self.skull == 3:
            if self.medicine.status == True:  # tester medecine pour chaque joueur/ si pas de medecine=> -3 points:
                print('You have medecine')
                print('No effect')
            else:
                print('Pestilence')
                self.f_point -= 3

        elif self.skull == 4:
            if self.greatwall.status == True:
                print('You have the Great Wall')
                print('No effect')
            else:
                print('You have an Invasion, -4 points')
                self.f_point -= 4

        else:  # au moins 5 têtes de morts
            if self.religion.status == True:
                print('You have religion')
                print('No effect for you ')
                # tester la religion sur chacun des joueurs et enlever des points
            else:
                print('invasion, you lost all your resources')
                self.wheat, self.stone, self.wood, self.pottery, self.cloth, self.arrow = 0, 0, 0, 0, 0, 0
            print('revolt')

    def score(self):
        '''Updates the score after a round'''


class Construction(object):  # classe mère de Monuments, Cités, Developpement
    def __init__(self, point_max, point_min, cost, cases, status, name):
        self.point_max = point_max  # point max rapportes
        self.point_min = point_min  # point min rapportes
        self.cost = cost  # valeurs necessaires pour acquerir la construction, nombre de cases,ouvrier, monnaie, ressources
        self.cases = cases  # nombre de cases cochées
        self.status = status  # status acquis ou non
        self.nm = name

    def more(self, sup_quant):
        '''Adds a supplementary quantity'''

        return self.quant + sup_quant

    def test_construction(self, res=1, prix=0):
        '''Test if a construction can be build'''

        if self.status == False and res > prix:
            return True

    def construire(self, worker, nb_monument):
        '''Ask the player if he/she wants to build a construction'''

        print("Vous avez {} ouvriers".format(worker))
        nb_ouvrier = int(input("Combien d'ouvriers souhaitez vous utiliser?"))
        while nb_ouvrier > worker or nb_ouvrier > self.cases:  # cas d'utilisateur débile
            print("impossible")
            print("Vous avez {} ouvriers".format(worker))
            print("Il reste", self.cases, "à cocher")
            nb_ouvrier = input("Combien d'ouvriers souhaitez vous utiliser?")
        self.cases += nb_ouvrier
        worker -= nb_ouvrier
        if self.cases == self.cost:
            self.status = True
            print("Felicitation vous avez acqueri {}".format(self.nm))
        return worker, nb_monument + 1


class Monument(Construction):
    def __init__(self, point_max, point_min, cost, cases, statut, name, acces, first_buy):
        super().__init__(point_max, point_min, cost, cases, statut, name)
        self.acces = acces
        self.fisrt_buy = first_buy


class Developement(Construction):
    def __init__(self, point_max, point_min, cost, cases, status, nm, effet):
        super().__init__(point_max, point_min, cost, cases, status, nm)
        self.effet = effet


class Ressources(object):
    def __init__(self, name, ordre, quant):
        self.quant = quant
        self.nm = name

    def more(self, sup_quant):
        '''Adds a supplementary quantity'''
        return self.quant + sup_quant


class Desaster(object):  # on l'appelle a la fin du tour
    def __init__(self, name, nb_skull):
        self.nm = name
        self.nb_skull = nb_skull

    @property
    def desaster_name(self):
        return self.nm


class Dee(object):
    def __init__(self):
        self.__res = 0  # resultat du tirage
        self.gain = 0
        self.effect = "rien"
        self.step = 0

    def throw(self):
        '''Gives a random number to simulate a dee'''
        self.__res = np.random.randint(1, 7)

    @property
    def res(self):
        return self.__res

    @res.setter
    def res_setter(self, resultat):
        self.__res = resultat

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
    ''' This function controls the entire game '''

    # definition des variables nécessaires
    liste_joueur = []  # liste avce les objets players dedans
    # global liste_joueur

    # trame globale

    print('Bienvenue dans le jeu Roll Through the Ages')
    nombrejoueur = int(input('combien de joueur souhaitent jouer ?'))
    print("Merci d'écrire vos pseudos")
    for i in range(nombrejoueur):
        nom = input('Joueur n°{}'.format(i + 1))
        liste_joueur.append(Player(nom))  # création des joueurs
    for joueur in liste_joueur:
        nbmonument = joueur.nb_monument_accessible(
            nombrejoueur)  # on definit le nombre de monument en fonction du nombre de joueur

    print('le jeu commence, le joueur 1 commence')
    while end(liste_joueur, nbmonument) == False:  # tant qu'il n'y a pas de fin de partie
        for j in range(nombrejoueur):
            liste_joueur[j].unTour()
    # comptage des points
    score = ['a', -100]  # (joueur gagnant, nb point)
    for j in range(nombrejoueur):
        print(liste_joueur[j].nm, liste_joueur[j].f_point, 'points')


# lancer dés
# Afficher en permanence un tableau recapitulatif de la situation
# choix relancer ou pas
# Nourrir les villes, SI pas assez de nourriture: tete de mort (=-1 points)
# SI argent et ressources : proposition choix achat developpement
# SI ouvrier : propostion construction
# SI tete de mort: compter les effets malus
# Défausser les marchandise au - dela de six
# passer au joueur suivant

def end(L, nb):
    '''this fucntion is testing if the game is over or not:
        - a player has 5 developpments
        - a player built all the momuments

        entry: list with all the player ( Player class)
        exit: Bool , True if the game is over'''
    for player in L:
        if player.nb_dev >= 5:
            print(' FIN DE LA PARTIE /n le joueur {} a 5 développments'.format(player))
            return True
        if player.nb_monument == nb:
            print(' FIN DE LA PARTIE /n le joueur {} a tous les monuments'.format(player))
            return True
    return False
    #  A FAIRE test des developpements

    #  A FAIRE test des monuments


if __name__ == '__main__':
    rollthroughtheages()
