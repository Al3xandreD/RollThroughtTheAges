# Faire base de donnée avec les scores et les stratégies

# simplification de fou avec l'amelioration qeustion, a ajouter
# ligne 144
#FIN


import numpy as np
import time
from prettytable import PrettyTable
import bdd_projetinfo as bdd
import datetime


class Player(object):
    def __init__(self, nom,iD=0,matchP=0,matchW=0):
        self.nm = nom
        self.point=[0,0,0,0,0]# detail des points: developpment,monument,desastre,ville non nourrie,ville ( cas ingénieur)
        self.f_point = sum(self.point)  # nombre de points finaux
        self.skull = 0  # nombre de crane obtenu
        self.nb_city = 3  # nombre initial de ville
        self.max_relance = 2  # on ne peux relancer que 2 fois
        self.souhait_nb_relance = self.nb_city  # nombre de dee a relancer, doit initialement etre egale au nombre de ville

        # variable liées aux ressources
        self.food = Ressources("food", 7, 3)
        self.wood = Ressources("wood", 0, 0)
        self.pottery = Ressources("pottery", 2, 0)
        self.stone = Ressources("stone", 1, 0)
        self.cloth = Ressources("cloth", 3, 0)
        self.arrow = Ressources("arrow", 4, 0)
        self.workers = Ressources("workers", 5, 0)
        self.coins = Ressources("coins", 6, 0)
        self.plateau = [self.food, self.wood, self.stone, self.pottery, self.cloth, self.arrow, self.coins,
                        self.workers]
        self.gestionressource = [self.wood, self.stone, self.pottery, self.cloth, self.arrow]
        self.liste_nm_ressource = [ressource.nm for ressource in self.gestionressource]
        self.memoireR = 0

        # attributs liés aux developpements
        self.leadership = Developement(2, 2, 10, 1, False, "Leadership", "Re-roll one die")  # False veut dire non acheté
        self.irrigation = Developement(2, 2, 10, 1, False, "Irrigation", "Drought has no effect")
        self.agriculture = Developement(3, 3, 15, 1, False, "Agriculture", "+1 Food with a Food die")
        self.quarrying = Developement(3, 3, 15, 1, False, "Carrière", "+1 Stone when producing Stone")
        self.medicine = Developement(3, 3, 15, 1, False, "Medecine", "Pestilence has no effect")
        self.coinage = Developement(4, 3, 20, 1, False, "Finance", "1 Money Die = 12 Coins")
        self.caravans = Developement(4, 3, 20, 1, False, "Caravans", "No goods limit")
        self.religion = Developement(6, 6, 20, 1, False, "Religion", "Revolt effects opponents")
        self.granaries = Developement(6, 6, 30, 1, False, "Granary", "Change Food to 4 coins")
        self.masonry = Developement(6, 6, 30, 1, False, "Masonry", "+1 Worker with a Worker Die")
        self.engineering = Developement(6, 6, 40, 1, False, "Engineering", "Change Stone to 3 Workers")
        self.architecture = Developement(8, 6, 50, 1, False, "Architecture", "1 additional point for every monument")
        self.empire = Developement(8, 6, 60, 1, False, "Empire", "1 additional point for every city")
        self.liste_developpement = [self.leadership, self.irrigation, self.agriculture, self.quarrying, self.medicine,
                                    self.coinage, self.caravans, self.religion, self.granaries, self.masonry,
                                    self.engineering, self.architecture, self.empire]
        self.liste_nm_dev = [dev.nm for dev in self.liste_developpement]
        self.nb_dev = 0
        self.farchit = False # pour ajuster les points au moment ou il achete architecte
        self.femp = False # pour ajuster les points au moment ou il achete architecte

        # attributs liés aux cités
        self.city_sup1 = Construction(1, 1, 3, 0, False, "Roubaix")
        self.city_sup2 = Construction(1, 1, 4, 0, False, "Paris")
        self.city_sup3 = Construction(1, 1, 5, 0, False, "New-York")
        self.city_sup4 = Construction(1, 1, 6, 0, False, "Singapour")
        self.liste_cite = [self.city_sup1, self.city_sup2, self.city_sup3, self.city_sup4]
        self.liste_nm_cite = [cite.nm for cite in self.liste_cite]  # liste des noms

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
        self.liste_nm_monument = [monument.nm for monument in self.liste_monuments]  # liste des noms
        self.nb_monument = 0

        # Données mémorisées pour la base de donnée et le compte rendu sous forme de fichier
        self.table=PrettyTable()
        self.ftour=0

        # attributs liés à la BDD
        self.iD = iD  # numero du joueur dans la BDD
        self.matchP = matchP  # nombre de parties jouées
        self.matchW = matchW  # nombre de parties gagnées


    def nb_monument_accessible(self, nb_joueur):
        '''Gives acces to a certain number of monuments according to the nuber of player'''
        att=7
        for k in range(len(self.liste_monuments)):
            if nb_joueur == 2 and (self.liste_monuments[k].nm in ("Pyramide", "StoneHedge","Obelisque","Great Wall")):
                self.liste_monuments[k].acces_setter = True
                att=4
            elif nb_joueur == 3 and (self.liste_monuments[k].nm in (
                    "Pyramide","StoneHedge","Obelisque","Great Wall","Temple","Great Pyramide")):
                self.liste_monuments[k].acces_setter = True
                att=6
            elif nb_joueur>3 :
                self.liste_monuments[k].acces_setter = True
                att = 7
            else:
                self.liste_monuments[k].acces_setter = False
        return att

    def alimenter(self):
        '''Permet d'alimenter les villes'''
        self.food.quant -= self.nb_city

    def unTour(self):
        '''Simulates a round for the player'''

        ## Affichage etat du joueur
        print("\033[7m\033[4m\033[35m{}\033[0m".format(self.nm))
        print(' ')
        # definition affichage
        resources1 = []
        quantities1 = []
        self.ftour+=1
        for res in self.gestionressource:
            if res.quant > 0:
                resources1.append(res.nm)
                quantities1.append(res.quant)
        developments1 = [str(d) for d in self.liste_developpement if d.status == True]
        monuments1 = [str(d) for d in self.liste_monuments if d.status == True]
        cities1 = [str(d) for d in self.liste_cite if d.status == True]
        points1 = [str(self.f_point)]
        food1 = [str(self.food.quant)]

        # ajustement taille affichage
        taillemax = max(len(resources1), len(quantities1), len(developments1), len(monuments1), len(cities1),
                        len(points1))
        developments = developments1 + [' ' for i in range(taillemax - len(developments1))]
        monuments = monuments1 + [' ' for i in range(taillemax - len(monuments1))]
        cities = cities1 + [' ' for i in range(taillemax - len(cities1))]
        points = points1 + [' ' for i in range(taillemax - len(points1))]
        food = food1 + [' ' for i in range(taillemax - len(food1))]
        resources = resources1 + [' ' for i in range(taillemax - len(resources1))]
        quantities = quantities1 + [' ' for i in range(taillemax - len(quantities1))]

        print("\033[35m{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}\033[0m".format('resources', 'quantity', 'developments',
                                                                                'monuments',
                                                                                'cities', 'food', 'points'))
        print(
            "\033[35m---------------------------------------------------------------------------------------------------------\033[0m")

        for i in range(taillemax):
            print("\033[35m{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}\033[0m".format(resources[i], quantities[i],
                                                                                    developments[i],
                                                                                    monuments[i], cities[i],food[i],points[i]))
        ## FIN Affichage etat du joueur
        time.sleep(1)

        self.tirage()  # on lance les dees
        time.sleep(1)
        self.alimenter()  # on alimente
        if self.food.quant < 0:
            self.point[3] += self.food.quant  # on PERD des points lorsque l'on ne peut plus alimenter les villes, attention c'est negatif
            print(' ')
            print("\033[31m" + "You have not fed {} cities, you loose {} points".format(-self.food.quant,
                                                                                        -self.food.quant) + "\033[0m")
            self.food.quant = 0  # modifier avec le getter?
        self.desastereffect()  # on impose les desastre
        # dans le cas d'un ingénieur:
        if self.engineering.status==True and self.stone.quant>0:
            r = question('str',' BUT You have \033[33mengineering\033[0m, do you want to exchange 1 stone for 3 workers? yes/no',
                         ['yes', 'no'])
            if r=='yes':
                self.workers.quant+=3
                self.stone.decalage-=1
                self.stone.quant=suite(self.stone.decalage,2)
        if self.workers.quant > 0:
            while self.workers.quant > 0:
                print(' ')
                constru = question('str',"\033[3mWhere do you want to place your  {} workers? city/monument\033[0m".format(self.workers.quant),["city", "monument"])
                # achat cite
                if constru == "city":
                    print(' ')
                    print('You can build')
                    print(' ')
                    for cite in self.liste_cite:  # affichage des noms
                        if cite.status == False:
                            print('{:<15}   {:<2} workers remaining'.format(cite.nm, cite.cost - cite.cases))
                    print(' ')
                    nom_cite = question('str', "\033[3m" + "What is the name of the city?" + "\033[0m",
                                        [i for i in self.liste_nm_cite])
                    for construction in self.liste_cite:  # on construit si possible
                        if construction.test_construction() == True and construction.nm == nom_cite:  # on acquiert
                            self.workers.quant, self.nb_city, bool = construction.construire(self.workers.quant, self.nb_city)
                            if self.empire.status == True and bool==True: # bool= est ce que l'achat a été fait?
                                self.point[4]+=1



                # achat monument
                else:
                    for monument in self.liste_monuments:  # affichage des noms
                        if monument.status == False and monument.acces == True:
                            print(
                                '{:<15}   {:<2} workers remaining'.format(monument.nm, monument.cost - monument.cases))
                    nom_monument = question('str', "\033[3m" + "What is the name of the monument?" + "\033[3m",
                                            [i for i in self.liste_nm_monument])
                    for monument in self.liste_monuments:
                        if monument.test_construction() == True and monument.nm == nom_monument:  # test d'aqcuisition
                            self.workers.quant, self.nb_monument,bool = monument.construire(self.workers.quant,
                                                                                       self.nb_monument)  # on acquiert
                            for joueur in liste_joueur:  # on cherche à savoir s'il s'agit de l'acquereur primaire
                                # retirer le joueur actuel du test
                                if joueur.nm != self.nm and bool==True:
                                    monument.first_buy = True
                                    for monument_bis in joueur.liste_monuments:
                                        if monument_bis.fisrt_buy == True:
                                            monument.first_buy = False

                                    if monument.first_buy == True:  # attribution du nombre de point en fonction de l'ordre d'acquisition
                                        if self.architecture.status==True:
                                            self.point[1] += (monument.point_max+1)
                                        else:
                                            self.point[1] += monument.point_max
                                    else:
                                        if self.architecture.status==True:
                                            self.point[1] += (monument.point_min+1)
                                        else:
                                            self.point[1] += monument.point_min
        # achat developpement
        time.sleep(1)
        print('You have')
        print(' ')
        S = 0
        for res in self.gestionressource:
            if res.quant > 0:
                S += res.quant
        print("------------------------------------------------------------------------------------")
        print("{:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format('wood', 'stone', 'pottery', 'cloth', 'arrow', 'coins', 'food'))
        print("{:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format(self.wood.quant, self.stone.quant, self.pottery.quant,
                                                                 self.cloth.quant, self.arrow.quant, self.coins.quant,self.food.quant))
        print("------------------------------------------------------------------------------------")

        # developpment grenier
        if self.granaries.status==True and self.food.quant>0:
            r = question('str', ' BUT You have \033[33mgranaries\033[0m, do you want to sell 1 food for 4 coins? yes/no',['yes', 'no'])
            if r=='yes':
                self.food.quant-=1
                self.coins.quant+=4
                # on affiche de nouveau
                print("------------------------------------------------------------------------------------")
                print("{:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format('wood', 'stone', 'pottery', 'cloth', 'arrow',
                                                                         'coins', 'food'))
                print("{:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12}".format(self.wood.quant, self.stone.quant,
                                                                         self.pottery.quant,
                                                                         self.cloth.quant, self.arrow.quant,
                                                                         self.coins.quant, self.food.quant))
                print("------------------------------------------------------------------------------------")

        S2 = self.coins.quant
        if S + S2 > 0:
            achat_dev = question('str', "\033[3m" + "Do you want to buy a development? yes/no" + "\033[0m",
                                 ['yes', 'no'])
            if achat_dev == "yes":
                no = 0  # compter le nombre de dev achetable
                print(' ')
                print("{:<12} {:<12} {:<12} {:<60}".format('name','point', 'cost', 'effect'))
                print('------------------------------------------------------------------------------------')
                for dev in self.liste_developpement:
                    if dev.status == False and dev.cost <= S + S2:
                        print("{:<12} {:<12} {:<12} \033[3m\033[33m{:<60}\033[0m".format(dev.nm,dev.point_max,dev.cost,"\033[3m"+dev.effet+"\033[0m"))
                        no += 1
                if no == 0:
                    print("\033[33m Sorry you can't buy any development\033[0m")
                else:
                    nom_dev = question('str', "\033[3m" + 'Which development do you want to buy ?' + "\033[0m",
                                       [i for i in self.liste_nm_dev])
                    for developp in self.liste_developpement:
                        prix = developp.cost
                        if developp.test_construction(S + S2, prix) and developp.nm == nom_dev:  # on acquiert
                            print('You are using your coins')
                            prix -= self.coins.quant
                            self.coins.quant = 0
                            while prix > 0:
                                print(' ')
                                print("\033[33mThere is still an amount to pay {} resources\033[0m".format(prix))
                                Lnom2=[]
                                print('')
                                print('{:<12} {:<12} '.format('resource', 'quantity'))
                                for i in self.gestionressource:
                                    if i.decalage > 0:
                                        Lnom2.append(i.nm)
                                        print('{:<12} {:<12} '.format(i.nm, i.quant))

                                n = question('str', "\033[3mWhich resource do you want to use?\033[0m",
                                             [i for i in self.liste_nm_ressource])
                                for ressource in self.gestionressource:
                                    if ressource.nm == n:
                                        dec = self.gestionressource[ressource.ordre].decalage
                                        if dec > 0:
                                            prix -= self.gestionressource[ressource.ordre].quant
                                            self.gestionressource[ressource.ordre].decalage = 0
                                            self.gestionressource[ressource.ordre].quant=0
                                        else:
                                            print("You no longer have that resource")
                            print("\033[34mYou have obtained the development {}\033[0m".format(developp.nm))
                            # Ajustement des points s'il vient d'acheter Architecture
                            developp.status = True
                            self.nb_dev+=1
                            if self.architecture.status == True and self.farchit == False:
                                self.farchit = True
                                self.point[1] += self.nb_monument
                            # Ajustement des points s'il vient d'acheter Empire
                            if self.empire.status == True and self.femp == False:
                                self.femp = True
                                self.point[4] += self.nb_city
                            self.point[0] += developp.point_max  # ajout des points
                        elif developp.test_construction(S) == False:
                            print("You do not have enough resources OR you have already purchased the development")
        # PARTIE DE TEST POUR NE PAS DEPASSER 7 DECALAGES DE RESSOURCES
        sommedec = 0
        for j in range(1, 6):
            sommedec += self.gestionressource[j - 1].decalage
        while sommedec > 6 and self.caravans.status == False:  # Si decalage et pas la carvane
            sommedec = 0
            for j in range(1, 6):
                sommedec += self.gestionressource[j - 1].decalage
            print('')
            print("\033[33m"'You have too many resources' + "\033[0m")
            print('')
            Lnom = []
            print('{:<12} {:<12} '.format('resource', 'quantity'))
            for i in self.gestionressource:
                if i.decalage > 0:
                    Lnom.append(i.nm)
                    print('{:<12} {:<12} '.format(i.nm, i.quant))
            print('')
            a = question('str', ' Which one do you want to throw away?', Lnom)
            if a=='wood':
                self.wood.decalage-=1
                self.wood.quant=suite(self.wood.decalage,1)
            elif a=='stone':
                self.stone.decalage-=1
                self.stone.quant = suite(self.stone.decalage, 2)
            elif a=='pottery':
                self.pottery.decalage-=1
                self.pottery.quant = suite(self.pottery.decalage, 3)
            elif a=='cloth':
                self.cloth.decalage-=1
                self.cloth.quant = suite(self.cloth.decalage, 4)
            else :
                self.arrow.decalage-=1
                self.arrow.quant = suite(self.arrow.decalage, 5)


        print('')
        print("\033[91m" + "\033[1m" + 'NEXT PLAYER' + "\033[0m")
        print('')
        self.f_point=sum(self.point)

        # Gestion de la sauvgarde dans le fichier
        creer_compte_rendu_joueur(False, self.table, 'Compte rendu {}'.format(self.nm), self.ftour, self.f_point,
                                  self.food.quant, self.wood.quant, self.stone.quant, self.pottery.quant,
                                  self.cloth.quant, self.arrow.quant,
                                  self.skull, self.workers.quant, self.coins.quant,
                                  [i.nm[0:3] for i in self.liste_monuments if i.status == True],
                                  [i.nm[0:3] for i in self.liste_developpement if i.status == True],
                                  [i.nm[0:3] for i in self.liste_cite if i.status == True])

    def gestion(self, n):  # n est le nombre d'incrémentation pyramidale
        if n == 0:
            return 'gestion(0)'
        signe = n // abs(n)
        #Mise a jour des décalage
        if signe > 0:
            debut=self.memoireR # endroit ou il faut bouger ( dernier mv +1)
            for i in range(debut, debut+n):
                if (self.quarrying.status == True) and (i % 5 == 1):  # si on a la carrière et qu'on augmente la pierre
                    self.gestionressource[i % 5].decalage += 2
                else:
                    self.gestionressource[i % 5].decalage += 1
            self.memoireR= (n+self.memoireR)%5
        else:
            # cette partie sert a retirer si le joueur veut relancer
            debut = (self.memoireR-1)%5# endroit ou il faut commencer
            for u in range(debut, debut + n, -1): # attention n est negatif
                if (self.quarrying.status == True) and (u % 5 == 1):  # si on a la carrière et qu'on augmente la pierre
                    self.gestionressource[u % 5].decalage -= 2
                else:
                    self.gestionressource[u % 5].decalage -= 1
            self.memoireR = (debut + n) % 5
        #Mise a jour des quantité
        for j in range(1, 6):
            self.gestionressource[j - 1].quant = suite(self.gestionressource[j - 1].decalage, j)

        print(self.wood.quant, self.wood.decalage)
        print(self.stone.quant, self.stone.decalage)

    def tirage(self):  # a tester
        '''Gives a random number to simulate a die
        Management of the die throw and re-throw'''

        dee = Dee()  # création d'un dee
        list_dee = [0, 0, 0, 0, 0, 0]  # pour faire l'affichage des dees au joueur
        # autre idée: faire liste avec chacun des valeurs correspond a un dé

        self.skull = 0
        self.coins.quant = 0 # on remet l'argent à 0 avant chaque lancer
        self.workers.quant = 0  # on remet a 0 car on stock pas les travailleurs
        relance = 'yes'
        nbskullpert = 0  # si il a que des cranes, on ne redemande pas de retirer

        self.souhait_nb_relance = self.nb_city
        nbde = self.souhait_nb_relance
        self.max_relance = 2
        self.memoireR=0
        while relance == "yes" and self.max_relance >= 0:  # on veut relancer
            print(' ')
            print("You are throwing dice")
            print(' ')
            for k in range(self.souhait_nb_relance):  # 1 throw for 1 city
                dee.throw()  # on lance le dee
                list_dee[dee.res - 1] += 1
                effect = dee.correspondance()  # on donne l'effet
                print("\033[34m" + "{}".format(effect) + "\033[0m")  # affichage résultat
                # permet de simuler l'état avec l'effet du dée
                if effect == "2 Goods and 1 Skull	":
                    self.gestion(2)
                    self.skull += 1
                    nbskullpert += 1
                elif effect == "3 Food":
                    if self.agriculture.status == True:
                        self.food.quant += 4
                    else:
                        self.food.quant += 3
                elif effect == "1 Good":
                    self.gestion(1)
                elif effect == "3 Workers":
                    if self.masonry.status == True:
                        self.workers.quant += 4
                    else:
                        self.workers.quant += 3
                elif effect == "2 Food or 2 Workers":
                    choice = question('str', "Choose between 2 food or 2 workers: food/workers", ['workers', 'food'])
                    if choice == "food":
                        FOOD = True
                        if self.agriculture.status == True:
                            self.food.quant += 3
                        else:
                            self.food.quant += 2
                    else:
                        if self.masonry.status == True:
                            self.workers.quant += 3
                        else:
                            self.workers.quant += 2
                        FOOD = False
                elif effect == "7 Coins":
                    if self.coinage.status == True:
                        self.coins.quant += 12
                    else:
                        self.coins.quant += 7
                time.sleep(1.2)
            # affichage des résultats
            print('In total you got')
            print(' ')

            effects = []
            for i in range(6):
                temp1 = Dee()
                temp1.res_setter = i + 1
                effects.append(temp1.correspondance())
            skulll = [self.skull, ' ', ' ', ' ', ' ', ' ']  # affichage
            coinss = [self.coins.quant, ' ', ' ', ' ', ' ', ' ']  # affichage
            maxrell = [self.max_relance, ' ', ' ', ' ', ' ', ' ']  # affichage
            wworker = [self.workers.quant, ' ', ' ', ' ', ' ', ' ']  # affichage
            print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<20}".format('effects', 'die', 'resources',
                                                                                   'quantity',
                                                                                   'skulls', 'coins', 'workers',
                                                                                   'number of throw remaining'))
            print(
                "------------------------------------------------------------------------------------------------------------------------")

            for i in range(6):
                print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<20}".format(effects[i], list_dee[i],
                                                                                       self.plateau[i].nm,
                                                                                       self.plateau[i].quant, skulll[i],
                                                                                       coinss[i], wworker[i],
                                                                                       maxrell[i]))

            print(
                "------------------------------------------------------------------------------------------------------------------------")

            # gestion de la relance
            if self.max_relance == 0:  # on inverse pas
                print("\033[31mMaximum number of dice rolls reached\033[0m")
                self.max_relance = 2
                break
            print('')
            if nbskullpert == nbde:  # si il a eu que des cranes
                break
            relance = question('str', "Do you want to roll at least one die again: yes/no", ['yes', 'no'])
            if relance == "yes":  # on inverse pas
                list_relance = [0, 0, 0, 0, 0, 0]
                for d in range(6):  # pour tous les dees de tirées
                    if d != 2:  # si c est pas un crane
                        for j in range(1, list_dee[d] + 1):
                            temp = Dee()
                            temp.res_setter = d + 1
                            temp.correspondance()
                            choix = question('str', "Do you want to reroll the {}-th die with a value of \033[34m{}\033[0m? yes/no".format(j, temp.effect), ['yes', 'no'])
                            if choix == 'yes':
                                list_relance[d] += 1

                for i in range(6):  # on revient a une liste de dé avec que ceux valide
                    list_dee[i] -= list_relance[i]

                # ajustement des effets ( on inverse)

                for index, val in enumerate(list_relance):
                    for j in range(val):
                        fauxdee = Dee()
                        fauxdee.res_setter = index + 1
                        effect = fauxdee.correspondance()
                        if effect == "3 Food":
                            if self.agriculture.status == True:
                                self.food.quant -= 4
                            else:
                                self.food.quant -= 3
                        elif effect == "1 Good":
                            self.gestion(-1)
                        elif effect == "3 Workers":
                            if self.masonry.status == True:
                                self.workers.quant -= 4
                            else:
                                self.workers.quant -= 3
                        elif effect == "2 Food or 2 Workers":
                            if FOOD == True:
                                if self.agriculture.status == True:
                                    self.food.quant -= 3
                                else:
                                    self.food.quant -= 2
                            else:
                                if self.masonry.status == True:
                                    self.workers.quant -= 3
                                else:
                                    self.workers.quant -= 2
                        elif effect == "7 Coins":
                            if self.coinage.status == True:
                                self.coins.quant -= 12
                            else:
                                self.coins.quant -= 7
                self.souhait_nb_relance = sum(list_relance)

                self.max_relance -= 1
        if self.leadership.status == True:
            r = question('str', ' BUT You have \033[33mleadership\033[0m, do you want to play a last die? yes/no', ['yes', 'no'])
            if r == 'yes':
                list_relance = [0, 0, 0, 0, 0, 0]
                for d in range(6):  # pour tous les dees de tirées
                    for j in range(1, list_dee[d] + 1):
                        temp = Dee()
                        temp.res_setter = d + 1
                        temp.correspondance()
                        choix = question('str',
                                         "Do you want to reroll the {}-th die with a value of \033[34m{}\033[0m? yes/no".format(
                                             j, temp.effect), ['yes', 'no'])
                        if choix == 'yes':
                            list_relance[d] += 1
                            break  # on ne relance qu'un seul dé
                for i in range(6):  # on revient a une liste de dé avec que ceux valide
                    list_dee[i] -= list_relance[i]

                # ajustement des effets ( on inverse)

                for index, val in enumerate(list_relance):
                    for j in range(val):
                        fauxdee = Dee()
                        fauxdee.res_setter = index + 1
                        effect = fauxdee.correspondance()
                        if effect == "3 Food":
                            if self.agriculture.status == True:
                                self.food.quant -= 4
                            else:
                                self.food.quant -= 3
                        elif effect == "1 Good":
                            self.gestion(-1)
                        elif effect == "3 Workers":
                            if self.masonry.status == True:
                                self.workers.quant -= 4
                            else:
                                self.workers.quant -= 3
                        elif effect == "2 Food or 2 Workers":
                            if FOOD == True:
                                if self.agriculture.status == True:
                                    self.food.quant -= 3
                                else:
                                    self.food.quant -= 2
                            else:
                                if self.masonry.status == True:
                                    self.workers.quant -= 3
                                else:
                                    self.workers.quant -= 2
                        elif effect == "7 Coins":
                            self.coins.quant -= 7

                dee.throw()  # on lance le dee
                list_dee[dee.res - 1] += 1
                effect = dee.correspondance()  # on donne l'effet
                print("\033[34m" + "{}".format(effect) + "\033[0m")
                # permet de simuler l'état avec l'effet du dée
                if effect == "2 Goods and 1 Skull	":
                    self.gestion(2)
                    self.skull += 1
                elif effect == "3 Food":
                    if self.agriculture.status == True:
                        self.food.quant += 4
                    else:
                        self.food.quant += 3
                elif effect == "1 Good":
                    self.gestion(1)
                elif effect == "3 Workers":
                    if self.masonry.status == True:
                        self.workers.quant += 4
                    else:
                        self.workers.quant += 3
                elif effect == "2 Food or 2 Workers":
                    choice = question('str', "Choose between 2 food or 2 workers: food/workers", ['workers', 'food'])
                    if choice == "food":
                        FOOD = True
                        if self.agriculture.status == True:
                            self.food.quant += 3
                        else:
                            self.food.quant += 2
                    else:
                        if self.masonry.status == True:
                            self.workers.quant += 3
                        else:
                            self.workers.quant += 2
                        FOOD = False
                elif effect == "7 Coins":
                    self.coins.quant += 7

    def desastereffect(self):
        '''Execute effects depending on the number of skulls'''

        print('')
        print('You have {} skulls'.format(self.skull))
        if self.skull == 2:
            if self.irrigation.status == True:
                print('\033[32mYou have irrigation, you are protected\033[0m')
            else:
                print('\033[35mYou have a drought, -2 points\033[0m')
                self.point[2]-= 2

        elif self.skull == 3:  # tester medecine pour chaque joueur/ si pas de medecine=> -3 points:
            for joueur in liste_joueur:
                if joueur.medicine.status == False and joueur.nm != self.nm:
                    print("\033[35mjoueur {} doesn't have medicine: -3 points\033[0m".format(joueur.nm))
                    self.point[2]-= 3
        elif self.skull == 4:
            if self.greatwall.status == True:
                print('\033[32mYou have the Great Wall, your are protected\033[0m')
            else:
                print('\033[35mYou have an Invasion, -4 points\033[0m')
                self.point[2] -= 4

        elif self.skull == 4:  # au moins 5 têtes de morts
            if self.religion.status == True:
                print('\033[32mYou have religion, you are protected, let see the other\033[0m')
                for joueur in liste_joueur:  # tester la religion sur chacun des joueurs et enlever des points
                    if joueur.medicine.status == True and joueur.nm != self.nm:
                        print("\033[35mjoueur {} doesn't have religion: HE LOSES EVERYTHING !\033[0m".format(joueur.nm))
                        (joueur.wood.quant, joueur.stone.quant, joueur.pottery.quant, joueur.cloth.quant,
                         joueur.arrow.quant) = (0, 0, 0, 0, 0)
            else:
                print('\033[35minvasion, HE LOSES EVERYTHING\033[0m')
                self.food.quant, self.stone.quant, self.wood.quant, self.pottery.quant, self.cloth.quant, self.arrow.quant = 0, 0, 0, 0, 0, 0
        else:
            print('\033[32mno effect\033[0m')


class Construction(object):  # classe mère de Monuments, Cités, Developpement
    def __init__(self, point_max, point_min, cost, cases, status, name):
        self.point_max = point_max  # point max rapportes
        self.point_min = point_min  # point min rapportes
        self.cost = cost  # valeurs necessaires pour acquerir la construction, nombre de cases,ouvrier, monnaie, ressources
        self.cases = cases  # nombre de cases cochées
        self.status = status  # status acquis ou non
        self.nm = name

    def __str__(self):
        return self.nm

    def test_construction(self, res=1, prix=0):
        '''Test if a construction can be build'''

        if self.status == False and res > prix:
            return True

    def construire(self, worker, nb_monument):
        '''Ask the player if he/she wants to build a construction'''

        print("You have {} workers".format(worker))
        nb_ouvrier = question('int', "How many workers do you want to use?", [i for i in range(20)])
        bool=False # savoir si ya eu un achat
        while nb_ouvrier > worker:  # test d'erreur
            print("\033[33mimpossible\033[0m")
            print("You have {} workers".format(worker))
            nb_ouvrier = question('int', "How many workers do you want to use?", [i for i in range(10)])
            print(' ')
        self.cases += nb_ouvrier
        worker -= nb_ouvrier
        if self.cases >= self.cost:
            worker += (self.cases - self.cost)
            self.cases == self.cost
            self.status = True
            print("\033[32mCongratulations, you have acquired {}\033[0m".format(self.nm))
            nb_monument = nb_monument + 1
            bool=True
        return worker, nb_monument, bool

    def __str__(self):
        return self.nm


class Monument(Construction):
    def __init__(self, point_max, point_min, cost, cases, statut, name, acces, first_buy):
        super().__init__(point_max, point_min, cost, cases, statut, name)
        self.__acces = acces
        self.fisrt_buy = first_buy

    @property
    def acces(self):
        return self.__acces

    @acces.setter
    def acces_setter(self, bool):
        self.__acces = bool


class Developement(Construction):
    def __init__(self, point_max, point_min, cost, cases, status, nm, effet):
        super().__init__(point_max, point_min, cost, cases, status, nm)
        self.effet = effet


class Ressources(object):
    def __init__(self, name, ordre, quant):
        self.quant = quant
        self.nm = name
        self.decalage = 0
        self.ordre = ordre


class Desaster(object):  # on l'appelle a la fin du tour
    def __init__(self, name, nb_skull):
        self.nm = name
        self.nb_skull = nb_skull


class Dee(object):
    def __init__(self):
        self.__res = 0  # resultat du tirage
        self.gain = 0
        self.effect = "rien"
        self.step = 0

    @property
    def res(self):
        return self.__res

    @res.setter
    def res_setter(self, resultat):
        self.__res = resultat

    def correspondance(self):
        '''Allows to make the link between the dee's result and its effect '''
        if self.res == 1:
            self.effect = "3 Food"
        elif self.res == 2:
            self.effect = "1 Good"
        elif self.res == 3:
            self.effect = "2 Goods and 1 Skull	"
        elif self.res == 4:
            self.effect = "3 Workers"
        elif self.res == 5:
            self.effect = "2 Food or 2 Workers"
        elif self.res == 6:
            self.effect = "7 Coins"
        else:
            self.effect = 'none'
        return self.effect

    def throw(self):
        '''Gives a random number to simulate a dee'''
        self.__res = np.random.randint(1, 7)


def rollthroughtheages():
    ''' This function controls the entire game '''

    # definition des variables nécessaires
    global liste_joueur
    liste_joueur = []  # liste avce les objets players dedans
    # global liste_joueur

    # trame globale

    print(
        "                                 \033[1m" + "\033[91m" + 'Welcome to the game : Roll Through the Ages' + "\033[0m")
    print(' ')
    nombrejoueur = question('int', 'How many players wish to play ?', [i for i in range(2, 11)])
    print(' ')
    print("Please write your usernames.")
    for i in range(nombrejoueur):
        nom = input('Player n°{}'.format(i + 1))
        liste_joueur.append(Player(nom))  # création des joueurs
    for joueur in liste_joueur:
        nbmonument = joueur.nb_monument_accessible(
            nombrejoueur)  # on definit le nombre de monument en fonction du nombre de joueur

    print("\033[91m" + 'The game begins, player 1 starts' + "\033[0m")
    print(' ')
    while end(liste_joueur, nbmonument) == False:  # tant qu'il n'y a pas de fin de partie
        for j in range(nombrejoueur):
            liste_joueur[j].unTour()

    print(' ')
    print("\033[91m" + 'Somebody won ! END OF THE GAME' + "\033[0m")
    # Affichage des points
    for j in range(nombrejoueur):
        print(liste_joueur[j].nm, liste_joueur[j].f_point, 'points')
    re=question('str','Do you want a feed back of the game? yes/no',['yes','no'])
    if re=='yes':
        for i in liste_joueur:
            creer_compte_rendu_joueur(True, i.table, 'Compte rendu {}'.format(i.nm), 1,1,1,1,1,1,1,1,1,1,1,1,1,1)

def rollthroughtheagesbdd():
    ''' This function controls the entire game '''

    # definition des variables nécessaires
    cursor = bdd.connection()  # connexion à la bdd et generation du curseur
    l_looser = []  # liste des perdants
    m_date = datetime.datetime.now()  # date de la partie
    m_date.strftime("%x")  # formatage de la date
    # on genere le numero de la partie à partir du moment où elle est lancée :
    num_match = int(str(m_date.strftime("%S")) + str(m_date.strftime("%M")) + str(m_date.strftime("%H")) + str(
        m_date.strftime("%d")) + str(m_date.strftime("%m")) + str(m_date.strftime("%Y")))

    global liste_joueur
    liste_joueur = []  # liste avce les objets players dedans

    # global liste_joueur

    # trame globale

    print(
        "                                 \033[1m" + "\033[91m" + 'Welcome to the game : Roll Through the Ages' + "\033[0m")
    print(' ')
    nombrejoueur = question('int', 'How many players wish to play ?', [i for i in range(2, 11)])
    print(' ')
    print("Please write your usernames.")
    for i in range(nombrejoueur):
        nom = input('Player n°{}'.format(i + 1))
        iD = input("What's your game ID?")

        # download de la BDD
        ligne = bdd.fetch_player(cursor, "player", True, iD)
        num_played, num_won = ligne[0][2], ligne[0][3]

        liste_joueur.append(Player(nom, iD, num_played, num_won))  # création des joueurs

    for joueur in liste_joueur:  # on definit le nombre de monument en fonction du nombre de joueur
        nbmonument = joueur.nb_monument_accessible(nombrejoueur)
        joueur.matchP += 1

    print("\033[91m" + 'The game begins, player 1 starts' + "\033[0m")
    print(' ')
    while end(liste_joueur, nbmonument) == False:  # tant qu'il n'y a pas de fin de partie
        for j in range(nombrejoueur):
            liste_joueur[j].unTour()
    print(' ')
    print("\033[91m" + 'Somebody won ! END OF THE GAME' + "\033[0m")

    # Affichage des points
    for j in range(nombrejoueur):
        print(liste_joueur[j].nm, liste_joueur[j].f_point, 'points')

    # on determine le gagnant
    final_score = max([player.f_point for player in liste_joueur])
    for player in liste_joueur:
        if player.f_point == final_score:
            winner = player
        else:
            l_looser.append(player)

        # upload in the database
        bdd.insertion_match(cursor, "matches",str(tuple(num_match, winner.iD, winner.f_point, m_date)))  # données de la partie
        for player in liste_joueur:
            bdd.insertion_player(cursor, "player", str(tuple(player.num, player.nm, player.matchP, player.matchW)),player.iD)
        re = question('str', 'Do you want a feed back of the game? yes/no', ['yes', 'no'])
        if re == 'yes':
            for i in liste_joueur:
                creer_compte_rendu_joueur(True, i.table, 'Compte rendu {}'.format(i.nm), 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                          1, 1, 1, 1)

def end(L, nb):
    '''this fucntion is testing if the game is over or not:
        - a player has 5 developpments
        - a player built all the momuments

        entry: list with all the player ( Player class)
        exit: Bool , True if the game is over'''
    for player in L:
        if player.nb_dev >= 5:
            print('Player \033[1m{}\033[0m has 5 development'.format(player.nm))
            return True
        if player.nb_monument == nb:
            print('Player \033[1m{}\033[0m has all the monuments'.format(player.nm))
            return True
    return False
    #  A FAIRE test des developpements

    #  A FAIRE test des monuments

def suite(k, U1):  # fonction récursives
    if k <= 0:
        return 0
    elif k == 1:
        return U1
    else:
        return U1 * k + suite(k - 1, U1)


def question(type, question, listereponses_attendues):
    """check if the answer is correct or not"""

    while True:
        if type == 'int':
            try:
                reponse = int(input(question))
                if reponse in listereponses_attendues:
                    break
                else:
                    print("\033[3m" + "\033[33m" + "Wrong answer, please try again" + "\033[0m")
            except:
                print("\033[3m" + "\033[33m" + "Wrong answer, please try again" + "\033[0m")
        else:
            reponse = input(question)
            if reponse in listereponses_attendues:
                break
            else:
                print("\033[3m" + "\033[33m" + "Wrong answer, please try again" + "\033[0m")
    # Retourne la réponse de l'utilisateur
    return reponse

def creer_compte_rendu_joueur(end,table,nom_fichier,tour,points,food,wood,stone,pottery,cloth,arrow,skull,workers,coins,Monuments,Developments,cities):
    ''' Writes in a file the details and results of the game'''
    if end==True: # on fabrique la table
        table.field_names = ["Tour", "Points", "food","wood","stone","pottery","cloth","arrow","skulls", "workers","coins", "Monuments", "Developments", "cities"]
        with open(nom_fichier, "w") as f:
            f.write(str(table))
    else:
        table.add_row([tour, points, food,wood,stone,pottery,cloth,arrow,skull,workers,coins, ';'.join(Monuments),';'.join(Developments), ';'.join(cities)])


if __name__ == '__main__':
    rollthroughtheages()
    #rollthroughtheagesbdd() # Cette fonction sera pour la bdd, il nous manque que l'herbergeur de la base de donnée