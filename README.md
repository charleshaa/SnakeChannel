# SnakeChannel
Reseaux TP1

Le script scriptTest.py permet de tester la connexion et l'envoi de message ainsi que le comportement de la connexion avec un réseau stressé.

snackChanel permet les fonctions suivantes:

void connect((ip, port))
Demande un connection à l'ip/port précisé.

void send(data, (ip, (port, ip)))
Envoi des data à l'ip/port précisé (sinon connecté, les data sont perdu)

data, addr receive(time)
fonction bloquante, qui attend la réception de data. Elle sort les data ainsi que l'ip/port émettrice.
L'argument time peut être renseigné. Après time seconde, la fonction retour null et débloque.


Note:
    En mode bidirectionnel, il faut impérativement utiliser send avec une ip et un port renseigné!
    Ainsi un client peut se connecter et accepter des connections.