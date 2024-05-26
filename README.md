# HTML to Jira Wiki Markup Converter

[![PyPI version](https://badge.fury.io/py/html-to-jira.svg)](https://badge.fury.io/py/html-to-jira)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package that converts HTML content to Jira Wiki Markup format. It supports various HTML elements including headers, paragraphs, lists, links, tables, inline styles, and images within table cells.

## Features

- Converts HTML headers (`<h1>`, `<h2>`, `<h3>`) to Jira Wiki headers.
- Converts paragraphs (`<p>`) and inline text styles (`<em>`, `<strong>`, `<span style="color">`).
- Converts unordered lists (`<ul>`) and ordered lists (`<ol>`) to Jira Wiki lists.
- Converts links (`<a>`) to Jira Wiki link format.
- Converts tables (`<table>`, `<tr>`, `<th>`, `<td>`) to Jira Wiki table format.
- Supports images (`<img>`) within table cells.

## Installation

You can install the package via pip:

```bash
pip install html-to-jira
```

## Usage
### Converting HTML to Jira Wiki Markup

You can use the html_to_jira function from the html_to_jira package to convert your HTML content to Jira Wiki Markup.

```python
from html_to_jira.converter import html_to_jira

html_string = '''
<h1>Welcome to Jira!</h1>
<p>This is a <em>sample</em> HTML string with <strong>bold</strong> text and <span style="color:red;">colored text</span>.</p>
<ul>
  <li>Item 1 with <strong>bold</strong> text</li>
  <li>Item 2 with <span style="color:blue;">colored text</span></li>
</ul>
<ol>
  <li>First with <em>italic</em> text</li>
  <li>Second with <span style="color:green;">green text</span></li>
</ol>
<p>Visit <a href="https://example.com">this link</a> for more information.</p>
<table>
  <tr>
    <th>Heading 1</th>
    <th>Heading 2</th>
  </tr>
  <tr>
    <td>Col A1 with <strong>bold</strong> text</td>
    <td>Col A2 with <span style="color:purple;">purple text</span> and <img src="https://example.com/image.png" alt="Example Image"></td>
  </tr>
</table>
'''

jira_markup = html_to_jira(html_string)
print(jira_markup)
```

### Example Output
```python
h1. Welcome to Jira!

This is a _sample_ HTML string with *bold* text and {color:red}colored text{color}.

* Item 1 with *bold* text
* Item 2 with {color:blue}colored text{color}

# First with _italic_ text
# Second with {color:green}green text{color}

Visit [this link|https://example.com] for more information.

||Heading 1|Heading 2||
|Col A1 with *bold* text|Col A2 with {color:purple}purple text{color} and !https://example.com/image.png|alt=Example Image!|
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.