# di-africa
Projet Informatique Mines-Paristech

# Contexte

Notre projet d'informatique du second semestre nous a été proposé par deux industriels travaillant pour la start-up Di-Africa. Di-Africa est spécialisé notamment dans la maintenance de plateformes pétrolières sur les côtes africaines. Afin de palier au problème de corrosion des matériaux utilisés sur les plateformes et pour prévenir les réparations et les maintenances, Di-Africa a contacté les Mines de Paris afin d'écrire un algorithme permettant de traiter les images avec marques de corrosion.

Notre groupe (Ambroise Favre, Charlotte de Mailly Nesle, Thomas Monnier) devait remplir deux objectifs :
- traiter les images selon une classification binaire des matériaux (0 : non corrodé, 1 : corrodé)
- quantifier le degré de corrosion du matériau

Malheureusement, le second objectif a très vite été écarté au profit du premier. En effet, quantifier le degré de corrosion d'un matériau à l'aide d'algorithmes de Machine Learning semble quasi-impossible étant donné le nombre de variables entrant en jeu. La plus évidente - le degré de corrosion d'un matériau dépend de la distance à laquelle on photographie ce dernier - nous a convaincu qu'il valait mieux se concentrer sur le premier objectif.

# Etapes de résolution

**Etape 0 : réflexion**

Afin de pouvoir répondre à notre objectif, il a fallu savoir à quoi nous devions nous intéresser et répondre aux questions basiques : *A quel problème est-on confronté ? Quels algorithmes de Machine Learning pouvons-nous utiliser ? Quel est le choix le plus judicieux pour traiter les images ?*

Malgré le nombre important d'algorithmes de Machine Learning qui sont exploités dans le milieu industriel, un nous a particulièrement intéressé : le CNN (Convolution Neural Network), le réseau de neurons à convolution.
