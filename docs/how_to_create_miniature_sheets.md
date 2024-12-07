# How to create miniature sheets

A simple Python program to pack all necessary images inside as few pages as possible.

It uses a JSON file (e.g., [example_packing_description.json](../sheet_composition_tools/example_packing_description.json)) to describe what images to pack inside the pages (and other configurations).

The goal of this tool is to ease/speed-up/automate the creation of a sheet containing the images that will become miniatures!

## Usage example

The command

```python
python3 sheet_composition_tools/create_miniature_sheet.py sheet_composition_tools/example_packing_description.json
```

will produce as many PNG files containing all the requested images. Such PNG files can then be printed and used to create the miniatures as described [here](./how_to_create_paper_miniatures.md#Recipe).


## Job description

```JSON
{
    "output": {
        "width": 210,
        "height": 297,
        "PPI": 300
    },
    "miniature_composition": {
        "support_height": 14,
        "support_color": [200, 200, 200],
        "padding": 8
    },
    "images": [
        {
            "path": "images/animals/boar_1.png",
            "quantity": 3
        }
    ]
}
```
