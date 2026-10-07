import re

with open('docs/METHODOLOGY.md', 'r') as f:
    text = f.read()

text = text.replace('subgraph Raw Anomalies', 'subgraph raw [Raw Anomalies]')
text = text.replace('subgraph Parsers (src/cleaning/)', 'subgraph parsers [Parsers src/cleaning]')
text = text.replace('subgraph Clean Types', 'subgraph clean_types [Clean Types]')

with open('docs/METHODOLOGY.md', 'w') as f:
    f.write(text)

