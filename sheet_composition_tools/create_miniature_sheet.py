import argparse
import json
import images_utils
import packing_algos


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("description_file",
        type=str,
        help="JSON file describing the expected output.")
    parser.add_argument("-p", "--packing_algorithm",
        type=int,
        default=1,
        help="Which algorithm to use (not documented, see source code).")
    parser.add_argument("-o", "--output_name",
        type=str,
        default="output",
        help="name to use for output files.")
    args = parser.parse_args()

    with open(args.description_file, "r") as f:
        descr = json.load(f)

    images = []
    for i, element in enumerate(descr["images"]):
        try:
            miniature = images_utils.createSimmetricMiniature(
                element["path"],
                descr["miniature_composition"],
                descr["output"]["PPI"])
        except:
            print("[ERROR] on image {} (file {})".format(i, element["path"]))
            raise

        images.append( (miniature, element["quantity"]) )

    output_w_pxl = images_utils.mm2pixel(descr["output"]["width"], descr["output"]["PPI"])
    output_h_pxl = images_utils.mm2pixel(descr["output"]["height"], descr["output"]["PPI"])
    if args.packing_algorithm == 1:
        pack = lambda x, y: packing_algos.simplePacking(x, y, "sort-descending")
    elif args.packing_algorithm == 2:
        pack = lambda x, y: packing_algos.simplePacking(x, y, "sort-ascending")
    elif args.packing_algorithm == 3:
        pack = lambda x, y: packing_algos.simplePacking(x, y, "random")
    elif args.packing_algorithm == 4:
        pack = lambda x, y: packing_algos.greedyPacking(x, y, "sort-descending")
    elif args.packing_algorithm == 5:
        pack = lambda x, y: packing_algos.greedyPacking(x, y, "sort-ascending")
    elif args.packing_algorithm == 6:
        pack = lambda x, y: packing_algos.greedyPacking(x, y, "random")
    else:
        raise RuntimeError("unknown packing algorithm!")
    pages_layout = pack(images, (output_w_pxl, output_h_pxl))
    print(pages_layout)

    for i, page_layout in enumerate(pages_layout):
        page = images_utils.composePage(images, page_layout, descr["output"])
        page.save("{}_{}.png".format(args.output_name, i),
            dpi=(descr["output"]["PPI"], descr["output"]["PPI"]))


if __name__ == "__main__":
    main()
