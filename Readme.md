# POC watcher de liens

Exemple simple d'un watcher de liens. Il manque des fonctions comme des abonnements 
qui pourraient envoyer un mail si une page change avec un maxratio < 0.80.

Si un ratio, de 0.99, la page n'a pas bcp changée. Cela peut être un js dynamique par exemple.
Un 'vrais' changement à un ratio de moins de 0.98/0.97. Si le ratio est à 1 alors la page n'a pas changée.
Il faut faire des tests sur votre page pour avoir le bon ratio.

## TODO

- Mettre du redis (celery) pour la creation d'un watcher, les snaps ...

## Documentation

### Create page

```
curl -X POST -d "url=http://classik.forumactif.com/t7431-ces-disques-rares-qu-on-reverait-d-acuerir" http://api.watcher.link/page/
```

```
{
  "page": {
    "baseurl": "http://classik.forumactif.com/t7431-ces-disques-rares-qu-on-reverait-d-acquerir", 
    "id": "55ce1e241d4aba8c80e8b636", 
    "maxratio": 0.98, 
    "name": "Ces disques rares qu'on r\u00eaverait d'acqu\u00e9rir...", 
    "snaps": []
  }
}
```

### View page

```
curl http://api.watcher.link/page/55ce1e241d4aba8c80e8b636/
```

```
{
  "page": {
    "baseurl": "http://classik.forumactif.com/t7431-ces-disques-rares-qu-on-reverait-d-acquerir", 
    "id": "55ce1e241d4aba8c80e8b636", 
    "maxratio": 0.98, 
    "name": "Ces disques rares qu'on r\u00eaverait d'acqu\u00e9rir...", 
    "snaps": [
      {
        "dthr": "Fri, 14 Aug 2015 18:59:11 GMT", 
        "id": "55ce1e5f1d4aba8c80e8b637"
      }, 
      {
        "dthr": "Fri, 14 Aug 2015 18:59:11 GMT", 
        "id": "55ce1e5f1d4aba8c80e8b638"
      }, 
      {
        "dthr": "Fri, 14 Aug 2015 19:02:22 GMT", 
        "id": "55ce1f1e1d4aba8c80e8b639"
      }, 
      {
        "dthr": "Fri, 14 Aug 2015 19:02:22 GMT", 
        "id": "55ce1f1e1d4aba8c80e8b63a"
      }, 
      {
        "dthr": "Fri, 14 Aug 2015 19:02:24 GMT", 
        "id": "55ce1f201d4aba8c80e8b63b"
      }, 
      {
        "dthr": "Fri, 14 Aug 2015 19:02:24 GMT", 
        "id": "55ce1f201d4aba8c80e8b63c"
      }, 
      {
        "dthr": "Fri, 14 Aug 2015 19:04:08 GMT", 
        "id": "55ce1f881d4aba8c9ae8998f"
      }, 
      {
        "dthr": "Fri, 14 Aug 2015 19:11:23 GMT", 
        "id": "55ce213b1d4aba8cef139b5d"
      }, 
      {
        "dthr": "Fri, 14 Aug 2015 19:11:30 GMT", 
        "id": "55ce21421d4aba8cef139b5e"
      }
    ]
  }
}
```

### Create snapshot

```
curl -X POST -d "page=55ce1e241d4aba8c80e8b636" http://api.watcher.link/snap/
```

```
{
  "id": "55ce1e5f1d4aba8c80e8b638"
}
```

### View snap

/!\ return all html and png ! 

```
curl http://api.watcher.link/snap/55ce1e5f1d4aba8c80e8b638/
```

#### View snap png screen

```
curl http://api.watcher.link/snap/55ce21421d4aba8cef139b5e/png/ > screen.png; open screen.png
```

#### View snap html 

```
curl http://api.watcher.link/snap/55ce21421d4aba8cef139b5e/html/ > screen.html
```

## View diff between two snap

```
curl http://api.watcher.link/diff/55ce213b1d4aba8cef139b5d/55ce21421d4aba8cef139b5e/
```

```
{
  "diff": {
    "delete": [], 
    "fst": {
      "dthr": "Fri, 14 Aug 2015 19:11:23 GMT", 
      "id": "55ce213b1d4aba8cef139b5d"
    }, 
    "insert": [
      ""
    ], 
    "ratio": 0.998598785614199, 
    "replace": [], 
    "snd": {
      "dthr": "Fri, 14 Aug 2015 19:11:30 GMT", 
      "id": "55ce21421d4aba8cef139b5e"
    }
  }
}
```

## Installation

Voir le provisioning du Vagrantfile

```
pip setup.py install
```

```
apt-get install phantomjs python-dev
```

```
pip install -r requirements.txt 
```