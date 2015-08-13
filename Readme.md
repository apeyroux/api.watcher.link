# Exemple d'utilisation 

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

If the ratio is small, the page had more change. Here, there was not to change.

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