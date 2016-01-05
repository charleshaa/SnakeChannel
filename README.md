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

# SnakePost

void send(data, addr)
    Permet d'envoyer un message non sécurisé. Si ack en attente, piggybacking.

int sendSecure(data, addr)
    Permet de mettre un message en attente d'envoi sécurisé.
    Si la fille d'attente est pleine, retourne 1, si non retourne 0

void sendAllSecureQueued()
    Fonction privé qui permet de faire un envoye sécurisé de tout les premieres messages de chaque liste de fille d'attente.

data listen()
    Permet la réception de message, gère la récéption de ack et de seq. Retourne des data quand il y en a.

void close()
    Envoi le dernier ack en attente.