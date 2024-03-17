# Projet Processus Métier

## Objectif
Le projet illustre de manière détaillée le processus de conception et de développement d'un système innovant de traitement de commandes asynchrone, élaboré en utilisant FastAPI et RabbitMQ. Ce projet vise à établir une architecture composée de deux piliers fondamentaux : un processus client, destiné à l'initiation et à la soumission de commandes, et un processus fournisseur, dédié à la gestion intégrale des demandes, comprenant la génération de devis ainsi que la confirmation des commandes.
## Modélisation

![Schéma du Processus de Traitement des Commandes](https://github.com/alhajnadine/Projet_ProcMetier/blob/master/schema.png?raw=true)

Dans notre modèle BPMN (Business Process Model and Notation), nous décrivons le flux du processus de traitement des commandes, mettant en évidence les interactions entre le client et le fournisseur, ainsi que les décisions prises lors du traitement de chaque commande.

- **Événement de départ:**
  Le processus commence lorsque le client passe une commande. C'est l'événement déclencheur qui initie le processus de traitement des commandes.

- **Tâche de Traitement de Commande:**
  Une fois que la commande est passée, elle est envoyée au fournisseur pour traitement. Le fournisseur reçoit la commande et commence à la traiter.

- **Validation de la Commande par le Fournisseur:**
  Le fournisseur doit décider de la validité de la commande. S'il la valide, il la confirme et envoie une confirmation de commande au client. Sinon, le processus se termine.

- **Génération du Devis:**
  Une fois la commande confirmée, le fournisseur génère un devis pour la commande confirmée à partir des détails fournis.

- **Confirmation du Devis par le Client:**
  Une fois que le devis est reçu,Le client examine le devis et décide de le valider ou non. Si le client ne valide pas le devis, le processus se termine. Si le client confirme le devis, le fournisseur reçoit une confirmation du client.

Ce modèle offre une vue détaillée du flux de traitement des commandes, des interactions entre les parties prenantes et des décisions prises à chaque étape du processus.

## Execution du code
Connection avec RabbitMQ <br>
Connection avec Base de données <br>
Activer l'environment: ***venv\Scripts\activate*** <br>
Executer code client: ***python client.py*** <br>
Executer code fournisseur: ***python fournisseur.py***<br>
