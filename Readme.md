# 'watcher' de liens en 150 lignes

Exemple simple d'un watcher de liens. Il manque des fonctions comme des abonnements 
qui pourraient envoyer un mail si une page change avec un maxratio < .80.

## Exemple utilisation


### Je veux watch une url

curl http://api.watcher.link/new/?url=http://classik.forumactif.com/f7-concerts

```
{
  "page": {
    "_id": {
      "$oid": "55cd19651d4aba7ea02889e1"
    }, 
    "baseurl": "http://classik.forumactif.com/f7-concerts", 
    "diffs": [], 
    "maxratio": 0.97, 
    "name": "Concerts", 
    "snaps": []
  }
}
```

### Je fais un snap avec l'id de la page 55cd19651d4aba7ea02889e1

curl http://api.watcher.link/snap/55cd19651d4aba7ea02889e1/

```
{
  "page": {
    "_id": {
      "$oid": "55cd19651d4aba7ea02889e1"
    }, 
    "baseurl": "http://classik.forumactif.com/f7-concerts", 
    "diffs": [], 
    "maxratio": 0.97, 
    "name": "Concerts", 
    "snaps": [
      {
        "$oid": "55cd19661d4aba7ea02889e2"
      }, 
      {
        "$oid": "55cd19671d4aba7ea02889e3"
      }, 
      {
        "$oid": "55cd19741d4aba7ea02889e4"
      }
    ]
  }
}
```

J'ai 3 snap 55cd19661d4aba7ea02889e2, 55cd19671d4aba7ea02889e3 et 55cd19741d4aba7ea02889e4

### get le screen d'un snap (png)

curl http://api.watcher.link/screen/55cd19741d4aba7ea02889e4/

### Voir le diff

curl http://api.watcher.link/diff/55cd19651d4aba7ea02889e1/

```
{
  "diff": {
    "delete": [], 
    "fst": {
      "dthr": "Fri, 14 Aug 2015 00:12:30 GMT", 
      "id": "55cd164e1d4aba7e10fb82b5"
    }, 
    "insert": [
      "BEGIN cookies_alert  END cookies_alert"
    ], 
    "ratio": 0.9980487804878049, 
    "replace": [], 
    "snd": {
      "dthr": "Fri, 14 Aug 2015 00:12:18 GMT", 
      "id": "55cd16421d4aba7e10fb82b4"
    }
  }
}
```

Ici, un ratio, de 0.99, la page n'a pas bcp changée. Il y a eu qu'un inster 'BEGIN cookies ...' qui ne sert à rien. 
Un 'vrais' changement à un ratio de moins de 0.98 0.97. Il faut faire des tests sur votre page pour voir le bon ratio.

### Voir le diff html

curl http://api.watcher.link/diffhtml/55cd19651d4aba7ea02889e1/

### voir un snap 

curl http://api.watcher.link/getsnap/55cd19671d4aba7ea02889e3/


## Installation

Voir le provisioning du Vagrantfile

```
apt-get install phantomjs python-dev
```

```
pip install -r requirements.txt 
```