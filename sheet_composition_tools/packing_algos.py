import random


def simplePacking(images, output_size, variant):
    expanded_indexes = []
    for i in range(len(images)):
        expanded_indexes.extend([i]*images[i][1])
    page_w_pxl, page_h_pxl = output_size

    def computeBBox(rows):
        w, h = 0, 0
        for row in rows:
            row_w = sum([images[i][0].size[0] for i in row])
            row_h = max([images[i][0].size[1] for i in row])
            w = max([w, row_w])
            h = h + row_h
        return (w, h)

    def computeScore(pages):
        return (len(pages)-1)*page_h_pxl + computeBBox(pages[-1])[1]

    def computePacking(indexes):
        pages = []
        current_rows = [[]]
        ERROR_TEMPLATE = "Image at index {} is too big ({}={}pxl) to fit output page!"
        for i in indexes:
            current_rows[-1].append(i)
            if computeBBox(current_rows)[0] > page_w_pxl:
                # adding current image results in a too-long row
                # => let's try to create a new row for current image
                current_rows[-1].pop()
                if len(current_rows[-1]) == 0:
                    raise RuntimeError(ERROR_TEMPLATE.format(i, "width", images[i][0].size[0]))
                current_rows.append([i])
            if computeBBox(current_rows)[1] > page_h_pxl:
                # adding current image results in the last row exceeding
                # the max height of the output image => let's create a
                # new output image/page!
                current_rows[-1].pop()
                if len(current_rows) == 1 and len(current_rows[0]) == 0:
                    raise RuntimeError(ERROR_TEMPLATE.format(i, "height", images[i][0].size[1]))
                elif len(current_rows[-1]) == 0:
                    # remove last row if it is empty (i.e., we created a
                    # new row because new images made previous row too
                    # large, but the new row exceed the page height)
                    current_rows.pop()
                pages.append(current_rows)
                current_rows = [[i]]
        if len(current_rows) > 0 and len(current_rows[0]) > 0:
            pages.append(current_rows)
        return pages

    pages = []
    if variant == "random":
        best_score = 9999999999
        best_sol = None
        for _ in range(10000):
            random.shuffle(expanded_indexes)
            sol = computePacking(expanded_indexes)
            score = computeScore(sol)
            if score < best_score:
                print("found better packing: {}->{}".format(best_score, score))
                best_score = score
                best_sol = sol
        pages = best_sol
    elif variant == "sort-descending":
        expanded_indexes.sort(key=lambda x: -images[x][0].size[0])
        pages = computePacking(expanded_indexes)
    elif variant == "sort-ascending":
        expanded_indexes.sort(key=lambda x: images[x][0].size[0])
        pages = computePacking(expanded_indexes)
    else:
        raise RuntimeError("unknown variant {} for algo 'simplePacking'".format(variant))

    print("TOTAL VERTICAL PIXELS={}".format(computeScore(pages)))
    return pages


def greedyPacking(images, output_size, variant=False):
    expanded_indexes = []
    for i in range(len(images)):
        expanded_indexes.extend([i]*images[i][1])
    page_w_pxl, page_h_pxl = output_size

    def computeBBox(rows):
        w, h = 0, 0
        for row in rows:
            row_w = sum([images[i][0].size[0] for i in row])
            row_h = max([images[i][0].size[1] for i in row])
            w = max([w, row_w])
            h = h + row_h
        return (w, h)

    def computeScore(pages):
        return (len(pages)-1)*page_h_pxl + computeBBox(pages[-1])[1]

    def computePacking(indexes):
        pages = []
        for i in indexes:
            added = False
            for k1, page in enumerate(pages):
                if added:
                    break
                for k2, row in enumerate(page):
                    row.append(i)
                    bbox = computeBBox(page)
                    if bbox[0] <= page_w_pxl and bbox[1] <= page_h_pxl:
                        added = True
                        break
                    row.pop()
                if not added:
                    page.append([i])
                    bbox = computeBBox(page)
                    if bbox[0] <= page_w_pxl and bbox[1] <= page_h_pxl:
                        added = True
                        break
                    page.pop()
                else:
                    break
            if not added:
                pages.append([[i]])
        return pages

    pages = []
    if variant == "random":
        best_score = 9999999999
        best_sol = None
        for _ in range(10000):
            random.shuffle(expanded_indexes)
            sol = computePacking(expanded_indexes)
            score = computeScore(sol)
            if score < best_score:
                print("found better packing: {}->{}".format(best_score, score))
                best_score = score
                best_sol = sol
        pages = best_sol
    elif variant == "sort-descending":
        expanded_indexes.sort(key=lambda x: -images[x][0].size[0])
        pages = computePacking(expanded_indexes)
    elif variant == "sort-ascending":
        expanded_indexes.sort(key=lambda x: images[x][0].size[0])
        pages = computePacking(expanded_indexes)
    else:
        raise RuntimeError("unknown variant {} for algo 'greedyPacking'".format(variant))

    print("TOTAL VERTICAL PIXELS={}".format(computeScore(pages)))
    return pages
