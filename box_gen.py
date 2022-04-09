

def gen_box(x, y, z):
    print("[")
    for xs in x:
        for ys in y:
            for zs in z:
                print("[" + str(xs) + ',' + str(ys) + ',' + str(zs) + '],')
    print("]")

gen_box((-30, -46), (5, 4), (-1, 1))