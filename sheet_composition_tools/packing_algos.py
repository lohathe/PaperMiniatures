"""
Algorithms to pack together rectangles.

The final goal is to create a packing that must be easy to
cut with scissors, not really to create the best possible
packing!
"""
import random


FLAG_PRESORT_OFF = 0x0001
FLAG_PRESORT_DESCENDING = 0x0002
FLAG_PRESORT_ASCENDING = 0x0004
FLAG_RANDOM_OFF = 0x0010
FLAG_RANDOM_ON = 0x0020
FLAG_LOOKBACK_OFF = 0x0100
FLAG_LOOKBACK_ON = 0x0200
FLAG_AUTO_PADDING_OFF = 0x1000
FLAG_AUTO_PADDING_ON = 0x2000


class RectElement:
    def __init__(self, id, width, height):
        self.id = id
        self.w = width
        self.h = height
    def __repr__(self):
        return f"RectElement(id={self.id}, {self.w}x{self.h})"


class PositionedElement:
    def __init__(self, id, pos_x, pos_y):
        self.id = id
        self.x = pos_x
        self.y = pos_y
    def __repr__(self):
        return f"PositionedElement(id={self.id}, @({self.x}, {self.y}))"


def boundingBox(rows):
    w, h = 0, 0
    for row in rows:
        row_w = sum(element.w for element in row)
        row_h = max(element.h for element in row)
        w = max([w, row_w])
        h = sum([h, row_h])
    return (w, h)


def packingScore(pages, page_height):
    return (len(pages)-1)*page_height + boundingBox(pages[-1])[1]


def stepNoLookback(elements, page_w_pxl, page_h_pxl):
    pages = []
    current_rows = [[]]
    ERROR_TEMPLATE = "element.id=={} is too big ({}={}pxl) to fit output page!"
    for el in elements:
        current_rows[-1].append(el)
        if boundingBox(current_rows)[0] > page_w_pxl:
            # adding current element results in a too-long row
            # => let's try to create a new row for current element
            current_rows[-1].pop()
            if len(current_rows[-1]) == 0:
                raise RuntimeError(ERROR_TEMPLATE.format(el.id, "width", el.w))
            current_rows.append([el])
        if boundingBox(current_rows)[1] > page_h_pxl:
            # adding current element results in the last row exceeding
            # the max height of page => let's create new output page!
            current_rows[-1].pop()
            if len(current_rows) == 1 and len(current_rows[0]) == 0:
                raise RuntimeError(ERROR_TEMPLATE.format(el.id, "height", el.h))
            elif len(current_rows[-1]) == 0:
                # remove last row if it is empty (i.e., we created a
                # new row because new element made previous row too
                # large, but the new row exceed the page height)
                current_rows.pop()
            pages.append(current_rows)
            current_rows = [[el]]
    if len(current_rows) > 0 and len(current_rows[0]) > 0:
        pages.append(current_rows)
    return pages


def stepWithLookback(elements, page_w_pxl, page_h_pxl):
    pages = []
    for el in elements:
        added = False
        for page in pages:
            if added:
                break
            for row in page:
                row.append(el)
                bbox = boundingBox(page)
                if bbox[0] <= page_w_pxl and bbox[1] <= page_h_pxl:
                    added = True
                    break
                row.pop()
            if not added:
                page.append([el])
                bbox = boundingBox(page)
                if bbox[0] <= page_w_pxl and bbox[1] <= page_h_pxl:
                    added = True
                    break
                page.pop()
            else:
                break
        if not added:
            pages.append([[el]])
            bbox = boundingBox(pages[-1])
            if bbox[0] > page_w_pxl or bbox[1] > page_h_pxl:
                raise RuntimeError("element.id={} ({}x{}) can not fit page".format(el.id, el.w, el.h))
    return pages


def determineOffsets(pages, fit_to_width_pxl=None, fit_to_height_pxl=None):
    pages_layout = []
    for i, page in enumerate(pages):
        pages_layout.append([])
        current_h_pxl = 0
        vertical_padding = 0
        if fit_to_height_pxl and i != len(pages)-1:
            page_bbox = boundingBox(page)
            vertical_padding = (fit_to_height_pxl - page_bbox[1]) // (len(pages)*2)
        for row in page:
            row_bbox = boundingBox([row])
            current_w_pxl = 0
            horizontal_padding = 0
            if fit_to_width_pxl:
                horizontal_padding = (fit_to_width_pxl - row_bbox[0]) // (len(row)*2)
            for element in row:
                vertical_centering_offset = (row_bbox[1] - element.h) // 2
                pos_x = horizontal_padding + current_w_pxl
                pos_y = current_h_pxl + vertical_padding + vertical_centering_offset
                pages_layout[-1].append(PositionedElement(element.id, pos_x, pos_y))
                current_w_pxl += element.w + 2*horizontal_padding
            current_h_pxl += row_bbox[1] + 2*vertical_padding
    return pages_layout


def computePacking(elements_and_quantities, output_size, algo_flags):
    elements = []
    for element, quantity in elements_and_quantities:
        elements.extend([element]*quantity)
    page_w_pxl, page_h_pxl = output_size

    if algo_flags & FLAG_PRESORT_ASCENDING:
        elements.sort(key=lambda el: el.h)
    elif algo_flags & FLAG_PRESORT_DESCENDING:
        elements.sort(key=lambda el: -el.w)
    if algo_flags & FLAG_LOOKBACK_ON:
        step = stepWithLookback
    else:
        step = stepNoLookback

    pages = []
    if algo_flags & FLAG_RANDOM_ON:
        best_score = 9999999999
        for _ in range(10000):
            random.shuffle(elements)
            sol = step(elements, page_w_pxl, page_h_pxl)
            score = packingScore(sol, page_h_pxl)
            if score < best_score:
                best_score = score
                pages = sol
    else:
        pages = step(elements, page_w_pxl, page_h_pxl)
    print("TOTAL VERTICAL PIXELS={}".format(packingScore(pages, page_h_pxl)))

    pages_layout = []
    if algo_flags & FLAG_AUTO_PADDING_ON:
        pages_layout = determineOffsets(pages, page_w_pxl, page_h_pxl)
    else:
        pages_layout = determineOffsets(pages, None, None)

    return pages_layout
