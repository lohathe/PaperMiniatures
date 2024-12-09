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


def composePage(images, elements_layout, output_definition):
    page_w_pxl = mm2pixel(output_definition["width"], output_definition["PPI"])
    page_h_pxl = mm2pixel(output_definition["height"], output_definition["PPI"])
    res = Image.new("RGBA", (page_w_pxl, page_h_pxl), (255, 255, 255, 255))

    for el in elements_layout:
        res.paste(images[el.id], (el.x, el.y), images[el.id].split()[3])
    return res
