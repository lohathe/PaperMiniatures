from PIL import Image
import PIL


def mm2pixel(val, PPI):
    IN_2_MM = 25.4
    return int(val/IN_2_MM*PPI)


def createSimmetricMiniature(img_path, composition, PPI):
    base = Image.open(img_path)
    # TODO: convert to RGBA with correct PPI in case input image is not OK!
    flipped = base.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    base_w_pxl, base_h_pxl = base.size
    support_pxl = mm2pixel(composition["support_height"], PPI)
    padding_pxl = mm2pixel(composition["padding"], PPI)
    support = Image.new("RGBA", (base_w_pxl, support_pxl), tuple(composition["support_color"]))
    res_w_pxl = base_w_pxl + 2*padding_pxl
    res_h_pxl = 2*base_h_pxl + support_pxl + 2*padding_pxl

    res = Image.new("RGBA", (res_w_pxl, res_h_pxl), (255, 255, 255, 0))
    res.paste(base, (padding_pxl, padding_pxl))
    res.paste(support, (padding_pxl, padding_pxl+base_h_pxl))
    res.paste(flipped, (padding_pxl, padding_pxl+base_h_pxl+support_pxl))
    return res


def composePage(images, page_layout, output_definition):
    page_w_pxl = mm2pixel(output_definition["width"], output_definition["PPI"])
    page_h_pxl = mm2pixel(output_definition["height"], output_definition["PPI"])
    res = Image.new("RGBA", (page_w_pxl, page_h_pxl), (255, 255, 255, 255))

    current_h_pxl = 0
    for row in page_layout:
        current_w_pxl = 0
        row_h_pxl = max(images[i][0].size[1] for i in row)
        for el in row:
            vertical_centering_offset = (row_h_pxl - images[el][0].size[1]) // 2
            res.paste(
                images[el][0],
                (current_w_pxl, current_h_pxl+vertical_centering_offset),
                images[el][0].split()[3])
            current_w_pxl += images[el][0].size[0]
        current_h_pxl += row_h_pxl
    return res
