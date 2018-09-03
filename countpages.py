mypages = [4, 6, 8, 13, 14, 16, 22, 24, 25, 28, 30, 31, 33, 36, 38, 39, 41, 42,
    44, 46, 48, 50, 52, 53, 55, 56, 58, 59, 89, 98, 144, 155, 156, 157, 163, 166,
    167, 187, 188, 189, 192, 194, 196, 241, 242, 243, 244, 247, 248, 296]

def countpages(pages):

    new_pages = []
    start = 0
    end = 0
    i = 0

    for p in pages:
        if type(p) != int:
            exit("FEHLER: '{}' ist kein Integerwert, Liste muss aus Integern bestehen!".format(p))

    pages.sort()

    while i < len(pages):
        start = pages[i]
        end = pages[i]

        #print("Durchlaufe p[{}] mit Wert {}".format(i, pages[i]))

        k = i + 1

        while k < len(pages):
            if pages[k] == pages[k-1] + 1:
                end = pages[k]
            else:
                break

            k = k + 1

        i = k
        if start == end:
            new_pages.append(str(start))
        #elif end == start + 1:
        #    new_pages.append("{}f.".format(start))
        else:
            new_pages.append("{}-{}".format(start, end))

    return ", ".join(new_pages)

#countpages(mypages)
