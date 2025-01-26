# Explication du Processus de Build et Déploiement avec Docker

L'application "Filmy" est divisée en deux dépôts distincts : un pour l'application principale et un pour l'API. Pour simplifier le déploiement avec Docker et éviter de devoir gérer plusieurs commandes pour chaque dépôt, nous avons décidé de construire les images Docker nous-mêmes. Cela nous permet d'utiliser ces images directement dans notre compose, ce qui simplifie grandement la gestion de l'ensemble du projet.

## Pourquoi ne pas cloner les dépôts dans le Dockerfile ?

Nous aurions pu choisir d'ajouter une étape dans notre `Dockerfile` pour cloner les dépôts directement et les builder à chaque fois. Cependant, cette approche aurait entraîné une complexité supplémentaire et des étapes inutiles dans le processus de build. Au lieu de cela, nous avons décidé de construire les images localement une seule fois, afin de les utiliser plus efficacement dans notre [compose](./compose.yml).

## Développement local avec Docker

Afin de faciliter le développement local, nous avons créé des fichiers [compose](../compose.yml) et [Dockerfile](../Dockerfile) spécifiques à l'environnement de développement. Ces fichiers permettent de faire tourner l'application et l'API sur votre machine simplement.

## Build des images

Les images Docker ont été construites pour deux architectures différentes : `amd64` et `arm64` (pour les Macs Apple équipés des puces M1,2,3, par exemple). Cela permet d'assurer que l'application fonctionne sur diverses plateformes sans nécessiter d'adaptations supplémentaires. Ces images sont disponibles sur Docker Hub et peuvent être utilisées dans notre compose avec le tag `latest` (détecte automatiquement l'architecture) afin de déployer l'application rapidement sans avoir à rebuild les images à chaque fois.
Les images sont disponibles sur le Docker Hub :
- [ollopic/filmy](https://hub.docker.com/repository/docker/ollopic/filmy/general)
- [ollopic/filmy-api](https://hub.docker.com/repository/docker/ollopic/filmy-api/general)

Les commandes de build utilisées sont les suivantes :
```bash
docker buildx build --platform linux/amd64,linux/arm64 -f Dockerfile.prod . -t ollopic/filmy-api:latest --push
```