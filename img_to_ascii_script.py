#!/usr/bin/env python3
import sys
import argparse
from PIL import Image, ImageEnhance
import numpy as np
filename=""
height=0
width=0

def find_closest(p):
    global pix_vals
    begin = abs(pix_vals[0] - p)
    num = int(begin / 28)
    if abs(pix_vals[num] - p) < abs(pix_vals[num + 1] - p):
        return pix_vals[num]
    else:
        return pix_vals[num + 1]

def proccess_image(img):
    global width,height
    width = int(width / 8)
    height = int(height / 8)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    img = img.convert('L')

    pixels=img.load()
    new_pix=[]

    for y in range(height):
        row = []
        for x in range(width):
            new_p = find_closest(pixels[x, y])
            row.append(new_p)
        new_pix.append(row)
    return new_pix

def make_into_ascii_art(pix, pixel_size):
    global height,width,pixels_ascii,filename
    with open(f"ascii/{filename.split(".")[0]}.html", "w") as f:
        f.write(f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ASCII Art {filename.split("."[1])}</title>
            <style>
                body {{
                    background-color: rgb(39, 38, 38);
                    color: azure;
                    font-size: {pixel_size}px;
                    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', 
                                 Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                    text-justify: none;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <pre>""")

        for y in range(height):
            line = ''.join(pixels_ascii[pix[y][x]]+" " for x in range(width))
            f.write(line + "\n")

        # Write footer
        f.write("""    </pre>
    </body>
    </html>""")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate ASCII art from an image.")

    parser.add_argument('-f', '--file', help='File to process')
    parser.add_argument("--size","-s",type=int,default=8)

    args = parser.parse_args()

    if not args.file:
        exit()
    if not args.image:
        exit()

    img = Image.open(f"imgs/{sys.argv[1]}")
    height=img.height
    width=img.width
    pixels = proccess_image(img)
    make_into_ascii_art(pixels,8)

pixels_ascii = {
    0: " ",
    28: ".",
    56: "^",
    84: "*",
    112: ":",
    140: "!",
    168: ">",
    196: "P",
    224: "@",
    255: "█",
}
pix_vals = [
    0,
    28,
    56,
    84,
    112,
    140,
    168,
    196,
    224,
    255,
]
