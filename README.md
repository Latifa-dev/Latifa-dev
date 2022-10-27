# Script pour automatisation de création et suppression des comptes utilisateurs temporaires sur des postes connectés  dans un ou plusieurs réseaux LAN


Ce Srcript a pour les fonctionnalités suivantes: 

Scanner notre réseau pour récupérer les Adresses Ip des postes connectés à notre réseau LAN. Ensuite se connecter via ssh a ces potes à l'aide d'un compte priviligié pour exécuter notre script sur chaque poste et donne le résultat suivant:


    -chaque poste de travail portera un nom (hostname)

    -Supprimer 'ancien compte stagiaire avec son dossier principal et tous ses fichiers.

    - Création d'un nouveau utilisateur stagiaire 
    
    -Donner accés au nouveau stagiaire à un dossier partagé .

![architecture](https://user-images.githubusercontent.com/85403571/198307019-44837d59-d00d-461d-a8eb-cd858434b769.PNG)
![Capture](https://user-images.githubusercontent.com/85403571/198307109-bc86f522-10f3-48b8-9fde-f6698102a917.PNG)
![execution script](https://user-images.githubusercontent.com/85403571/198307169-d6c5e2d6-020b-47c0-ae8d-3451a1f8bc63.PNG)
