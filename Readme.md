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
    "delete": [
      "TwitterRecherche", 
      "bit.ly/1gszRGs\u00a0Voir le r\u00e9sum\u00e9Masquer le r\u00e9sum\u00e92 Retweets1 favorisR\u00e9pondreRetweeter2Retweet\u00e92Favori1Ajout\u00e9 aux favoris1Plus"
    ], 
    "fst": {
      "dthr": "Thu, 13 Aug 2015 15:18:35 GMT", 
      "id": "55cc992b1d4aba76f425f2bd"
    }, 
    "insert": [
      "@j4pe_36 minil y a 36 minutesVoir la traductionWhy learn haskell for great good ... #python#haskellhttps://gist.github.com/j4/8369502251f6cbc49239\u00a0\u2026Voir la traduction\u00c0 l'origine en"
    ], 
    "ratio": 0.9779104477611941, 
    "replace": [
      "691 <-> j4pe_"
    ], 
    "snd": {
      "dthr": "Thu, 13 Aug 2015 15:18:18 GMT", 
      "id": "55cc991a1d4aba76f425f2bc"
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
    "delete": [
      "TwitterRecherche", 
      "bit.ly/1gszRGs\u00a0Voir le r\u00e9sum\u00e9Masquer le r\u00e9sum\u00e92 Retweets1 favorisR\u00e9pondreRetweeter2Retweet\u00e92Favori1Ajout\u00e9 aux favoris1Plus"
    ], 
    "fst": {
      "dthr": "Thu, 13 Aug 2015 15:18:35 GMT", 
      "id": "55cc992b1d4aba76f425f2bd"
    }, 
    "insert": [
      "@j4pe_36 minil y a 36 minutesVoir la traductionWhy learn haskell for great good ... #python#haskellhttps://gist.github.com/j4/8369502251f6cbc49239\u00a0\u2026Voir la traduction\u00c0 l'origine en"
    ], 
    "ratio": 0.9779104477611941, 
    "replace": [
      "691 <-> j4pe_"
    ], 
    "snd": {
      "dthr": "Thu, 13 Aug 2015 15:18:18 GMT", 
      "id": "55cc991a1d4aba76f425f2bc"
    }
  }
}
```

### Diff html

*http://api.watcher.link/diffhtml/55cc93bb1d4aba76d0162f4b/*