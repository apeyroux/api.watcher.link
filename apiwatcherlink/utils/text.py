
def split80(tbl):
    lentbl = len(tbl)
    if lentbl >= 80:
        yield "".join(list(split80(tbl[80:]))[:80])
    else:
        yield tbl


