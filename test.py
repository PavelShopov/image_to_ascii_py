from PIL import Image, ImageEnhance

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


def make_into_ascii_art(pix, pixel_size, new_width, new_height):
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
        for y in range(new_height):
            line = f" ".join(pixels_ascii_values[pix[y][x]] for x in range(new_width))
            f.write(line + "\n")

        f.write("""</pre>
        </body>
        </html>""")

def main():
    img = Image.open('imgs/owl.jpg')
    width, height = img.size
    resize_factor = 12
    new_width = width // resize_factor
    new_height = height // resize_factor

    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    resized_img = ImageEnhance.Brightness(resized_img).enhance(1.1)
    resized_img = ImageEnhance.Contrast(resized_img).enhance(1.4)
    resized_img = ImageEnhance.Sharpness(resized_img).enhance(1.2)
    gray_resized_img = resized_img.convert('L')
    pixels_image = gray_resized_img.load()

    new_pix = []

    for y in range(new_height):
        row = [find_closest( pixels_image[x,y]) for x in range(new_width)]
        new_pix.append(row)

    make_into_ascii_art(new_pix, 4, new_width, new_height)
if __name__ == '__main__':
    main()