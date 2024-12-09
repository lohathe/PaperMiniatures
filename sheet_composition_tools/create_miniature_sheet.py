import argparse
import json
import images_utils
import packing_algos


def main():
    def auto_int(x):
        return int(x, 0)
    parser = argparse.ArgumentParser()
    parser.add_argument("description_file",
        type=str,
        help="JSON file describing the expected output.")
    parser.add_argument("-f", "--algo_flags",
        type=auto_int,
        default=1,
        help="Flags for the packing algoritm.")
    parser.add_argument("-o", "--output_name",
        type=str,
        default="output",
        help="name to use for output files.")
    args = parser.parse_args()

    with open(args.description_file, "r") as f:
        descr = json.load(f)

    images = []
    quantities = []
    for i, element in enumerate(descr["images"]):
        try:
            miniature_image = images_utils.createSimmetricMiniature(
                element["path"],
                descr["miniature_composition"],
                descr["output"]["PPI"])
        except:
            print("[ERROR] on image {} (file {})".format(i, element["path"]))
            raise

        images.append(miniature_image)
        quantities.append(element["quantity"])

    output_w_pxl = images_utils.mm2pixel(descr["output"]["width"], descr["output"]["PPI"])
    output_h_pxl = images_utils.mm2pixel(descr["output"]["height"], descr["output"]["PPI"])

    elements = []
    for i, image in enumerate(images):
        elements.append(packing_algos.RectElement(i, image.size[0], image.size[1]))

    pages_layout = packing_algos.computePacking(
        zip(elements, quantities),
        (output_w_pxl, output_h_pxl),
        args.algo_flags)

    for i, page_layout in enumerate(pages_layout):
        page = images_utils.composePage(images, page_layout, descr["output"])
        page.save("{}_{}.png".format(args.output_name, i),
            dpi=(descr["output"]["PPI"], descr["output"]["PPI"]))


if __name__ == "__main__":
    main()
