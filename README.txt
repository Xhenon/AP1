floconHeavy.py:
floconHeavy.py permet d'observer la croissance d'un flocon �tape par �tape � l'aide d'une fenetre graphique et permet �galement d'exporter le r�sultat sous forme de fichier .png
Lancer le programme en double cliquant dessus.
Boutons 'Suivant' et 'Suivant ++' pour g�n�rer les �tapes suivantes du flocon
Boutons 'Precedent' et 'Precedent ++' pour afficher les �tapes pr�c�dentes du flocon
Bouton 'Exporter' pour exporter le flocon actuel sous forme de fichier .png nomm� 'image.png'
Bouton 'Rafraichir' pour forcer la fenetre � actualiser tous les polygones (pas utile sauf en cas d'erreur d'affichage)

floconCommand.py:
floconCommand.py permet de g�n�rer des images d'un flocon sans passer par une fenetre graphique. On peut choisir pr�ciser les constantes initiales en param�tre ou non (si non, elles sont choisies par le programme)
A lancer de pr�f�rence via un terminal de commande. (Se placer dans le m�me dossier que floconCommand.py)
Executer l'instruction:
python floconCommand.py (+plus les param�tres que l'on souhaite rajouter)

Entrer l'instruction suivante pour plus de d�tails sur les param�tres:
python floconCommand.py help


startup.py:
startup.py permet de g�n�rer un fichier texte utilisable par create.py pour g�n�rer des flocons.
A lancer de pr�f�rence via un terminal de commande. (Se placer dans le m�me dossier que startup.py)
Executer l'instruction:
python startup.py (+plus les param�tres que l'on souhaite rajouter)

Entrer l'instruction suivante pour plus de d�tails sur les param�tres:
python startup.py help

create.py:
create.py permet de lancer plusieurs instances de floconCommande.py
A lancer de pr�f�rence via un terminal de commande. (Se placer dans le m�me dossier que create.py)
Executer l'instruction:
python create.py nomdufichier.txt
avec nomdufichier.txt le nom du fichier texte cr�� par startup.py

