floconHeavy.py:
floconHeavy.py permet d'observer la croissance d'un flocon étape par étape à l'aide d'une fenetre graphique et permet également d'exporter le résultat sous forme de fichier .png
Lancer le programme en double cliquant dessus.
Boutons 'Suivant' et 'Suivant ++' pour générer les étapes suivantes du flocon
Boutons 'Precedent' et 'Precedent ++' pour afficher les étapes précédentes du flocon
Bouton 'Exporter' pour exporter le flocon actuel sous forme de fichier .png nommé 'image.png'
Bouton 'Rafraichir' pour forcer la fenetre à actualiser tous les polygones (pas utile sauf en cas d'erreur d'affichage)

floconCommand.py:
floconCommand.py permet de générer des images d'un flocon sans passer par une fenetre graphique. On peut choisir préciser les constantes initiales en paramètre ou non (si non, elles sont choisies par le programme)
A lancer de préférence via un terminal de commande. (Se placer dans le même dossier que floconCommand.py)
Executer l'instruction:
python floconCommand.py (+plus les paramètres que l'on souhaite rajouter)

Entrer l'instruction suivante pour plus de détails sur les paramètres:
python floconCommand.py help


startup.py:
startup.py permet de générer un fichier texte utilisable par create.py pour générer des flocons.
A lancer de préférence via un terminal de commande. (Se placer dans le même dossier que startup.py)
Executer l'instruction:
python startup.py (+plus les paramètres que l'on souhaite rajouter)

Entrer l'instruction suivante pour plus de détails sur les paramètres:
python startup.py help

create.py:
create.py permet de lancer plusieurs instances de floconCommande.py
A lancer de préférence via un terminal de commande. (Se placer dans le même dossier que create.py)
Executer l'instruction:
python create.py nomdufichier.txt
avec nomdufichier.txt le nom du fichier texte créé par startup.py

