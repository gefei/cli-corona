# cli-corona

Cli tool to generate up-to-date diagram of corona data.

## Data source
`https://interaktiv.morgenpost.de/data/corona/history.light.v4.csv`

## usage
`python3 cli-corona.py [-h] [--daily] [--ave AVE] [--per100k] [--width WIDTH] [--height HEIGHT] [--png PNG] [--html HTML] [--show] countries [countries ...]`

### positional arguments

  `countries        countries to track in the diagram`

### optional arguments
  ```
  -h, --help       show this help message and exit
  --daily          if set, include daily new cases, otherwise include cumulative number of cases
  --ave AVE        include AVE day rolling average. Effective only when --daily is set. Default=7
  --per100k        normalize the numbers to 100k population
  --width WIDTH    width of the diagram
  --height HEIGHT  height of the diagram
  --png PNG        if set, diagram in png will be saved under this name
  --html HTML      if set, html output will be saved under this name
  --show           if set, diagram will be shown in the browser. Only effective when --html is set
  ```
