# cli-corona

Cli tool to generate up-to-date diagram of corona data.

## Data source
`https://interaktiv.morgenpost.de/data/corona/history.light.v4.csv`

## usage
```
python3 cli-corona.py [-h] [--ids [IDS [IDS ...]]] [--search [SEARCH [SEARCH ...]]] [--col COL]
                             [--daily] [--ave AVE] [--cumu] [--per100k] [--width WIDTH] [--height HEIGHT]
                             [--start START] [--end END] [--png PNG] [--html HTML] [--show]

```

### optional arguments
  ```
  -h, --help            show this help message and exit
  --ids [IDS [IDS ...]]
                        ids of regions to track in the diagram. Country ids are ISO 3166-1 alpha-2 codes. See
                        also --search
  --search [SEARCH [SEARCH ...]]
                        search for id
  --col COL             one of "confirmed", "recovered", or "deaths"
  --daily               if set, include daily new cases, otherwise include cumulative number of cases
  --ave AVE             include AVE day rolling average
  --cumu                if set, include cumulative numbers
  --per100k             normalize the numbers to 100k population
  --width WIDTH         width of the diagram
  --height HEIGHT       height of the diagram
  --start START         first day to track. Format: yyyymmdd
  --end END             last day to track. Format: yyyymmdd
  --png PNG             if set, diagram in png will be saved under this name
  --html HTML           if set, html output will be saved under this name
  --show                if set, diagram will be shown in the browser. Only effective when --html is set
  ```
