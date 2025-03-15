from bs4 import BeautifulSoup, Tag, NavigableString
import re


def html_to_jira(html):
    soup = BeautifulSoup(html, "html.parser")

    # Ensure there's a body tag in the HTML
    if not soup.body:
        soup = BeautifulSoup(f"<body>{html}</body>", "html.parser")

    jira_markup = []

    def parse_element(element, level=0):
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
        elif element.name in ["ul", "ol"]:
            return parse_list(element, level)
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
        """Safely parses child elements without assuming .contents exists"""
        if isinstance(element, NavigableString):
            return element.strip()
        elif isinstance(element, Tag):
            return "".join(
                parse_element(child) if isinstance(child, Tag) else child
                for child in element.contents
            ).strip()
        return ""

    def parse_list(element, level=0):
        """ Recursively parses lists and ensures no duplication """
        prefix = "*" * (level + 1) if element.name == "ul" else "#" * (level + 1)
        items = []

        for li in element.find_all("li", recursive=False):
            # Extract only non-list text from the <li>
            text_parts = [parse_children(child) for child in li.contents if not child.name or child.name not in ["ul", "ol"]]
            item_text = " ".join(filter(None, text_parts))  # Ensure no extra spaces

            # Find nested lists inside the current <li>
            sub_list = li.find(["ul", "ol"])
            if sub_list:
                item_text += "\n" + parse_list(sub_list, level + 1)

            items.append(f"{prefix} {item_text}")

        return "\n".join(items)

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