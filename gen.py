import random
import json
import sys

# Read config
config_file = open("config.json") #open(sys.argv[1])
config = config_file.read()
config = json.loads(config)
indent = config["indent"]

def open_tag(code, left_pad, tag, attributes={}):
    for i in range (0, left_pad):
        code += " "
    code += f"<{tag}"
    for key in attributes:
        code += f" {key}='{attributes[key]}'"
    code += ">\n"
    left_pad += indent
    return (code, left_pad)

def add_single_tag(code, left_pad, tag, attributes={}):
    for i in range (0, left_pad):
        code += " "
    code += f"<{tag}"
    for key in attributes:
        code += f" {key}='{attributes[key]}'"
    code += ">\n"
    return (code, left_pad)

def close_tag(code, left_pad, tag):
    left_pad -= indent
    for i in range (0, left_pad):
        code += " "
    code += f"</{tag}>\n"
    return (code, left_pad)

def add_content(code, left_pad, content):
    for i in range (0, left_pad):
        code += " "
    code += f"{content}\n"
    return (code, left_pad)

def open_close_tag(code, left_pad, tag, attributes=[], content=""):
    # Open tag
    for i in range (0, left_pad):
        code += " "
    code += f"<{tag}"
    for attribute in attributes:
        code += f" {attribute['name']}='{attribute['value']}'"
    code += ">"
    # Add content
    code += content
    # Close tag
    code += f"</{tag}>\n"
    return (code, left_pad)

""" def generate_html_css(name):
    code = ""
    left_pad = 0
    css = ""
    code, left_pad = open_tag(code, left_pad, "html")
    code, left_pad = generate_head(code, left_pad, name)
    code, left_pad = open_tag(code, left_pad, "div", { "class": "cont hstart" })
    code, left_pad = add_content(code, left_pad, "External content.")
    code, left_pad = open_close_tag(code, left_pad, "div", content="This is an open-close tag.")
    code, left_pad = close_tag(code, left_pad, "div")
    code, left_pad = close_tag(code, left_pad, "html")
    return (code.strip(), css.strip())

def generate_head(code, left_pad, name):
    code, left_pad = open_tag(code, left_pad, "head")
    # Add style reference
    code, left_pad = add_single_tag(code, left_pad, "link", { "rel": "stylesheet", "href": f"{name}.css"})
    code, left_pad = close_tag(code, left_pad, "head")
    return (code, left_pad) """

def pick_random(l):
    return l[random.randint(0, len(l) - 1)]

def random_rgb():
    return f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"

def format_document(name, html):
    return f"""<!DOCTYPE HTML>
<html>
<head>
<style>
* {{
    font-family: {pick_random(config["font-family"])};
}}
body {{
    margin: 0;
}}
</style>
<link rel="stylesheet" type="text/css" href="{name}.css">
</head>
<body>
{html}
</body>
</html>"""

def generate_document():
    html = ""
    css = {}
    left_pad = 0
    # Choose page-wide css
    css["main-cont"] = {
        "margin": 0,
        "padding": pick_random(config["padding"]),
        "color": pick_random(config["color"]),
        "background-color": pick_random(config["color"]),
    }
    # Open main container div
    html, left_pad = open_tag(html, left_pad, "div", { "class": "main-cont" })
    # Choose number of rows and generate them
    num_rows = pick_random(config["num_rows"])
    html, css = generate_rows(html, css, left_pad, num_rows)
    # Close main container div
    html, left_pad = close_tag(html, left_pad, "div")

    # Generate css code from dict
    css_code = ""
    for c in css:
        css_code += f".{c} {{\n"
        for a in css[c]:
            for i in range(0, indent): css_code += " "
            css_code += f"{a}: {css[c][a]};\n"
        css_code += "}\n\n"

    return (html.strip(), css_code.strip())

def generate_rows(html, css, left_pad, num_rows):
    for i in range(0, num_rows):
        html, css = generate_row(html, css, left_pad, pick_random(["single", "multiple"]))

    return (html, css)

def generate_row(html, css, left_pad, columns):
    # Row css class
    css["h-cont"] = {
        "display": "flex",
        "flex-direction": "row"
    }
    classes = "h-cont"
    # Custom style?
    if (pick_random([True, False, False, False, False, False])):
        css[f"c-cont-{len(html)}"] = {
            "justify-content": pick_random(config["justify-content"]),
            "align-items": pick_random(config["align-items"])
        }
        classes += f" c-cont-{len(html)}"
    # Open row
    html, left_pad = open_tag(html, left_pad, "div", { "class": classes })
    if (columns == "single"):
        html, css = generate_single_column(html, css, left_pad)
    else:
        num_cols = pick_random(config["num_cols"])
        for i in range(0, num_cols):
            html, css = generate_column(html, css, left_pad, num_cols)
    # Close row
    html, left_pad = close_tag(html, left_pad, "div")

    return (html, css)

def generate_single_column(html, css, left_pad):
    # Single column css class
    css["s-col"] = {
        "flex": "1"
    }
    # Custom style?
    if (pick_random([True, False, False, False])):
        custom_class_name = f"c-col-{len(html)}"
        css[custom_class_name] = {
            "padding": pick_random(config["padding"]),
            "color": pick_random(config["color"]),
            "background-color": pick_random(config["color"]),
        }
        classes = f"s-col {custom_class_name}"
    else:
        classes = "s-col"
    # Open column
    html, left_pad = open_tag(html, left_pad, "div", { "class": classes })
    # TODO pick random block
    html, left_pad = add_content(html, left_pad, "PLACEHOLDER")
    # Close column
    html, left_pad = close_tag(html, left_pad, "div")
    
    return (html, css)

def generate_column(html, css, left_pad, num_cols):
    # Column css class
    css[f"n{num_cols}-col"] = {
        "flex": '{0:.2g}'.format(1/num_cols)
    }
    # Custom style?
    if (pick_random([True, False, False, False])):
        custom_class_name = f"c-col-{len(html)}"
        css[custom_class_name] = {
            "padding": pick_random(config["padding"]),
            "color": pick_random(config["color"]),
            "background-color": pick_random(config["color"]),
        }
        classes = f"n{num_cols}-col {custom_class_name}"
    else:
        classes = f"n{num_cols}-col"
    # Open column
    html, left_pad = open_tag(html, left_pad, "div", { "class": classes })
    # TODO pick random block
    html, left_pad = add_content(html, left_pad, "PLACEHOLDER")
    # Close column
    html, left_pad = close_tag(html, left_pad, "div")

    return (html, css)

html, css = generate_document()
hbdl_file = open("out.hbdl", "w")
hbdl_file.write(html)
html_file = open("out.html", "w")
html_file.write(format_document("out", html))
css_file = open("out.css", "w")
css_file.write(css)


