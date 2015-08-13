# 'watcher' de liens en 150 lignes

Exemple simple d'un watcher de liens. Il manque des fonctions comme des abonnements 
qui pourraient envoyer un mail si une page change avec un ratio < .80, ajouter un 
screenshot de la page au snap avec weasyprint ...

## Exemple

Plus le ratio est petit, plus il y a eu du changement.

http://api.watcher.link/diff/55cc953f1d4aba76d0162f4f/

```
{
  "diff": {
    "fst": {
      "dthr": "Thu, 13 Aug 2015 15:02:22 GMT", 
      "id": "55cc955e1d4aba76d0162f53"
    }, 
    "ratio": 0.979129397734049, 
    "snd": {
      "dthr": "Thu, 13 Aug 2015 15:02:10 GMT", 
      "id": "55cc95521d4aba76d0162f52"
    }
  }
}
```

Preview html

http://api.watcher.link/diffhtml/55cc953f1d4aba76d0162f4f/

## Ajouter une url

*http://api.watcher.link/new/?url=http://classik.forumactif.com/f7-concerts*

```
{
  "page": {
    "_id": {
      "$oid": "55cc93bb1d4aba76d0162f4b"
    }, 
    "baseurl": "http://classik.forumactif.com/f7-concerts", 
    "contents": [], 
    "diffs": [], 
    "name": "Concerts"
  }
}
```

## Snap d'une url

Le différentiel est fait entre les deux derniers snaps. 
Plus les snaps sont courts, moins il y a de chance d'avoir un diff.

*http://api.watcher.link/snap/55cc93bb1d4aba76d0162f4b/*

```
{
  "page": {
    "_id": {
      "$oid": "55cc93bb1d4aba76d0162f4b"
    }, 
    "baseurl": "http://classik.forumactif.com/f7-concerts", 
    "contents": [
      {
        "$oid": "55cc942d1d4aba76d0162f4c"
      }, 
      {
        "$oid": "55cc943c1d4aba76d0162f4d"
      }
    ], 
    "diffs": [], 
    "name": "Concerts"
  }
}
```

## Diff d'une url

Plus le ratio est petit, plus il y a eu du changement. Le ratio est compris entre 0 et 1.

*http://api.watcher.link/diff/55cc93bb1d4aba76d0162f4b/*

```
{
  "diff": {
    "fst": {
      "dthr": "Thu, 13 Aug 2015 14:57:33 GMT", 
      "id": "55cc943d1d4aba76d0162f4e"
    }, 
    "ratio": 1.0, 
    "snd": {
      "dthr": "Thu, 13 Aug 2015 14:57:32 GMT", 
      "id": "55cc943c1d4aba76d0162f4d"
    }
  }
}
```

### Diff html

*http://api.watcher.link/diffhtml/55cc93bb1d4aba76d0162f4b/*