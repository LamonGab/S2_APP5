#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Programme python pour l'évaluation du code de détection des auteurs et de génération de textes
#
#
#  Copyright 2018-2023 F. Mailhot et Université de Sherbrooke
#

import argparse
import importlib
import os.path
import sys



class TestMarkov():
    """Classe à utiliser pour valider la résolution de la problématique :

        - Contient tout le nécessaire pour tester la problématique.

    Pour valider la solution de la problématique, effectuer :
        - python testmarkov.py -help
            + Indique tous les arguments et options disponibles

    Copyright 2018-2023, F. Mailhot et Université de Sherbrooke
    """

    # Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
    def print_verbose(self):
        """Mode verbose, imprime l'ensemble des paramètres utilisés pour ce test:
            - Valeur des paramètres par défaut s'ils n'ont pas été modifiés sur la ligne de commande
            - Ensemble des tests demandés

        Returns :
            void : Ne fait qu'imprimer les valeurs contenues dans self
        """
        if self.args.v:
            print("Mode verbose:")

            if self.args.f:
                print("Fichier inconnu à étudier: " + self.args.f)

            print("Calcul avec des " + str(self.args.m) + "-grammes")
            if self.args.F:
                print(str(self.args.F) + "e mot (ou digramme) le plus fréquent sera calculé")

            if self.args.a:
                print("Auteur étudié: " + self.args.a)

            if self.args.noPonc:
                print("Retirer les signes de ponctuation")
#                self.markov.print_ponc()
            else:
                print("Conserver les signes de ponctuation")

            if self.args.G:
                print("Génération d'un texte de " + str(self.args.G) + " mots, pour l'auteur: ", self.auteur)
                print("Le nom du fichier généré sera: " + self.get_gen_file_name())

            print("Calcul avec les auteurs du répertoire: " + self.args.d)
            print("Liste des auteurs: ")
            for a in self.auteurs:
                aut = a.split("/")
                print("    " + aut[-1])

            print("")
        return

    def get_gen_file_name(self):
        name = self.gen_basename
        if self.g_cip :
            name = name + self.g_sep + self.cip
        if self.g_aut :
            name = name + self.g_sep + self.auteur
        if self.g_ext :
            name = name + self.g_ext

        return name

    def setup_and_parse_cli(self):
        """Utilise le module argparse pour :
            - Enregistrer les commandes à reconnaître
            - Lire la ligne de commande et créer le champ self.args qui récupère la structure produite

        Returns :
            void : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """
        parser = argparse.ArgumentParser(prog='markov_CIP1_CIP2.py')
        parser.add_argument('-d', default='./TextesPourEtudiants',
                            help='Repertoire contenant les sous-repertoires des auteurs (./TextesPourEtudiants par défaut)')
        parser.add_argument('-a', help='Résultats à produire pour cet auteur spécifique')
        parser.add_argument('-f', help='Fichier inconnu pour lequel on recherche un auteur')
        parser.add_argument('-m', default=1, type=int, choices=range(1, 20),
                            help='Mode (1 ou 2 ou 3 ou ... 20) - unigrammes ou digrammes ou trigrammes ou ...')
        parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou n-gramme) a imprimer')
        parser.add_argument('-G', default=0, type=int, help='Taille du texte a generer')
        parser.add_argument('-g', default='Gen_text', help='Nom de base du fichier de texte à générer')
        parser.add_argument('-g_ext', default='.txt', help='Extension utilisée pour le fichier généré, .txt par défaut')
        parser.add_argument('-g_nocip', action='store_true', help='Ne pas utiliser les CIPs dans le nom du fichier généré')
        parser.add_argument('-g_noaut', action='store_true', help='Ne pas utiliser le nom de l\'auteur dans le nom du fichier généré')
        parser.add_argument('-g_sep', default="_", help='Utiliser cette chaine de caractères comme séparateur dans le nom de fichier généreé')
        parser.add_argument('-g_reformat', help='Indique que le reformattage doit être utilisé dans le texte généré')
        parser.add_argument('-v', action='store_true', help='Mode verbose')
        parser.add_argument('-noPonc', action='store_true', help='Retirer la ponctuation')
        parser.add_argument('-rep_code', default='.', help='Répertoire contenant la liste des CIPs et le code markov_CIP1_CIP2.py')
        parser.add_argument('-recursion', help='Récursion maximale permise (par défaut, 1000)')
        parser.add_argument('-r1', help='Retrait des mots de 1 caractère')
        parser.add_argument('-r2', help='Retrait des mots de 2 caractères')
        parser.add_argument('-golden', help='Compare les résultats avec la version \'golden\' indiquée par ce paramètre')
        parser.add_argument('-fichier_res', help='Tous les prints seront faits dans ce fichier')
        parser.add_argument('-dir_res', help='Tous les résultats seront ajoutés dans ce répertoire (sous le répertoire courant)')
        self.parser = parser
        self.args = parser.parse_args()

        if self.args.d:
            self.dir = self.args.d
        if self.args.noPonc:
            self.keep_punc = False
        if self.args.m:
            self.ngram = self.args.m
        if self.args.G:
            self.gen_size = self.args.G
            if self.gen_size > 0:
                self.gen_text = True
                if self.args.g:
                    self.gen_basename = self.args.g
        if self.args.a:
            self.auteur = self.args.a
        if self.args.rep_code:
            self.rep_code = self.args.rep_code
        if self.args.g_ext:
            self.g_ext = self.args.g_ext
        if self.args.g_nocip:
            self.g_cip = False
        if self.args.g_noaut:
            self.g_aut = False
        if self.args.g_sep:
            self.g_sep = self.args.g_sep
        if self.args.f :
            self.oeuvre = self.args.f
            self.find_author = True
        if self.args.F:
            self.do_get_nth_ngram = True
            self.nth_ngram = self.args.F
        if self.args.r1:
            self.remove_word_1 = True
        if self.args.r2:
            self.remove_word_2 = True

        if self.args.fichier_res:
            # https://stackoverflow.com/questions/5104957/how-do-i-create-a-file-at-a-specific-path
            cur_path = os.path.dirname(__file__)
            if self.args.dir_res:
                dir_res_path = os.path.relpath(self.args.dir_res, cur_path)
                try:    # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
                    os.mkdir(dir_res_path)
                except FileExistsError:
                    pass
            else:
                dir_res_path = cur_path
            output_file_path = os.path.join(dir_res_path,self.args.fichier_res)
            # Voir: https://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python
            # et: https://stackoverflow.com/questions/3597480/how-to-make-python-3-print-utf8
            sys.stdout = open(output_file_path, 'w', encoding='UTF-8', buffering=1)
        return

    def list_cips(self):
        """Lit le fichier etudiants.txt, trouve les CIPs, et retourne la liste
           Le CIP est obtenu du fichier etudiants.txt, dans le répertoire courant
            ou tel qu'indiqué en paramètre (option -rep_code)

        Returns:
            void: void: Au retour, tous les cips sont inclus dans la liste self.cips
        """
        cip_file = self.rep_code + "/etudiants.txt"
        cip_list = open(cip_file,"r")
        lines = cip_list.readlines()
        for line in lines:
            for cip in line.split():
                self.cips.append(cip)

        return

    def import_markov_cip(self, import_cip):
        """Importe le fichier markov_CIP1_CIP2.py, où "CIP1_CIP2" est passé dans le paramètre cip

        Args :
            import_cip (string): Contient "CIP1_CIP2", les cips pour le code à tester

        Returns :
            void : Au retour, le module markov_CIP1_CIP2 est importé et remplace le précédent
        """

        if "init_module" in self.init_modules:
            # Deuxième appel (ou subséquents) : enlever tous les modules supplémentaires
            for m in sys.modules.keys():
                if m not in self.init_modules:
                    del(sys.modules[m])
        else:
            # Premier appel : identifier tous les modules déjà présents
            self.init_modules = sys.modules.keys()

        self.cip = import_cip
        markov_name = "markov_" + import_cip
        self.markov_module = importlib.import_module(markov_name)
#        getattr(self.markov_module, "markov")

        return

    def check_and_setup_golden(self):
        if self.args.golden:
            self.golden_module = importlib.import_module(self.args.golden)
        return

    def __init__(self):
        """Constructeur pour la classe testmarkov.  Initialisation de l'ensemble des éléments requis

        Args :
            void : Le constructeur lit la ligne de commande et ajuste l'état de l'objet testmarkov en conséquence

        Returns :
            void : Au retour, la nouvelle instance de test est prête à être utilisée
        """
        self.dir = "."
        self.ngram = 1
        self.keep_punc = True
        self.gen_text = False
        self.gen_size = 0
        self.gen_basename = "Gen_text"
        self.cip = ""
        self.markov_module = ""
        self.golden_module = ""
        self.g_ext = ".txt"
        self.g_cip = True
        self.g_aut = True
        self.g_sep = '_'
        self.rep_code = '.'
        self.auteur = ""
        self.oeuvre = ""
        self.find_author = False
        self.tests = []
        self.do_analyze = False
        self.do_get_nth_ngram = False
        self.remove_word_1 = False
        self.remove_word_2 = False
        self.setup_and_parse_cli()
        self.check_and_setup_golden()

        self.cips = []
        self.list_cips()
        self.init_modules = {}


if __name__ == "__main__":
    tm = TestMarkov()       # Initialisation de l'instance de test

    tm.something_to_do = tm.gen_text | tm.find_author | tm.do_get_nth_ngram
    if not tm.something_to_do:
        print('Aucune action à effectuer. Utiliser un paramètre pour:')
        print('\t - Générer un texte aléatoire')
        print('\t - Trouver l\'auteur d\'un texte inconnu')
        print('\t - Trouver le k-ieme n-gramme le plus fréquent d\'un auteur')
        print('')
        tm.parser.print_help()
        exit()

    if tm.args.recursion :
        sys.setrecursionlimit(int(tm.args.recursion))
        print("Récursion maximale: ", sys.getrecursionlimit())

    if tm.oeuvre:
        try:
            symlink = os.readlink(tm.oeuvre)  # https://www.tutorialspoint.com/python/os_readlink.htm
            print(f'Oeuvre inconnue: {tm.oeuvre} avec lien symbolique vers: {symlink}')
        except:
            print('L\'oeuvre ', tm.oeuvre, ' n\'est pas un lien symbolique')

    for cip in tm.cips:   # Permet de tester le code d'une ou plusieurs équipes, à tour de rôle
        tm.import_markov_cip(cip)
        tm.markov = tm.markov_module.markov()

        # Ajout de l'information nécessaire dans l'instance à tester de la classe markov sous étude:
        #   Utilisation de la ponctuation (ou non), taille des n-grammes, répertoire des auteurs
        if tm.args.noPonc :
            tm.markov.set_ponc(False)
        else:
            tm.markov.set_ponc(True)

        tm.markov.set_ngram(tm.ngram)
        tm.markov.set_aut_dir(tm.dir)

        tm.auteurs = tm.markov.auteurs
        tm.print_verbose()  # Imprime l'état de l'instance (si le mode verbose a été utilisé sur la ligne de commande)

        tm.markov.analyze()

        if tm.gen_text:
            filename = tm.get_gen_file_name()
            tm.markov.gen_text(tm.auteur, tm.gen_size, filename)

        if tm.find_author:
            tm.analysis_result = tm.markov.find_author(tm.oeuvre)

            print(f'cip: {cip} - Fréquences pour l\'oeuvre "{tm.oeuvre}": ', end='')
            # https://stackoverflow.com/questions/493386/how-to-print-without-a-newline-or-space
            for item in tm.analysis_result:
                print(f'{item[0]}:{item[1]:.4f} ', end='')
            print('')

        if tm.do_get_nth_ngram:
            if tm.auteur == "":
                print("Pas d'auteur indiqué: impossible de donner le n-ième ngramme.  Utiliser -a nom_de_l_auteur")
                break
            nth_ngram = tm.markov.get_nth_element(tm.auteur, tm.nth_ngram)
            print(f'cip: {cip} - Auteur: {tm.auteur}, '
                  f'{tm.nth_ngram}e n-gramme de {tm.ngram} mot{"s"[:tm.ngram>1]}: {nth_ngram}')

    if tm.args.fichier_res:  # stdout a été redirigé vers un fichier ; le fermer pour ne rien perdre
        sys.stdout.close()

