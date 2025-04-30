#!/usr/bin/env python3
import sys
import argparse
from PIL import Image, ImageEnhance
import numpy as np

filename = ""
pixels_ascii_values = {
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


def find_closest(p):
    pix_vals = [0, 28, 56, 84, 112, 140, 168, 196, 224, 255]
    begin = abs(pix_vals[0] - p)
    num = int(begin / 28)
    if num == 9:
        return pix_vals[num]
    elif abs(pix_vals[num] - p) < abs(pix_vals[num + 1] - p):
        return pix_vals[num]
    else:
        return pix_vals[num + 1]


def make_into_ascii_art(pixels, args, new_width, new_height):
    global pixels_ascii_values
    with open("ascii/owl.html", "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>ASCII Art </title>
                    <style>
                        body {{
                            background-color: rgb(39, 38, 38);
                            color: azure;
                            font-size: {args.size}px;
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
        for y in range(new_height):
            line = f" ".join(pixels_ascii_values[pixels[y][x]] for x in range(new_width))
            f.write(line + "\n")

        f.write("""</pre>
        </body>
        </html>""")


def process_img(img, args, new_width, new_height):
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    resized_img = ImageEnhance.Brightness(resized_img).enhance(args.brightness)
    resized_img = ImageEnhance.Contrast(resized_img).enhance(args.contrast)
    resized_img = ImageEnhance.Sharpness(resized_img).enhance(args.sharpness)
    gray_resized_img = resized_img.convert('L')
    temp_pixels = gray_resized_img.load()
    new_pixels = []
    for y in range(new_height):
        row = [find_closest(temp_pixels[x, y]) for x in range(new_width)]
        new_pixels.append(row)
    return new_pixels


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate ASCII art from an image.")

    parser.add_argument('-f', '--file', help='File to process')
    parser.add_argument("--pixel_size", "-ps", type=int, default=8)
    parser.add_argument("--size", "-s", type=int, default=8)
    parser.add_argument("--brightness", "-b", type=float, default=1.2)
    parser.add_argument("--contrast", "-c", type=float, default=1.2)
    parser.add_argument("--sharpness", "-sh", type=float, default=1.2)

    args = parser.parse_args()

    if not args.file:
        exit()

    if not args.image:
        exit()

    img = Image.open(f"imgs/{sys.argv[1]}")
    width, height = img.size
    new_width = width // args.size
    new_height = height // args.size

    new_pixels = process_img(img, args, new_width, new_height)
    make_into_ascii_art(new_pixels, args,  new_width, new_height)
