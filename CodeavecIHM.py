from PyQt5.QtGui import QPixmap,QFont, QGuiApplication
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QStackedWidget,\
    QComboBox, QLineEdit, QGroupBox, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt,QEventLoop
import os
import PyQt5
import datetime
import numpy as np
import bdd as bdd
import subprocess
from PyQt5 import QtTest
from prettytable import PrettyTable

class FirstWindow(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        ######################## GESTION DES PAGES#########################

        # Création du widget empilé
        self.stacked_widget = QStackedWidget()

        # Création des pages
        page1 = QWidget()
        global page2
        page2 = QWidget()
        page3 = QWidget()

        # Ajout des pages au widget
        self.stacked_widget.addWidget(page1)
        self.stacked_widget.addWidget(page2)
        self.stacked_widget.addWidget(page3)

        ######################## PAGE 1 #########################
        self.setWindowTitle("Roll Through the Ages")
        #self.setFixedSize(400, 300)
        self.setGeometry(200, 200, 800, 600)

        # Créer une image pixmap pour l'image de fond
        file_path = os.path.abspath("Imagefondmenu1.jpg")
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(1100, 801)  # image de base : 2000*1456
        label = QLabel(page1)
        label.setPixmap(pixmap)

        # Créer des boutons pour la page1
        button_newgame = QPushButton("New Game", page1)  # Création du bouton pour changer de page
        button_continue = QPushButton("Continue", page1)
        button_rules = QPushButton("Rules", page1) # Création du bouton pour lire les règles
        button_scores = QPushButton("Score Board", page1)
        button_quit = QPushButton("Quit", page1) # Création du bouton pour quitter le jeu

        # Mettre en place le layout pour les boutons de la page1
        layout_buttons1 = QHBoxLayout()
        layout_buttons1.addWidget(button_newgame)
        layout_buttons1.addWidget(button_continue)
        layout_buttons1.addWidget(button_rules)
        layout_buttons1.addWidget(button_scores)
        layout_buttons1.addWidget(button_quit)

        # Mettre en place le layout principal de la page1
        layout1 = QVBoxLayout()
        layout1.addWidget(label)
        layout1.setAlignment(label, Qt.AlignCenter)
        layout1.addLayout(layout_buttons1)
        page1.setLayout(layout1)

        # Ajouter des actions aux boutons
        button_newgame.clicked.connect(self.changer_page)
        button_rules.clicked.connect(self.show_rules)
        button_newgame.clicked.connect(lambda: self.nb_joueur(self.label_mess))
        button_quit.clicked.connect(QApplication.quit)

        ######################## PAGE 2 #########################

        # Mise en place du plateau
        self.label2 = QLabel(page2)
        file_path2 = os.path.abspath("plateau.jpg")
        pixmap2 = QPixmap(file_path2)# taille 982 626
        pixmap2 = pixmap2.scaled(663, 423)
        self.label2.setPixmap(pixmap2)


        # Mise en place des tableau/image/boutons
        self.comboBox = QComboBox()
        self.submit = QPushButton("Submit", page2)
        self.label_tabl = QLabel(page2)  # label pour afficher le tableau de scores
        self.yes = QPushButton("Yes")
        self.no = QPushButton("No")
        self.label_tabl = QTableWidget()
        self.label_tabl.setFixedSize(600, 400)
        self.label_mess = QLabel(page2)  # label pour afficher le message

        # Layout du haut
        self.layout21 = QHBoxLayout()
        self.layout21.addWidget(self.label2, 0)
        self.layout21.addWidget(self.label_tabl, 0)

        # layout du bas
        self.layout22 = QHBoxLayout()
        self.layout22.addWidget(self.label_mess, 0)
        self.layout22.addWidget(self.comboBox, 0)
        self.layout22.addWidget(self.submit, 0)

        # encadrement
        group_box1 = QGroupBox("Messages")
        group_box2 = QGroupBox("Resources")

        # Mesure de la taille de l'écran
        screen_height = QGuiApplication.primaryScreen().availableGeometry().height()
        group_box1_height = round(screen_height / 2)
        group_box2_height = screen_height - group_box1_height

        # Définir le layout dans le QGroupBox
        group_box1.setLayout(self.layout22)
        group_box2.setLayout(self.layout21)

        # Mettre en place le layout principal de la page2
        layout2 = QVBoxLayout()
        layout2.addWidget(group_box2, 0)
        layout2.addWidget(group_box1, 0)
        group_box1.setFixedHeight(group_box1_height)
        group_box2.setFixedHeight(group_box2_height)
        page2.setLayout(layout2)

        #point à afficher sur le plateau
        file_point = os.path.abspath("point.png")

        self.labelfood = QLabel(page2)
        pixmapfood = QPixmap(file_point)
        pixmapfood = pixmapfood.scaled(20, 20)
        self.labelfood.setPixmap(pixmapfood)

        self.labelwood = QLabel(page2)
        pixmapwood = QPixmap(file_point)
        pixmapwood = pixmapwood.scaled(20, 20)
        self.labelwood.setPixmap(pixmapwood)

        self.labelstone = QLabel(page2)
        pixmapstone = QPixmap(file_point)
        pixmapstone = pixmapstone.scaled(20, 20)
        self.labelstone.setPixmap(pixmapstone)

        self.labelpottery = QLabel(page2)
        pixmappottery = QPixmap(file_point)
        pixmappottery = pixmappottery.scaled(20, 20)
        self.labelpottery.setPixmap(pixmappottery)

        self.labelcloth = QLabel(page2)
        pixmapcloth = QPixmap(file_point)
        pixmapcloth = pixmapcloth.scaled(20, 20)
        self.labelcloth.setPixmap(pixmapcloth)

        self.labelarrow= QLabel(page2)
        pixmaparrow = QPixmap(file_point)
        pixmaparrow = pixmaparrow.scaled(20, 20)
        self.labelarrow.setPixmap(pixmaparrow)


        ######################## BDD #########################
        global cursor
        global num_match
        global l_looser
        global m_date
        cursor, con = bdd.connection()  # connexion à la bdd et generation du curseur
        bdd.create_tables(cursor, con)
        l_looser = []  # liste des perdants
        m_date = datetime.datetime.now()  # date de la partie
        m_date.strftime("%x")  # formatage de la date
        # on genere le numero de la partie à partir du moment où elle est lancée :
        num_match = int(str(m_date.strftime("%S")) + str(m_date.strftime("%M")) + str(m_date.strftime("%H")) + str(
            m_date.strftime("%d")) + str(m_date.strftime("%m")) + str(m_date.strftime("%Y")))

        # autres variables
        self.statePress = False
        self.nombrejoueur = 1
        self.nom = 'JCVD'
        self.gameiD = 13
        self.gameiD_s = 42
        self.changerep = 0
        self.compt_joueur = 0
        self.firstP = True
        self.Ln=[]

        # Mettre en place le layout principal de la page1
        self.setCentralWidget(self.stacked_widget)

        # Ajouter des actions aux boutons
        self.submit.clicked.connect(self.answer)
        self.yes.clicked.connect(self.game_id_ex)
        self.no.clicked.connect(self.game_id_gen)

        self.loop = QEventLoop()

        ######################## MUSIC #########################

        #Si QtMultimedia disponible (hors Anaconda)

        #CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        #file_path4 = os.path.abspath("sound.mp3")
        #filename = os.path.join(CURRENT_DIR, file_path4)
        #player = PyQt5.QtMultimedia.QMediaPlayer()
        #url = PyQt5.QtCore.QUrl.fromLocalFile(filename)
        #player.setMedia(PyQt5.QtMultimedia.QMediaContent(url))
        #player.play()

        #sinon pygame
        import pygame
        pygame.init()
        pygame.mixer.init()
        chemin_fichier_audio = os.path.abspath("sound.mp3")
        pygame.mixer.music.load(chemin_fichier_audio)
        pygame.mixer.music.play(loops=-1)

    def changer_page(self):
        # Récupérer l'index de la page actuelle
        '''Change the page in the stacked widget'''

        index = self.stacked_widget.currentIndex()

        if index == 0:
            self.stacked_widget.setCurrentIndex(1)
        elif index == 1:
            self.stacked_widget.setCurrentIndex(2)
        else:
            self.stacked_widget.setCurrentIndex(0)

    def gen_combo(self, listereponse):
        '''Adds items to the comboBox  with answers

        entry: list of items to put into the combobox
        exit: None'''

        self.comboBox.clear()
        self.comboBox.addItems(listereponse)  # ajout items

    def answer(self):
        '''Gets the answer from the comboBox,
        Determines the number of players'''

        self.nombrejoueur = int(self.comboBox.currentText())    # nombre de joueur
        self.changerep += 1
        self.line_edit = QLineEdit(self)
        self.layout22.addWidget(self.line_edit, 1)  # adds the QLineEdit
        self.layout22.addWidget(self.submit, 0)  # adds the submit QPushButton
        self.label_mess.setText(
            "Please write your username Player n°{}".format(str(self.compt_joueur + 1)))  # first player
        self.submit.disconnect()
        self.submit.clicked.connect(self.game_id)

    def name(self):
        '''Gets the players' names from the lineEdit widget'''

        if self.compt_joueur == self.nombrejoueur:
            self.yes.hide()
            self.no.hide()
            self.submit.show()
            self.submit.setText("Submit")
            self.submit.clicked.disconnect(self.name)
            self.submit.clicked.connect(self.sending)
            self.line_edit.hide()
            self.layout22.update()
            self.comboBox.show()  # showing the QComboBox widget
            self.rollthroughtheages()  # launching the game

            # game ended, seeking winner
            final_score = max([player.f_point for player in self.liste_joueur])
            for player in self.liste_joueur:
                if player.f_point == final_score:
                    winner = player
                    winner.matchW += 1
                else:
                    l_looser.append(player)

                # upload in the database
                bdd.insertion_match(cursor, "matches",
                                    str(tuple(num_match, winner.iD, winner.f_point, m_date)))  # données de la partie
                for player in self.liste_joueur:
                    bdd.insertion_player(cursor, "player",
                                         str(tuple(player.num, player.nm, player.matchP, player.matchW)),
                                         player.iD)

        else:
            self.submit.setText("Submit")
            self.submit.clicked.connect(self.game_id)
            self.comboBox.hide()  # hiding the QComboBox widget
            self.line_edit.show()
            self.label_mess.setText("Please write your username Player")

    def game_id(self):
        '''Asks user if he has a gameiD'''

        self.nom = self.line_edit.text()
        self.line_edit.clear()
        self.layout22.addWidget(self.yes)
        self.layout22.addWidget(self.no)
        self.no.show()
        self.yes.show()
        self.submit.hide()
        self.line_edit.hide()
        self.submit.disconnect()
        self.label_mess.setText("Do you have a gameiD {} ?".format(str(self.nom)))  # gameiD

    def game_id_ex(self):
        '''Called when gameiD already exists'''

        self.yes.hide()
        self.no.hide()
        self.submit.show()
        self.label_mess.setText("Please, enter your gameiD {}".format(str(self.nom)))   # gameiD
        self.line_edit.show()
        self.submit.clicked.connect(self.creat_p_ex)  # connecting to new slot

    def creat_p_ex(self):
        '''Creates a player when gameid exists'''

        self.gameiD = self.line_edit.text()
        try:
            ligne = bdd.fetch_player(cursor, "player", self.gameiD, True)  # fetching player's data
        except bdd.DatabaseError as er:
            self.label_mess.setText("There was a problem retrieving your data")
        else:
            num_played, num_won = int(ligne[0][2]), int(ligne[0][3])
            self.liste_joueur.append(Player(self.nom, self, self.gameiD, num_played, num_won))  # adding player
            self.compt_joueur += 1  # joueur crée
            self.label_mess.setText("We find your data in the database")
        self.submit.disconnect()
        self.submit.clicked.connect(self.name)  # connecting to new slot
        self.submit.setText("OK")
        self.submit.show()
        self.layout22.update()

    def game_id_gen(self):
        '''Called when gameiD doesn't exists, generates one'''

        self.no.hide()
        self.yes.hide()
        try:
            bdd_res = bdd.mx_giD(cursor)  # max gameiD used, in tuple
        except bdd.DatabaseError as er:
            self.label_mess.setText("there was a problem creating your gameiD")
        else:
            self.gameiD = int(bdd_res[0]) + 1  # gameiD of the new player
            if self.gameiD == self.gameiD_s:  # 42 is used for the player's gameiD when there's a problem with the database
                self.gameiD = 43
            self.label_mess.setText(
                "Here is your gameiD {} \n \n {}".format(self.nom, self.gameiD))  # gameiD
            self.liste_joueur.append(Player(self.nom, self, self.gameiD, 0, 0))  # adding the player
            self.compt_joueur += 1
        self.submit.clicked.connect(self.name)
        self.submit.setText("OK")
        self.submit.show()
        self.layout22.update()

    def end(self, L, nb):
        '''this fucntion is testing if the game is over or not:
            - a player has 5 developments
            - a player built all the momuments

            entry: list with all the player ( Player class)
            exit: Bool , True if the game is over'''

        for player in L:
            if player.nb_dev >= 5:
                self.label_mess.setText('Player {} has 5 development'.format(player.nm))
                return True
            if player.nb_monument == nb:
                self.label_mess.setText('Player {} has all the monuments'.format(player.nm))
                return True
        return False

    def sending(self):

        '''Quits the QEventLoop when called'''
        self.loop.quit()

    def nb_joueur(self, label_mess):
        '''Used to determine the number of player'''

        self.liste_joueur = []  # liste avce les objets players dedans
        label_mess.setText(
            "\n" + 'Welcome to the game : Roll Through the Ages' + "\n" + '\n' + '\n' + 'How many players wish to play ?')

        self.gen_combo([str(i) for i in range(2, 11)])

    def rollthroughtheages(self):
        ''' This function starts the game '''

        self.layout22.addWidget(self.submit, 0)
        for joueur in self.liste_joueur:  # on definit le nombre de monument en fonction du nombre de joueur
            nbmonument = joueur.nb_monument_accessible(self.compt_joueur)
            joueur.matchP += 1

        self.label_mess.setText('The game begins, player 1 starts')
        while self.end(self.liste_joueur, nbmonument) == False:  # tant qu'il n'y a pas de fin de partie
            for j in range(self.compt_joueur):
                self.liste_joueur[j].unTour()
        self.label_mess.setText('Somebody won ! END OF THE GAME')

        # Affichage des points
        for j in range(self.compt_joueur):
            self.ajoutmess(str(self.liste_joueur[j].nm) + str(self.liste_joueur[j].f_point) + 'points', True)
        # Compte rendu
        for i in self.liste_joueur:
            creer_compte_rendu_joueur(True, i.table, 'Compte rendu {}'.format(i.nm), i.food.quant, i.wood.quant, i.stone.quant,i.pottery.quant,
                                      i.cloth.quant,i.arrow.quant, i.skull, i.worker.quant, i.coins.quant, i.nb_city,i.nb_monument,i.d)
    def show_rules(self):
        ''' Open a pdf which explains the rules '''

        file_path = os.path.abspath("règle.pdf")
        subprocess.run(['start', '', file_path], shell=True)  # Windows
        # subprocess.run(['open', file_path])  # macOS

class Point(list):
    ''' This class is used to create and move put points that will be on the game board '''

    def __init__(self,name,ox,oy,label,ord):
        self.orx=ox
        self.ory=oy
        self.append(ox) # origine de x
        self.append(oy) #origine de y
        self.nm=name
        self.ord = ord
        self.x,self.y = self.coord(0)
        self.label=label
        self.label.setGeometry(self.x, self.y, 20, 20)

    def coord(self,m):
        '''the function gives all the coordinates to place the points'''

        position = np.array(
            [[(self.orx + 70, self.ory + 52), (self.orx + 143, self.ory + 52), (self.orx + 206, self.ory + 52), (self.orx + 271, self.ory + 52), (self.orx + 329, self.ory + 52),
              (self.orx + 329, self.ory + 52),(self.orx + 329, self.ory + 52),(self.orx + 329, self.ory + 52),(self.orx + 329, self.ory + 52),(self.orx + 329, self.ory + 52),
              (self.orx + 329, self.ory + 52),(self.orx + 329, self.ory + 52),(self.orx + 329, self.ory + 52),(self.orx + 329, self.ory + 52),(self.orx + 329, self.ory + 52),
              (self.orx + 329, self.ory + 52),],
             [(self.orx + 75, self.ory + 117), (self.orx + 150, self.ory + 117), (self.orx + 207, self.ory + 117), (self.orx + 269, self.ory + 117), (self.orx + 334, self.ory + 117),
              (self.orx + 390, self.ory + 117),(self.orx + 390, self.ory + 117),(self.orx + 390, self.ory + 117),(self.orx + 390, self.ory + 117),(self.orx + 390, self.ory + 117),
              (self.orx + 390, self.ory + 117),(self.orx + 390, self.ory + 117),(self.orx + 390, self.ory + 117),(self.orx + 390, self.ory + 117),(self.orx + 390, self.ory + 117),
              (self.orx + 390, self.ory + 117)],
             [(self.orx + 71, self.ory + 178), (self.orx + 151, self.ory + 178), (self.orx + 210, self.ory + 178), (self.orx + 278, self.ory + 178), (self.orx + 336, self.ory + 178),
              (self.orx + 397, self.ory + 178), (self.orx + 458, self.ory + 178),(self.orx + 458, self.ory + 178),(self.orx + 458, self.ory + 178),(self.orx + 458, self.ory + 178),
              (self.orx + 458, self.ory + 178),(self.orx + 458, self.ory + 178),(self.orx + 458, self.ory + 178),(self.orx + 458, self.ory + 178),(self.orx + 458, self.ory + 178),
              (self.orx + 458, self.ory + 178)],
             [(self.orx + 72, self.ory + 243), (self.orx + 149, self.ory + 243), (self.orx + 212, self.ory + 243), (self.orx + 269, self.ory + 243), (self.orx + 331, self.ory + 243),
              (self.orx + 391, self.ory + 243), (self.orx + 448, self.ory + 243), (self.orx + 511, self.ory + 243),(self.orx + 511, self.ory + 243),(self.orx + 511, self.ory + 243),
              (self.orx + 511, self.ory + 243),(self.orx + 511, self.ory + 243),(self.orx + 511, self.ory + 243),(self.orx + 511, self.ory + 243),(self.orx + 511, self.ory + 243),
              (self.orx + 511, self.ory + 243)],
             [(self.orx + 77, self.ory + 308), (self.orx + 149, self.ory + 308), (self.orx + 205, self.ory + 308), (self.orx + 271, self.ory + 308), (self.orx + 334, self.ory + 308),
              (self.orx + 392, self.ory + 308), (self.orx + 453, self.ory + 308), (self.orx + 509, self.ory + 308), (self.orx + 574, self.ory + 308),(self.orx + 574, self.ory + 308),
              (self.orx + 574, self.ory + 308),(self.orx + 574, self.ory + 308),(self.orx + 574, self.ory + 308),(self.orx + 574, self.ory + 308),(self.orx + 574, self.ory + 308),
              (self.orx + 574, self.ory + 308)],
             [(self.orx +75, self.ory + 371),(self.orx +153,self.ory + 371),(self.orx +180,self.ory + 371),(self.orx +211,self.ory + 371),(self.orx +244,self.ory + 371),
              (self.orx +276,self.ory + 371),(self.orx +304,self.ory + 371),(self.orx +335,self.ory + 371),(self.orx +367,self.ory + 371),(self.orx +400,self.ory + 371),
              (self.orx +433,self.ory + 371),(self.orx +460,self.ory + 371),(self.orx +496,self.ory + 371),(self.orx +526,self.ory + 371),(self.orx +553,self.ory + 371),
              (self.orx +583,self.ory + 371)]
             ])
        return position[self.ord][m][0],position[self.ord][m][1]

    def move(self,a):
        '''the function permits to move a point'''

        self.x = a
        self.label.setGeometry(self.coord(a)[0],self.coord(a)[1],20, 20)
class Player(object):
    '''This class defines a player'''

    def __init__(self, nom, window, iD, matchP, matchW):

        # attributs de gestion du joueurs
        self.nm = nom
        self.point = [0, 0, 0, 0,
                      0]  # detail des points: developpment,monument,desastre,ville non nourrie,ville ( cas ingénieur)
        self.f_point = sum(self.point)  # nombre de points finaux
        self.skull = 0  # nombre de crane obtenu
        self.nb_city = 3  # nombre initial de ville
        self.max_relance = 2  # on ne peux relancer que 2 fois
        self.souhait_nb_relance = self.nb_city  # nombre de dee a relancer, doit initialement etre egale au nombre de ville

        # attributs liés aux ressources
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
        self.leadership = Developement(2, 2, 10, 1, False, "Leadership",
                                       "Re-roll one die")  # False veut dire non acheté
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
        self.architecture = Developement(8, 6, 50, 1, False, "Architecture",
                                         "1 additional point for every monument")
        self.empire = Developement(8, 6, 60, 1, False, "Empire", "1 additional point for every city")
        self.liste_developpement = [self.leadership, self.irrigation, self.agriculture, self.quarrying,
                                    self.medicine,
                                    self.coinage, self.caravans, self.religion, self.granaries, self.masonry,
                                    self.engineering, self.architecture, self.empire]
        self.liste_nm_dev = [dev.nm for dev in self.liste_developpement]
        self.nb_dev = 0
        self.farchit = False  # pour ajuster les points au moment ou il achete architecte
        self.femp = False  # pour ajuster les points au moment ou il achete architecte

        # attributs liés aux cités
        self.city_sup1 = Construction(1, 1, 3, 0, False, "Roubaix", window)
        self.city_sup2 = Construction(1, 1, 4, 0, False, "Paris", window)
        self.city_sup3 = Construction(1, 1, 5, 0, False, "New-York", window)
        self.city_sup4 = Construction(1, 1, 6, 0, False, "Singapour", window)
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
        self.d=' ' # liste develomment

        # Données mémorisées pour la base de donnée et le compte rendu sous forme de fichier
        self.table = PrettyTable()
        self.ftour = 0

        # attributs liés à la BDD
        self.iD = iD  # gameiD
        self.matchP = matchP  # number of match played
        self.matchW = matchW  # number of match won

        #points affichage
        x,y=18,15
        self.pfood = Point('food',x,y,window.labelfood,5)
        self.pwood = Point('wood',x,y,window.labelwood,4)
        self.pstone = Point('stone',x,y,window.labelstone,3)
        self.ppottery = Point('pottery',x,y,window.labelpottery,2)
        self.pcloth = Point('cloth',x,y, window.labelcloth,1)
        self.parrow = Point('arrow',x,y,window.labelarrow,0)
        self.liste_points=[self.pfood,self.pwood,self.pstone,self.ppottery,self.pcloth,self.parrow]

    def ajoutmess(self, m, bool):  # bool pour savoir si on saute une ligne
        '''This function adds a text to the label_mess
            entry: m:message(str)
                bool: boolean
            exit: none'''

        t = window.label_mess.text()
        if bool == True:
            window.label_mess.setText(t + '\n' + '\n' + m)
        else:
            window.label_mess.setText(t + '\n' + m)

    def affichage(self):
        '''This function creats the scoreboard'''

        rows = 8
        columns = 2
        window.label_tabl.setRowCount(rows)
        window.label_tabl.setColumnCount(columns)
        d = []
        for i in self.liste_developpement:
            if i.status == True:
                d.append(str(i.nm))
        self.d = ' '.join(d)
        data = np.array([['Player', str(self.nm)],
                         ['Skulls', str(self.skull)],
                         ['Coins', str(self.coins.quant)],
                         ['Workers', str(self.workers.quant)],
                         ['Number of throw', str(self.max_relance)],
                         ['City', str(self.nb_city)],
                         ['Monument', str(self.nb_monument)],
                         ['Development', self.d]])
        font = QFont('Arial', 16)
        for row in range(rows):
            for column in range(columns):
                item = QTableWidgetItem(data[row][column])
                item.setFont(font)
                window.label_tabl.setItem(row, column, item)

        # Définir les en-têtes de colonnes
        headers = ['objects', 'quantity', self.nm]
        window.label_tabl.setHorizontalHeaderLabels(headers)

        cell_height = 40
        cell_width = 300
        for row in range(rows):
            window.label_tabl.setRowHeight(row, cell_height)  # Définir la hauteur des lignes
        for column in range(columns):
            window.label_tabl.setColumnWidth(column, cell_width)

        #mise a jour des points
        for i in range(len(self.liste_points)):
            if i==0:
                self.liste_points[i].move(self.plateau[i].quant)
            else:
                self.liste_points[i].move(self.plateau[i].decalage)

    def nb_monument_accessible(self, nb_joueur):
        '''Gives acces to a certain number of monuments according to the nuber of player
            entry: nb_joueur: number of players (int)
            exit: att: number of monuments accessible (int)'''

        att = 7
        for k in range(len(self.liste_monuments)):
            if nb_joueur == 2 and (self.liste_monuments[k].nm in ("Pyramide", "StoneHedge", "Obelisque", "Great Wall")):
                self.liste_monuments[k].acces_setter = True
                att = 4
            elif nb_joueur == 3 and (self.liste_monuments[k].nm in (
                    "Pyramide", "StoneHedge", "Obelisque", "Great Wall", "Temple", "Great Pyramide")):
                self.liste_monuments[k].acces_setter = True
                att = 6
            elif nb_joueur > 3:
                self.liste_monuments[k].acces_setter = True
                att = 7
            else:
                self.liste_monuments[k].acces_setter = False
        return att

    def alimenter(self):
        '''Feeds the cities'''

        self.food.quant -= self.nb_city
        window.label_mess.setText('You feed your cities')
        QtTest.QTest.qWait(1000)


    def unTour(self):
        '''Simulates a round for the player'''

        self.ftour += 1
        self.affichage()
        window.label_mess.setText('It is the turn of {}'.format(self.nm))
        QtTest.QTest.qWait(1000)

        self.tirage()  # on lance les dees
        self.affichage()
        self.alimenter()  # on alimente
        self.affichage()
        if self.food.quant < 0:
            self.point[
                3] += self.food.quant  # on PERD des points lorsque l'on ne peut plus alimenter les villes, attention c'est negatif
            window.label_mess.setText("You have not fed {} cities, you loose {} points".format(-self.food.quant,
                                                                                               -self.food.quant))
            self.food.quant = 0  # modifier avec le getter?
        self.desastereffect()  # on impose les desastre
        self.affichage()
        # dans le cas d'un ingénieur:
        if self.engineering.status == True and self.stone.quant > 0:
            self.ajoutmess('BUT You have engineering, do you want to exchange 1 stone for 3 workers?', True)
            window.gen_combo(['yes', 'no'])
            window.loop.exec_()
            r = window.comboBox.currentIndex()
            if int(r) == 0:
                self.workers.quant += 3
                self.stone.decalage -= 1
                self.stone.quant = suite(self.stone.decalage, 2)
            self.affichage()
        self.affichage()
        if self.workers.quant > 0:
            while self.workers.quant > 0:
                QtTest.QTest.qWait(1000)
                window.label_mess.setText("Where do you want to place your  {} workers?".format(self.workers.quant))
                window.gen_combo(["city", "monument"])
                window.loop.exec_()
                constru = window.comboBox.currentIndex()

                # achat cite
                if int(constru) == 0:
                    QtTest.QTest.qWait(1000)
                    window.label_mess.setText('You can build')
                    possible = []
                    for cite in self.liste_cite:  # affichage des noms
                        if cite.status == False:
                            self.ajoutmess('{:<15}   {:<2} workers remaining'.format(cite.nm, cite.cost - cite.cases),
                                           True)
                            possible.append(cite.nm)
                    self.ajoutmess("What is the name of the city?", True)
                    window.gen_combo(possible)
                    window.loop.exec_()
                    nom_cite = window.comboBox.currentText()
                    for construction in self.liste_cite:  # on construit si possible
                        if construction.test_construction() == True and construction.nm == nom_cite:  # on acquiert
                            self.workers.quant, self.nb_city, bool = construction.construire(self.workers.quant,
                                                                                             self.nb_city)
                            if self.empire.status == True and bool == True:  # bool= est ce que l'achat a été fait?
                                self.point[4] += 1
                    self.affichage()

                # achat monument
                else:
                    possible2 = []
                    for monument in self.liste_monuments:  # affichage des noms
                        if monument.status == False:
                            self.ajoutmess(
                                '{:<15}   {:<2} workers remaining'.format(monument.nm, monument.cost - monument.cases),
                                False)
                            possible2.append(monument.nm)
                    self.ajoutmess("What is the name of the monument?", False)
                    window.gen_combo(possible2)
                    window.loop.exec_()
                    nom_monument = window.comboBox.currentText()
                    for monument in self.liste_monuments:
                        if monument.test_construction() == True and monument.nm == nom_monument and monument.acces == True:  # test d'aqcuisition
                            self.workers.quant, self.nb_monument, bool = monument.construire(self.workers.quant,
                                                                                             self.nb_monument)  # on acquiert
                            for joueur in window.liste_joueur:  # on cherche à savoir s'il s'agit de l'acquereur primaire
                                # retirer le joueur actuel du test
                                if joueur.nm != self.nm and bool == True:
                                    monument.first_buy = True
                                    for monument_bis in joueur.liste_monuments:
                                        if monument_bis.fisrt_buy == True:
                                            monument.first_buy = False

                                    if monument.first_buy == True:  # attribution du nombre de point en fonction de l'ordre d'acquisition
                                        if self.architecture.status == True:
                                            self.point[1] += (monument.point_max + 1)
                                        else:
                                            self.point[1] += monument.point_max
                                    else:
                                        if self.architecture.status == True:
                                            self.point[1] += (monument.point_min + 1)
                                        else:
                                            self.point[1] += monument.point_min
                    # achat developpement
                    self.affichage()
        S = 0
        for res in self.gestionressource:
            if res.quant > 0:
                S += res.quant
        # developpment grenier
        if self.granaries.status == True and self.food.quant > 0:
            window.gen_combo(['yes', 'no'])
            QtTest.QTest.qWait(1000)
            window.label_mess.setText(' BUT You have granaries, do you want to sell 1 food for 4 coins?')
            window.loop.exec_()
            r = window.comboBox.currentText()
            if r == 'yes':
                self.food.quant -= 1
                self.coins.quant += 4
        self.affichage()
        S2 = self.coins.quant
        if S + S2 > 0:
            window.gen_combo(['yes', 'no'])
            QtTest.QTest.qWait(1000)
            window.label_mess.setText("Do you want to buy a development?")
            window.loop.exec_()
            achat_dev = window.comboBox.currentText()
            if achat_dev == "yes":
                no = 0  # compter le nombre de dev achetable
                text = "{:<15} {:<15} {:<15} {:<30}".format('name', 'point', 'cost', 'effect') + '\n'
                text += '------------------------------------------------------------------------------' + '\n'
                for dev in self.liste_developpement:
                    if dev.status == False and dev.cost <= S + S2:
                        text += "{:<15} {:<15} {:<15} {:<30}".format(dev.nm, dev.point_max,
                                                                     dev.cost,
                                                                     dev.effet) + '\n'
                        no += 1
                window.label_mess.setText(text)
                if no == 0:
                    self.ajoutmess("Sorry you can't buy any development", False)
                    QtTest.QTest.qWait(1000)
                else:
                    self.ajoutmess('Which development do you want to buy ?', True)
                    window.gen_combo([i for i in self.liste_nm_dev])
                    window.loop.exec_()
                    nom_dev = window.comboBox.currentText()
                    for developp in self.liste_developpement:
                        prix = developp.cost
                        if developp.test_construction(S + S2, prix) and developp.nm == nom_dev:  # on acquiert
                            # print('You are using your coins')
                            prix -= self.coins.quant
                            self.coins.quant = 0
                            while prix > 0:
                                possible3 = []
                                QtTest.QTest.qWait(1000)
                                window.label_mess.setText("There is still an amount to pay {} resources".format(prix))
                                for ressource in self.gestionressource:
                                    if self.gestionressource[ressource.ordre].decalage > 0:
                                        self.ajoutmess(ressource.nm, False)
                                        possible3.append(ressource.nm)
                                QtTest.QTest.qWait(1000)
                                self.ajoutmess("Which resource do you want to use?", False)
                                window.gen_combo(possible3)
                                window.loop.exec_()
                                n = window.comboBox.currentText()
                                for ressource in self.gestionressource:
                                    if ressource.nm == n:
                                        prix -= suite(self.gestionressource[ressource.ordre].decalage, ressource.ordre)
                                        self.gestionressource[ressource.ordre].decalage = 0
                            window.label_mess.setText("You have obtained the development {}".format(developp.nm))
                            QtTest.QTest.qWait(2000)
                            # Ajustement des points s'il vient d'acheter Architecture
                            developp.status = True
                            self.nb_dev += 1
                            if self.architecture.status == True and self.farchit == False:
                                self.farchit = True
                                self.point[1] += self.nb_monument
                            # Ajustement des points s'il vient d'acheter Empire
                            if self.empire.status == True and self.femp == False:
                                self.femp = True
                                self.point[4] += self.nb_city
                            self.point[0] += developp.point_max  # ajout des points
                        elif developp.test_construction(S) == False:
                            self.ajoutmess(
                                "You do not have enough resources OR you have already purchased the development", False)
                        self.affichage()
        # PARTIE DE TEST POUR NE PAS DEPASSER 7 DECALAGES DE RESSOURCES
        self.affichage()
        sommedec = 0
        for j in range(1, 6):
            sommedec += self.gestionressource[j - 1].decalage
        while sommedec > 6 and self.caravans.status == False:  # Si decalage et pas la carvane
            sommedec = 0
            for j in range(1, 6):
                sommedec += self.gestionressource[j - 1].decalage

            text = 'You have too many resources'
            Lnom = []
            text += '\n' + '{:<12} {:<12} '.format('resource', 'quantity')
            for i in self.gestionressource:
                if i.decalage > 0:
                    Lnom.append(i.nm)
            text += '\n' + "Which one do you want to throw away?"
            QtTest.QTest.qWait(1000)
            window.label_mess.setText(text)
            window.gen_combo(Lnom)
            window.loop.exec_()
            a = window.comboBox.currentText()
            self.affichage()
            if a == 'wood':
                self.wood.decalage -= 1
                self.wood.quant = suite(self.wood.decalage, 1)
            elif a == 'stone':
                self.stone.decalage -= 1
                self.stone.quant = suite(self.stone.decalage, 2)
            elif a == 'pottery':
                self.pottery.decalage -= 1
                self.pottery.quant = suite(self.pottery.decalage, 3)
            elif a == 'cloth':
                self.cloth.decalage -= 1
                self.cloth.quant = suite(self.cloth.decalage, 4)
            else:
                self.arrow.decalage -= 1
                self.arrow.quant = suite(self.arrow.decalage, 5)
            self.affichage()
        window.label_mess.setText('NEXT PLAYER')
        QtTest.QTest.qWait(1000)
        self.f_point = sum(self.point)

    def gestion(self, n):
        '''This function manages/counts the ressources according to the rules
            entry: n: number of pyramidal incrementation (int)'''

        if n == 0:
            return 'gestion(0)'
        signe = n // abs(n)
        # Mise a jour des décalage
        if signe > 0:
            debut = self.memoireR  # endroit ou il faut bouger ( dernier mv +1)
            for i in range(debut, debut + n):
                if (self.quarrying.status == True) and (
                        i % 5 == 1):  # si on a la carrière et qu'on augmente la pierre
                    self.gestionressource[i % 5].decalage += 2
                else:
                    self.gestionressource[i % 5].decalage += 1
            self.memoireR = (n + self.memoireR) % 5
        else:
            # cette partie sert a retirer si le joueur veut relancer
            debut = (self.memoireR - 1) % 5  # endroit ou il faut commencer
            for u in range(debut, debut + n, -1):  # attention n est negatif
                if (self.quarrying.status == True) and (
                        u % 5 == 1):  # si on a la carrière et qu'on augmente la pierre
                    self.gestionressource[u % 5].decalage -= 2
                else:
                    self.gestionressource[u % 5].decalage -= 1
            self.memoireR = (debut + n) % 5

        # Mise a jour des quantité
        for j in range(1, 6):
            self.gestionressource[j - 1].quant = suite(self.gestionressource[j - 1].decalage, j)

    def tirage(self):
        '''Gives a random number to simulate a die
        Management of the die throw and re-throw'''

        dee = Dee()  # création d'un dee
        list_dee = [0, 0, 0, 0, 0, 0]  # pour faire l'affichage des dees au joueur
        # autre idée: faire liste avec chacun des valeurs correspond a un dé

        self.skull = 0
        self.coins.quant = 0  # on remet l'argent à 0 avant chaque lancer
        self.workers.quant = 0  # on remet à 0 car on stock pas les travailleurs
        relance = 'yes'
        nbskullpert = 0  # s'il y a que des crânes, on ne redemande pas de retirer

        self.souhait_nb_relance = self.nb_city
        nbde = self.souhait_nb_relance
        self.max_relance = 2
        self.memoireR = 0
        while relance == "yes" and self.max_relance >= 0:  # on veut relancer
            window.label_mess.setText("You are throwing dice")

            for k in range(self.souhait_nb_relance):  # 1 throw for 1 city
                QtTest.QTest.qWait(1000)
                dee.throw()  # on lance le dee
                list_dee[dee.res - 1] += 1
                effect = dee.correspondance()  # on donne l'effet
                if k == 0:
                    self.ajoutmess("{}".format(effect), True)  # affichage résultat
                else:
                    self.ajoutmess("{}".format(effect), False)
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
                    self.ajoutmess("Choose between 2 food or 2 workers", False)
                    window.gen_combo(['workers', 'food'])
                    window.loop.exec_()
                    choice = window.comboBox.currentText()
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
                    self.affichage()
                elif effect == "7 Coins":
                    if self.coinage.status == True:
                        self.coins.quant += 12
                    else:
                        self.coins.quant += 7
                self.affichage()

            # gestion de la relance
            if self.max_relance == 0:  # on inverse pas
                QtTest.QTest.qWait(1000)
                window.label_mess.setText("Maximum number of dice rolls reached")
                self.max_relance = 2
                break
            if nbskullpert == nbde:  # si il a eu que des cranes
                break
            self.ajoutmess("Do you want to roll at least one die again?", True)
            window.gen_combo(['yes', 'no'])
            window.loop.exec_()
            relance = window.comboBox.currentText()
            if relance == "yes":  # on inverse pas
                list_relance = [0, 0, 0, 0, 0, 0]
                for d in range(6):  # pour tous les dees de tirées
                    if d != 2:  # si c est pas un crane
                        for j in range(1, list_dee[d] + 1):
                            temp = Dee()
                            temp.res_setter = d + 1
                            temp.correspondance()
                            window.label_mess.setText(
                                "Do you want to reroll the {}-th die with a value of {} ? ".format(
                                    j, temp.effect))
                            window.gen_combo(['yes', 'no'])
                            window.loop.exec_()
                            choix = window.comboBox.currentText()
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
                self.affichage()
        self.affichage()
        if self.leadership.status == True:
            self.ajoutmess("BUT You have leadership , do you want to play a last die?", True)
            window.gen_combo(['yes', 'no'])
            window.loop.exec_()
            r = window.comboBox.currentText()
            if r == 'yes':
                list_relance = [0, 0, 0, 0, 0, 0]
                for d in range(6):  # pour tous les dees de tirées
                    for j in range(1, list_dee[d] + 1):
                        temp = Dee()
                        temp.res_setter = d + 1
                        temp.correspondance()
                        QtTest.QTest.qWait(1000)
                        window.label_mess.setText(
                            "Do you want to reroll the {}-th die with a value of {} ? ".format(
                                j, temp.effect))
                        window.gen_combo(['yes', 'no'])
                        window.loop.exec_()
                        choix = window.comboBox.currentText()
                        if choix == 'yes':
                            list_relance[d] += 1
                            break  # on ne relance qu'un seul dé
                self.affichage()
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
                        self.affichage()
                dee.throw()  # on lance le dee
                list_dee[dee.res - 1] += 1
                effect = dee.correspondance()  # on donne l'effet
                QtTest.QTest.qWait(1000)
                window.label_mess.setText("{}".format(effect))
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
                    self.ajoutmess("Choose between 2 food or 2 workers", False)
                    window.gen_combo(['workers', 'food'])
                    window.loop.exec_()
                    choice = window.comboBox.currentText()
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
                    self.affichage()
                elif effect == "7 Coins":
                    self.coins.quant += 7
                self.affichage()

    def desastereffect(self):
        '''Execute effects depending on the number of skulls'''

        window.label_mess.setText('You have {} skulls'.format(self.skull))
        QtTest.QTest.qWait(1000)
        if self.skull == 2:
            if self.irrigation.status == True:
                self.ajoutmess('You have irrigation, you are protected', True)
            else:
                self.ajoutmess('You have a drought, -2 points', True)
                self.point[2] -= 2

        elif self.skull == 3:  # tester medecine pour chaque joueur/ si pas de medecine=> -3 points:
            for joueur in window.liste_joueur:
                if joueur.medicine.status == False and joueur.nm != self.nm:
                    self.ajoutmess("joueur {} doesn't have medicine: -3 points".format(joueur.nm), True)
                    self.point[2] -= 3
        elif self.skull == 4:
            if self.greatwall.status == True:
                self.ajoutmess('You have the Great Wall, your are protected', True)
            else:
                self.ajoutmess('You have an Invasion, -4 points', True)
                self.point[2] -= 4

        elif self.skull == 4:  # au moins 5 têtes de morts
            if self.religion.status == True:
                self.ajoutmess('You have religion, you are protected, let see the other', True)
                for joueur in window.liste_joueur:  # tester la religion sur chacun des joueurs et enlever des points
                    if joueur.medicine.status == True and joueur.nm != self.nm:
                        self.ajoutmess("joueur {} doesn't have religion: HE LOSES EVERYTHING !".format(
                            joueur.nm), True)
                        (joueur.wood.quant, joueur.stone.quant, joueur.pottery.quant, joueur.cloth.quant,
                         joueur.arrow.quant) = (0, 0, 0, 0, 0)
            else:
                self.ajoutmess('invasion, HE LOSES EVERYTHING', True)
                self.food.quant, self.stone.quant, self.wood.quant, self.pottery.quant, self.cloth.quant, self.arrow.quant = 0, 0, 0, 0, 0, 0
        else:
            self.ajoutmess('no effect', True)
        self.affichage()
        QtTest.QTest.qWait(1000)

class Construction(object):  # classe mère de Monuments, Cités, Developpement
    '''This class build the Monument, city and develpemnt'''

    def __init__(self, point_max, point_min, cost, cases, status, name, window):
        self.point_max = point_max  # point max rapportes
        self.point_min = point_min  # point min rapportes
        self.cost = cost  # valeurs necessaires pour acquerir la construction, nombre de cases,ouvrier, monnaie, ressources
        self.cases = cases  # nombre de cases cochées
        self.status = status  # status acquis ou non
        self.nm = name

    def __str__(self):
        return self.nm

    def test_construction(self, res=1, prix=0):
        '''Test if a construction can be build
        entry: res: player's ressources(int)
        exit: prix: construction's price(int)'''

        if self.status == False and res > prix:
            return True

    def construire(self, worker, nb_monument):
        '''Ask the player if he/she wants to build a construction
            entry: worker: player's number of workers(int)
                    nb_monument: player's number of monument(int)
            exit: worker, nb_monument
                    bool: boolean to know if the monument is acquired'''

        QtTest.QTest.qWait(1000)
        window.label_mess.setText("You have {} workers".format(worker))
        window.label_mess.setText("How many workers do you want to use?")
        window.gen_combo([str(i + 1) for i in range(worker)])
        window.loop.exec_()
        nb_ouvrier = int(window.comboBox.currentText())
        bool = False  # savoir si ya eu un achat
        self.cases += nb_ouvrier
        worker -= nb_ouvrier
        if self.cases >= self.cost:
            worker += (self.cases - self.cost)
            self.cases == self.cost
            self.status = True
            window.label_mess.setText("Congratulations, you have acquired {}".format(self.nm))
            QtTest.QTest.qWait(1000)
            nb_monument = nb_monument + 1
            bool = True
        return worker, nb_monument, bool

    def __str__(self):
        return self.nm

class Monument(Construction):
    def __init__(self, point_max, point_min, cost, cases, statut, name, acces, first_buy):
        super().__init__(point_max, point_min, cost, cases, statut, name, window)
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
        super().__init__(point_max, point_min, cost, cases, status, nm, window)
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

def suite(k, U1):  # fonction récursives
    '''This function calculates the quantity of resource'''

    if k <= 0:
        return 0
    elif k == 1:
        return U1
    else:
        return U1 * k + suite(k - 1, U1)

def creer_compte_rendu_joueur(end,table,nom_fichier,tour,points,food,wood,stone,pottery,cloth,arrow,skull,workers,coins,Monuments,Developments,cities):
    ''' Writes in a file the details and results of the game'''

    if end==True: # on fabrique la table
        table.field_names = ["Tour", "Points", "food","wood","stone","pottery","cloth","arrow","skulls", "workers","coins", "Monuments", "Developments", "cities"]
        with open(nom_fichier, "w") as f:
            f.write(str(table))
    else:
        table.add_row([tour, points, food,wood,stone,pottery,cloth,arrow,skull,workers,coins, ';'.join(Monuments),';'.join(Developments), ';'.join(cities)])

if __name__ == '__main__':
    app = QApplication([])
    window = FirstWindow()
    window.showFullScreen()
    app.exec_()
