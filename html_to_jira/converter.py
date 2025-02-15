from bs4 import BeautifulSoup, Tag
import re


def html_to_jira(html):
    soup = BeautifulSoup(html, "html.parser")

    # Ensure there's a body tag in the HTML
    if not soup.body:
        soup = BeautifulSoup(f"<body>{html}</body>", "html.parser")

    jira_markup = []

    def parse_element(element):
        if element.name == "h1":
            return f"h1. {parse_children(element)}"
        elif element.name == "h2":
            return f"h2. {parse_children(element)}"
        elif element.name == "h3":
            return f"h3. {parse_children(element)}"
        elif element.name == "p":
            return parse_children(element)
        elif element.name == "em":
            return f"_{parse_children(element)}_"
        elif element.name == "strong":
            return f"*{parse_children(element)}*"
        elif element.name == "u":
            return f"+{parse_children(element)}+"
        elif element.name == "ul":
            return "\n".join(
                [f"* {parse_children(li)}" for li in element.find_all("li", recursive=False)]
            )
        elif element.name == "ol":
            return "\n".join(
                [f"# {parse_children(li)}" for li in element.find_all("li", recursive=False)]
            )
        elif element.name == "a":
            return f"[{element.get_text()}|{element['href']}]"
        elif element.name == "table":
            rows = element.find_all("tr")
            table_markup = []
            for row in rows:
                cells = row.find_all(["th", "td"])
                cell_markup = "|".join([parse_children(cell).strip() for cell in cells])
                table_markup.append(
                    f"||{cell_markup}||" if row.find("th") else f"|{cell_markup}|"
                )
            return "\n".join(table_markup)
        elif element.name == "img":
            return parse_image(element)
        elif element.name == "span" and "style" in element.attrs:
            return parse_span_with_styles(element)
        return element.get_text()

    def parse_children(element):
        if not element.contents:
            return ""
        return "".join(
            [
                parse_element(child) if isinstance(child, Tag) else child
                for child in element.contents
            ]
        )

    def parse_span_with_styles(element):
        style = element["style"]
        color_match = re.search(
            r"color\s*:\s*(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|\w+)", style
        )
        color = color_match.group(1) if color_match else None
        text = parse_children(element)
        if color:
            return f"{{color:{color}}}{text}{{color}}"
        return text

    def parse_image(element):
        src = element.get("src", "")
        alt = element.get("alt", "")
        width = element.get("width", "")
        height = element.get("height", "")

        res = f" !{src}"
        if alt:
            res += f"|alt={alt}"
        if width:
            res += f"|width={width}"
        if height:
            res += f"|height={height}"

        res += "!"
        return res

    for element in soup.body.find_all(recursive=False):
        jira_markup.append(parse_element(element))

    return "\n\n".join(jira_markup)
