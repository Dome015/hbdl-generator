import random
import json
import sys
from lorem_text import lorem

# Read config
config_file = open("config.json") #open(sys.argv[1])
config = config_file.read()
config = json.loads(config)
indent = config["indent"]
# Keep track of open/closed tags
open_tag_n = 0

def open_tag(code, left_pad, tag, attributes={}):
    global open_tag_n
    for i in range (0, left_pad):
        code += " "
    code += f"<{tag}"
    for key in attributes:
        code += f" {key}='{attributes[key]}'"
    code += ">\n"
    left_pad += indent
    open_tag_n += 1
    return (code, left_pad)

def add_single_tag(code, left_pad, tag, attributes={}):
    for i in range (0, left_pad):
        code += " "
    code += f"<{tag}"
    for key in attributes:
        code += f" {key}='{attributes[key]}'"
    code += ">\n"
    return (code)

def close_tag(code, left_pad, tag):
    global open_tag_n
    left_pad -= indent
    for i in range (0, left_pad):
        code += " "
    code += f"</{tag}>\n"
    open_tag_n -= 1
    return (code, left_pad)

def add_content(code, left_pad, content):
    for i in range (0, left_pad):
        code += " "
    code += f"{content}\n"
    return code

def open_close_tag(code, left_pad, tag, attributes={}, content=""):
    # Open tag
    for i in range (0, left_pad):
        code += " "
    code += f"<{tag}"
    for key in attributes:
        code += f" {key}='{attributes[key]}'"
    code += ">"
    # Add content
    code += content
    # Close tag
    code += f"</{tag}>\n"
    return code

def pick_random(l):
    return l[random.randint(0, len(l) - 1)]

def probability(prob):
    return random.random() <= prob

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
        "padding": f"{pick_random(config['padding-tb'])} {pick_random(config['padding-lr'])}",
        "color": pick_random(config["color"]),
        "background-color": pick_random(config["color"]),
    }
    # Choose page-wide button css
    css["main-btn"] = {
        "padding": pick_random(config["button-padding"]),
        "color": pick_random(config["color"]),
        "font-size": pick_random(["medium, large"]),
        "font-weight": pick_random(["normal, bold"]),
        "background-color": pick_random(config["color"]),
        "border-style": "none",
        "border-radius": pick_random(config["border-radius"]),
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

    # If there are still open tags, that's an issue: warn me
    if open_tag_n != 0: print(f"WARNING: {open_tag_n} tags not closed")
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
    if (probability(0.1)):
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
        "flex": "1",
        "display": "flex",
        "flex-direction": "column"
    }
    # Custom style?
    if (probability(0.05)):
        custom_class_name = f"c-col-{len(html)}"
        css[custom_class_name] = {
            "padding": pick_random(config["padding"]),
            "color": pick_random(config["color"]),
            "background-color": pick_random(config["color"]),
            "justify-content": pick_random(config["justify-content"])
        }
        classes = f"s-col {custom_class_name}"
    else:
        classes = "s-col"
    # Open column
    html, left_pad = open_tag(html, left_pad, "div", { "class": classes })
    # Pick block
    block = pick_random(["title-text-button", "table"])
    html, css, left_pad = generate_block(html, css, left_pad, block)
    # Close column
    html, left_pad = close_tag(html, left_pad, "div")
    
    return (html, css)

def generate_column(html, css, left_pad, num_cols):
    # Column css class
    classes = ""
    if (probability(0.75)):
        css[f"n{num_cols}-col"] = {
            "flex": '{0:.2g}'.format(1/num_cols),
            "display": "flex",
            "flex-direction": "column",
            "text-align": pick_random(config["text-align"])
        }
        classes += f"n{num_cols}-col"
    else:
        css[f"c-col-{len(html)}-f"] = {
            "flex": '{0:.2g}'.format(2/num_cols),
            "display": "flex",
            "flex-direction": "column",
            "text-align": pick_random(config["text-align"])
        }
        classes += f"c-col-{len(html)}-f"
    # Custom style?
    if (probability(0.05)):
        custom_class_name = f"c-col-{len(html)}"
        css[custom_class_name] = {
            "padding": pick_random(config["padding"]),
            "color": pick_random(config["color"]),
            "background-color": pick_random(config["color"]),
            "justify-content": pick_random(config["justify-content"]),
            "align-items": pick_random(config["align-items"])
        }
        classes += f" {custom_class_name}"
    # Open column
    html, left_pad = open_tag(html, left_pad, "div", { "class": classes })
    # Pick block
    block = pick_random(["title-text-button", "table"])
    html, css, left_pad = generate_block(html, css, left_pad, block)
    # Close column
    html, left_pad = close_tag(html, left_pad, "div")

    return (html, css)

def generate_block(html, css, left_pad, block):
    if block == "title-text-button":
        # Title
        if (probability(0.5)):
            css["title-block"] = {
                "font-weight": "bold",
                "font-size": "large",
                "padding": f"{pick_random(config['padding'])}",
            }
            html, left_pad = open_tag(html, left_pad, "div", { "class": "title-block" })
            html = open_close_tag(html, left_pad, "div", content=lorem.words(random.randint(2, 5)))
            html, left_pad = close_tag(html, left_pad, "div")
        # Text
        if (probability(0.5)):
            css[f"text-block-{len(html)}"] = {
                "font-size": "medium",
                "display": "flex",
                "justify-content": pick_random(config["justify-content"]),
                "padding": f"{pick_random(config['padding'])}",
            }
            html, left_pad = open_tag(html, left_pad, "div", { "class": f"text-block-{len(html)}" })
            html = open_close_tag(html, left_pad, "div", content=lorem.words(random.randint(10, 30)))
            html, left_pad = close_tag(html, left_pad, "div")
        # Button
        if (probability(0.5)):            
            if (probability(0.1)):
                css[f"btn-{len(html)}"] = {
                    "padding": css["main-btn"]["padding"],
                    "color": pick_random(config["color"]),
                    "font-size": css["main-btn"]["font-size"],
                    "font-weight": css["main-btn"]["font-weight"],
                    "background-color": pick_random(config["color"]),
                    "border-style": css["main-btn"]["border-style"],
                    "border-radius": css["main-btn"]["border-radius"],
                }
                button_class = f"btn-{len(html)}"
            else:                
                button_class = "main-btn"
            html, left_pad = open_tag(html, left_pad, "div", { "class": f"text-block-{len(html)}" })
            for i in range(0, random.randint(1, 3)):
                html = open_close_tag(html, left_pad, "button", { "type": "button", "class": button_class }, lorem.words(random.randint(1, 3)))
            html, left_pad = close_tag(html, left_pad, "div")
    elif block == "table":
        # Table container styling
        table_cont_class_name = f"tbl-{len(html)}-cont"
        css[table_cont_class_name] = {
            "padding": pick_random(config["padding"])
        }
        table_class_name = f"tbl-{len(html)}"
        # Border styling
        css[f"{table_class_name} table, th, td"] = {
            "border": f'{pick_random(config["table-border"])} {pick_random(config["color"])}',         
        }
        # Width
        css[table_class_name] = {
            "width": "100%",
            "border-radius": pick_random(config["border-radius"]),
            "border-collapse": "collapse"
        }
        # Table headers styling
        css[f"{table_class_name} th"] = {
            "padding": f"{pick_random(config['table-padding-tb'])} {pick_random(config['table-padding-lr'])}",
            "text-align": pick_random(config["table-text-align"]),
            "background-color": pick_random(config["color"]),
            "color": pick_random(config["color"]),
            "font-weight": pick_random(config["font-weight"])
        }
        # Table row styling
        css[f"{table_class_name} tr"] = {
            "padding": f"{pick_random(config['table-padding-tb'])} {pick_random(config['table-padding-lr'])}",
            "text-align": pick_random(config["table-text-align"]),
            "background-color": pick_random(config["color"]),
            "color": pick_random(config["color"])
        }
        # Even rows colored different
        if probability(0.5):
            css[f"{table_class_name} tr:nth-child(even)"] = {
                "background-color": pick_random(config["color"])
            }
        # Fields with type
        num_fields = random.randint(2, 8)
        num_buttons = random.randint(0, 3)
        fields = []
        for i in range(0, num_fields):
            fields.append({
                "field_name": lorem.words(random.randint(1, 3)),
                "field_type": pick_random(["text", "integer", "float"])
            })
        # Filters?
        has_filters = probability(0.5)
        if has_filters:
            for field in fields:
                if field["field_type"] in ["text", "integer"]:
                    field["filter_type"] = pick_random(["text", "select", "none"])
                elif field["field_type"] == "float":
                    field["filter_type"] = pick_random(["text", "none"])
        num_rows = pick_random([5, 10])
        # Generate table
        html, left_pad = open_tag(html, left_pad, "div", { "class": table_cont_class_name })
        html, left_pad = open_tag(html, left_pad, "table", { "class": table_class_name })
        html, left_pad = open_tag(html, left_pad, "thead")
        for field in fields:
            html = open_close_tag(html, left_pad, "th", content=field["field_name"])
        html, left_pad = close_tag(html, left_pad, "thead")
        html, left_pad = open_tag(html, left_pad, "tbody")
        # Filters
        if has_filters:
            # Create styles
            text_class_name = f"tbl-{len(html)}-text"
            css[text_class_name] = {
                "color": pick_random(config["color"]),
                "border-radius": pick_random(config["border-radius"]),
                "border-style": "solid",
                "border-width": pick_random(config["border-width"]),
                "padding": f"{pick_random(config['table-padding-tb'])} {pick_random(config['table-padding-lr'])}"
            }
            select_class_name = f"tbl-{len(html)}-select"
            css[select_class_name] = {
                "color": pick_random(config["color"]),
                "border-radius": pick_random(config["border-radius"]),
                "border-style": "solid",
                "border-width": pick_random(config["border-width"]),
                "padding": f"{pick_random(config['table-padding-tb'])} {pick_random(config['table-padding-lr'])}"
            }
            # Add filters row, if there is at least one
            if len(list(filter(lambda f: f["filter_type"] != "none", fields))) > 0:
                html, left_pad = open_tag(html, left_pad, "tr")
                for field in fields:
                    html, left_pad = open_tag(html, left_pad, "td")
                    if field["filter_type"] == "text":
                        html = add_single_tag(html, left_pad, "input", {
                            "class": text_class_name,
                            "type": "text",
                            "placeholder": lorem.words(random.randint(0, 2))
                        })
                    elif field["filter_type"] == "select":
                        html, left_pad = open_tag(html, left_pad, "select", { "class": select_class_name })
                        for i in range(0, 3):
                            option_value = lorem.words(random.randint(1, 3))
                            html = open_close_tag(html, left_pad, "option", { "value": option_value }, option_value)
                        html, left_pad = close_tag(html, left_pad, "select")
                    html, left_pad = close_tag(html, left_pad, "td")
                html, left_pad = close_tag(html, left_pad, "tr")
        # Add data rows
        for i in range(0, num_rows):
            html, left_pad = open_tag(html, left_pad, "tr")
            for field in fields:
                content = ""
                if (field["field_type"] == "text"):
                    content = lorem.words(random.randint(1, 3))
                elif (field["field_type"] == "integer"):
                    content = str(random.randint(0, 100)) 
                elif (field["field_type"] == "float"):
                    content = '{0:.2g}'.format(random.random() * 100)
                html = open_close_tag(html, left_pad, "td", content=content)
            html, left_pad = close_tag(html, left_pad, "tr")
        html, left_pad = close_tag(html, left_pad, "tbody")
        html, left_pad = close_tag(html, left_pad, "table")
        html, left_pad = close_tag(html, left_pad, "div")
    else:
        html = add_content(html, left_pad, block)

    return (html, css, left_pad)


html, css = generate_document()
hbdl_file = open("out.hbdl", "w")
hbdl_file.write(html)
html_file = open("out.html", "w")
html_file.write(format_document("out", html))
css_file = open("out.css", "w")
css_file.write(css)


