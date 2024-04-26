#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" Ce fichier contient la classe markov, à utiliser pour solutionner la problématique.
    C'est un gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers.

    Les méthodes aparaissant dans ce fichier définissent une API qui est utilisée par l'application
    de test testmarkov.py
    Les paramètres d'entrée et de sortie (Application Programming Interface, API) sont définis,
    mais le code est à écrire au complet.
    Vous pouvez ajouter toutes les méthodes et toutes les variables nécessaires au bon fonctionnement du système

    La classe markov est invoquée par la classe testmarkov (contenue dans testmarkov.py):

        - Tous les arguments requis sont présents et accessibles dans args (dans le fichier testmarkov.py)
        - Note: vous pouvez tester votre code en utilisant les commandes:
            + "python testmarkov.py"
            + "python testmarkov.py -h" (donne la liste des arguments possibles)
            + "python testmarkov.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
"""
import math
import os
import glob
import ntpath
import numpy as np
import random

class markov():
    """Classe à utiliser pour coder la solution à la problématique:

        - Contient certaines fonctions de base pour faciliter le travail (recherche des auteurs).
        - Les interfaces du code à développer sont présentes, mais tout le code est à écrire
        - En particulier, il faut compléter les fonctions suivantes:
            - find_author(oeuvre)
            - gen_text(auteur, taille, textname)
            - get_nth_element(auteur, n)
            - analyze()

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
    """

    # Le code qui suit est fourni pour vous faciliter la vie.  Il n'a pas à être modifié
    # Signes de ponctuation à retirer (compléter la liste qui ne comprend que "!" et "," au départ)
    PONC = ["!",",",".",";",":","*","-","(",")","[","]","…","_","—","–","“","”","‘","’","«","»","/","'","?","<",">","@","#","$","%","^","&","`","~","|","--","..."]
    #PONC_TO_SPACE = ["'","-","\n\n","\n","    ","   ","  "]

    def set_ponc(self, value):
        """Détermine si les signes de ponctuation sont conservés (True) ou éliminés (False)

        Args:
            value (boolean) : Conserve la ponctuation (Vrai) ou élimine la ponctuation (Faux)

        Returns:
            void : ne fait qu'assigner la valeur du champs keep_ponc
        """
        self.keep_ponc = value

    def print_ponc(self):
        print("Signes de ponctuation à retirer: ", self.PONC)

    def set_auteurs(self):
        """Obtient la liste des auteurs, à partir du répertoire qui les contient tous

        Note: le champs self.rep_aut doit être prédéfini:
            - Par défaut, il contient le répertoire d'exécution du script
            - Peut être redéfini par la méthode set_aut_dir

        Returns:
            void : ne fait qu'obtenir la liste des répertoires d'auteurs et modifier la liste self.auteurs
        """
        files = self.rep_aut + "/*"
        full_path_auteurs = glob.glob(files)
        for auteur in full_path_auteurs:
            self.auteurs.append(ntpath.basename(auteur))
        return

    def get_aut_files(self, auteur):
        """Obtient la liste des fichiers (avec le chemin complet) des oeuvres d'un auteur

        Args:
            auteur (string): le nom de l'auteur dont on veut obtenir la liste des oeuvres

        Returns:
            oeuvres (Liste[string]): liste des oeuvres (avec le chemin complet pour y accéder)
        """
        auteur_dir = self.rep_aut + "/" + auteur + "/*"
        oeuvres = glob.glob(auteur_dir)
        return oeuvres

    def set_aut_dir(self, aut_dir):
        """Définit le nom du répertoire qui contient l'ensemble des répertoires d'auteurs

        Note: L'appel à cette méthode extrait la liste des répertoires d'auteurs et les ajoute à self.auteurs

        Args (string) : Nom du répertoire en question (peut être absolu ou bien relatif au répertoire d'exécution)

        Returns:
            void : ne fait que définir le nom du répertoire qui contient les répertoires d'auteurs
        """
        cwd = os.getcwd()
        if os.path.isabs(aut_dir):
            self.rep_aut = aut_dir
        else:
            self.rep_aut = os.path.join(cwd, aut_dir)

        self.rep_aut = os.path.normpath(self.rep_aut)
        self.set_auteurs()
        return


    def set_ngram(self, ngram):
        """Indique que l'analyse et la génération de texte se fera avec des n-grammes de taille ngram

        Args:
            ngram (int) : Indique la taille des n-grammes (1, 2, 3, ...)

        Returns:
            void : ne fait que mettre à jour le champs ngram
        """
        self.ngram = ngram

    def __init__(self):
        super().__init__()
        """Initialize l'objet de type markov lorsqu'il est créé

        Args:
            aucun: Utilise simplement les informations fournies dans l'objet Markov_config

        Returns:
            void : ne fait qu'initialiser l'objet de type markov
        """

        # Initialisation des champs nécessaires aux fonctions fournies
        self.keep_ponc = True
        self.rep_aut = os.getcwd()
        self.auteurs = []
        self.ngram = 1

        # Au besoin, ajouter votre code d'initialisation de l'objet de type markov lors de sa création

        return

    # Ajouter les structures de données et les fonctions nécessaires à l'analyse des textes,
    #   la production de textes aléatoires, la détection d'oeuvres inconnues,
    #   l'identification des n-ièmes mots les plus fréquents
    #
    # If faut coder les fonctions find_author(), gen_text(), get_nth_element() et analyse()
    # La fonction analyse() est appelée en premier par testmarkov.py
    # Ensuite, selon ce qui est demandé, les fonctions find_author(), gen_text() ou get_nth_element() sont appelées

    def find_author(self, oeuvre):
        """Après analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximité (un nombre entre 0 et 1) de l'oeuvre inconnue avec les écrits de chacun d'entre eux

        Args:
            oeuvre (string): Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns:
            resultats (Liste[(string,float)]) : Liste de tuples (auteurs, niveau de proximité), où la proximité est un nombre entre 0 et 1)
        """

        #resultats = [("balzac", 0.1234), ("voltaire", 0.1123)]   # Exemple du format des sorties
        resultats = [] #On fait l'analyse du texte inconnu
        with open(oeuvre, "r", encoding = "utf8") as file:
            unknown_text = file.read()
            for p in self.PONC:
                unknown_text = unknown_text.replace(p, " ")
            unknown_text = unknown_text.lower().split()
            unknown_word_list = []
            for word in unknown_text:
                if len(word) > 2:
                    unknown_word_list.append(word)

        #calcul du vecteur de frequence de l'oeuvre inconnue
        unknown_freq_dict = {}
        for i in range(len(unknown_word_list) - (self.ngram - 1)):
            unknown_ngramme = " ".join(unknown_word_list[i:i + self.ngram])
            if unknown_ngramme in unknown_freq_dict:
                unknown_freq_dict[unknown_ngramme] += 1
            else:
                unknown_freq_dict[unknown_ngramme] = 1

        unknown_norme = math.sqrt(sum(unknown_freq_dict[unknown_ngramme]**2 for unknown_ngramme in unknown_freq_dict))

        for auteur in self.freq_dict.keys():
            freq_dict_auteur = self.freq_dict[auteur]
            norm_auteur = math.sqrt(sum(freq_dict_auteur[unknown_ngramme]**2 for unknown_ngramme in freq_dict_auteur))
            dot_product = sum(freq_dict_auteur.get(unknown_ngramme, 0) * unknown_freq_dict.get(unknown_ngramme, 0) for unknown_ngramme in set(freq_dict_auteur) | set(unknown_freq_dict))
            normale = dot_product / (norm_auteur * unknown_norme)
            resultats.append((auteur, normale))
            #print("Norme: ", str(norm_auteur))
            #print("Norme: ", str(unknown_norme))


        # Ajouter votre code pour déterminer la proximité du fichier passé en paramètre avec chacun des auteurs
        # Retourner la liste des auteurs, chacun avec sa proximité au fichier inconnu
        # Plus la proximité est grande, plus proche l'oeuvre inconnue est des autres écrits d'un auteur
        #   Le produit scalaire entre le vecteur représentant les oeuvres d'un auteur
        #       et celui associé au texte inconnu pourrait s'avérer intéressant...
        #   Le produit scalaire devrait être normalisé avec la taille du vecteur associé au texte inconnu:
        #   proximité = (A . B) / (|A| |B|)   où A est le vecteur du texte inconnu et B est celui d'un auteur,
        #           . est le produit scalaire, et |X| est la norme (longueur) du vecteur X

        return resultats

    def gen_text(self, auteur, taille, textname):
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args:
            auteur (string): Nom de l'auteur à utiliser
            taille (int): Taille du texte à générer
            textname (string): Nom du fichier texte à générer.

        Returns:
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """

        # Créer une liste de n-grammes et de probabilités correspondantes
        ngrams = []
        probs = []
        for ngram, count in self.freq_dict[auteur].items():
            ngrams.append(ngram)
            probs.append(count)
        probs = np.array(probs)
        probs = probs.astype(float) / probs.sum()

        # Générer le texte en sélectionnant chaque n-gramme avec sa probabilité correspondante
        file = open(textname, "w+")
        ngram_index = np.random.choice(len(ngrams), size=taille, p=probs)
        for i in range(taille):
            if i < taille - 1:
                file.write(ngrams[ngram_index[i]] + " ")
            else:
                file.write(ngrams[ngram_index[i]])
        file.close()

        return

    def get_nth_element(self, auteur, n):
        """Après analyse des textes d'auteurs connus, retourner le n-ième plus fréquent n-gramme de l'auteur indiqué

        Args:
            auteur (string): Nom de l'auteur à utiliser
            n (int): Indice du n-gramme à retourner

        Returns:
            ngram (List[Liste[string]]) : Liste de liste de mots composant le n-gramme recherché (il est possible qu'il y ait plus d'un n-gramme au même rang)
        """

        dict_trie = dict(sorted(self.freq_dict[auteur].items(), key=lambda x: x[1], reverse=True))
        list_ngramme = list(dict_trie.keys())
        dict_ngramme_listed = {}  # Ce dictionnaire va utiliser la frequence comme cle et une liste de ngrammes comme
        # valeur
        for index, freq in enumerate(dict_trie.values()):
            if freq in dict_ngramme_listed.keys():
                dict_ngramme_listed[freq].append(list_ngramme[index])
            else:
                dict_ngramme_listed.update({freq: [list_ngramme[index]]})
        # print(dict_ngramme_listed)
        # print("-----------------")
        for index, freq in enumerate(dict_ngramme_listed.keys()):
            if index == n - 1:
                return dict_ngramme_listed[freq]


    def analyze(self):
        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args:
            void: toute l'information est contenue dans l'objet markov

        Returns:
            void : ne retourne rien, toute l'information extraite est conservée dans des strutures internes
        """

        # Ajouter votre code ici pour traiter l'ensemble des oeuvres de l'ensemble des auteurs
        # Pour l'analyse:  faire le calcul des fréquences de n-grammes pour l'ensemble des oeuvres
        #   d'un certain auteur, à la fois par oeuvre et aussi sans distinction des oeuvres individuelles,
        #       et recommencer ce calcul pour chacun des auteurs
        #   En procédant ainsi, les oeuvres comprenant plus de mots auront un impact plus grand sur
        #   les statistiques globales d'un auteur
        #initialisation du dictionnaire
        self.freq_dict = {}
        for auteur in self.auteurs:
            self.freq_dict[auteur] = {}
        #Pourcours les oeuvres de tous les auteurs
        nb_mots = 0
        for auteur in self.auteurs:
            file_name = auteur + " Occurenc_mots.txt"
            f = open(file_name, "w+", encoding = "utf8")
            for oeuvre in self.get_aut_files(auteur):
                with open(oeuvre, "r", encoding='utf8') as file:
                    text = file.read().lower()
                    for p in self.PONC:
                        text = text.replace(p, " ")
                    text = text.split()
                    word_list = []
                    for word in text:
                        if len(word) > 2:
                            nb_mots += 1
                            word_list.append(word)
                    #calcul des frequences de n-gramme
                    for i in range(len(word_list)-(self.ngram - 1)):
                        ngramme = " ".join(word_list[i:i+self.ngram])
                        if ngramme in self.freq_dict[auteur]:
                            self.freq_dict[auteur][ngramme] += 1
                        else:
                            self.freq_dict[auteur][ngramme] = 1

            for word, ngramme in self.freq_dict[auteur].items():
                f.write(str(word + " " + str(ngramme) + '\n'))

        #print(gen_text(self, Balzac, 10, "Yoyoyo"))
        #print(self.freq_dict['Balzac'])
        print(nb_mots)
        return

    


"""caca = markov()
filename = "texte problématique\TextesPourEtudiants\Verne\Jules Verne - Autour de la lune.txt"
unigrame = {}
caca.analyze()"""

# Il serait possible de considérer chacune des oeuvres d'un auteur comme ayant un poids identique.
#   Pour ce faire, il faudrait faire les calculs de fréquence pour chacune des oeuvres
#       de façon indépendante, pour ensuite les normaliser (diviser chaque vecteur par sa norme),
#       avant des les additionner pour obtenir le vecteur global d'un auteur
#   De cette façon, les mots d'un court poème auraient une importance beaucoup plus grande que
#   les mots d'une très longue oeuvre du même auteur. Ce n'est PAS ce qui vous est demandé ici.