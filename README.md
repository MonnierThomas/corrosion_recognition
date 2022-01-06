# Image processing of pictures with corrosion marks

> This GitHub repository is a project made in partnership with DiAfrica, and supervised by Mines Paris. We implemented a CNN in order to identify marks of corrosion on pictures of oil platforms.

# Contexte

Notre projet d'informatique du second semestre nous a été proposé par deux industriels travaillant pour la start-up Di-Africa. Di-Africa est spécialisé notamment dans la maintenance de plateformes pétrolières sur les côtes africaines. Afin de pallier au problème de corrosion des matériaux utilisés sur les plateformes et pour prévenir les réparations et les maintenances, Di-Africa a contacté les Mines de Paris pour obtenir un moyen de détection automatique des marques de corrosion sur les matériaux.

Notre groupe (Ambroise Favre, Charlotte de Mailly Nesle, Thomas Monnier) devait remplir deux objectifs :
- traiter les images selon une classification binaire des matériaux (0 : non corrodé, 1 : corrodé)
- quantifier le degré de corrosion du matériau

Malheureusement, le second objectif a très vite été écarté au profit du premier. En effet, quantifier le degré de corrosion d'un matériau à l'aide d'algorithmes de Machine Learning semble quasi-impossible étant donné le nombre de variables entrant en jeu. La plus évidente - le degré de corrosion d'un matériau dépend de la distance à laquelle on photographie ce dernier - nous a convaincu qu'il valait mieux se concentrer sur le premier objectif.

# Etapes de résolution

**Etape 0 : réflexion**

Afin de pouvoir répondre à notre objectif, il a fallu savoir à quoi nous devions nous intéresser et répondre aux questions basiques : *A quel problème est-on confronté ? Quels algorithmes de Machine Learning pouvons-nous utiliser ? Quel est le choix le plus judicieux pour traiter les images ?*

Malgré le nombre important d'algorithmes de Machine Learning qui sont exploités dans le milieu industriel, un nous a particulièrement intéressé : le CNN (Convolution Neural Network), le réseau de neurones à convolution. Pourquoi ?

Nous avons affaire à :
- un problème de classification à deux classes (non corrodé et corrodé)
- un problème de traitement d'images 

Un algorithme supervisé comme le CNN paraît donc approprié, d'autant plus que celui-ci est connu pour sa précision (que l'on évaluera par la mesure F1) très bonne.

**Etape 1 : obtention de la base de données - Image Scraping -**

Afin de pouvoir utiliser l'algorithme CNN, il faut avoir un set de données pour pouvoir entraîner notre algorithme. Problème, Di-Africa n'a pas une base de données avec des images de corrosion et non corrosion. Il faut donc réussir à télécharger des images d'Internet afin d'avoir notre propre database constitué d'environ 2 000 images (1 000 images de corrosion, 1 000 images de non corrosion). 

Pour cela, nous avons utilisé un webdriver (présent dans Image Scraping, chromedriver.zip), le module Selenium (framework de test de navigateur web) et nous avons écrit un algorithme de téléchargement d'images par mots-clés à partir de Google Images (script_ruler.py).

A partir de là, il a fallu faire face à des images non cohérentes (ne correspondant pas aux termes non corrosion et corrosion, des schémas, etc).

**Etape 2 : Traitement des Images**

Maintenant que nous avons notre database, nous avons dû formaté et dimensionné les images de manière à les avoir toutes de la même taille et de la même qualité pour pouvoir utiliser le CNN.

Il faut aussi créer trois batchs d'images : un d'entrainement, un de validation et un de test. Globalement, la répartition est la suivante :
- 80% des images vont dans entrainement et validation, respectivement répartis en 80% et 20%
- 20% des images vont dans test

Plus tard, afin d'avoir un set de données avec plus d'images pour obtenir de meilleurs résultats, nous avons eu recours à une stratégie : symétriser nos images, ce qui nous a permis d'en avoir 4 fois plus.

Les images que nous avons utilisé sont accessibles au drive suivant : https://drive.google.com/drive/folders/1dI_T78aLbZ_ueEv7izd3NsuUUJRtyjtM?usp=sharing

**Etape 3 : Utilisation du CNN**

Après avoir codé le CNN (CNN.py) et l'avoir testé sur un test basique (reconnaissance de carrés noirs avec deux classes - carrés noirs et carrés rouges -), nous avons procédé à plusieurs tests de reconnaissance de marques de corrosion sur nos images de test. Malheureusement, les résultats n'étaient pas au rendez-vous. Les performances de l'algorithme n'étaient pas très bonnes (autour de 0.6 de précision) et certains tests classaient toutes les images de test en "corrosion".

C'est pour pallier à ces problèmes que nous avons eu recours à la symétrisation des images, à la modification de la qualité des images, à la supression d'une couche (à cause de l'overfitting).

Finalement, nous avons une précision de 0.7, ce qui n'est pas suffisant pour l'usage que veulent en faire nos encadrants. Un point positif tout de même: les résultats de notre dernier modèle montre que lorsqu'il dit qu'une image ne présente pas de traces de corrosion, on peut être sûrs qu'elle n'en présente pas, ce qui est plutôt positif et occasionne déjà un gain de temps pour les maintenances.
De part notre manque d'images et la qualité variable de celles-ci, nous ne pourrons pas obtenir de meilleurs résultats.

**Conclusion**

Notre algorithme fonctionne. Il reste simplement à avoir une base de données avec quelques millions d'images professionnelles de matériaux corrodés et non corrodés utilisés par la start up pour avoir l'espoir d'obtenir une précision avoisinant les 0.95.

**Remerciements**

Nous remercions chaleureusement Bertrand Duvivier et Christophe Lemerle pour leur soutien, leur aide hebdomadaire et la proposition de sujet qui nous a vraiment permis de découvrir et d'apprendre.

Nous vous remontons ici le lien vers notre Drive, où vous pourrez trouver plus de détails sur nos démarches: https://drive.google.com/drive/folders/1dI_T78aLbZ_ueEv7izd3NsuUUJRtyjtM?usp=sharing

