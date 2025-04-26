# currency-calculator

Simple python GUI project using `tkinter` capable of:
- Currency conversion based on Central Bank of Russia (CBR) data
- Displaying exchange rate dynamics for selected currency over a specified period


## Features
- Real-time currency conversion 
- Historical rate visualization (April 2024 dataset)
- Interactive GUI with tkinter

## Data Relevance
| Data Type          | Status            | Details                          |
|--------------------|-------------------|----------------------------------|
| Exchange rates     | 🔄 Live           | Updates on startup               |
| Rate dynamics data | ⏳ Snapshot       | April 2024 version               |

## Dependencies

* matplotlib
* pandas
* numpy

## Try it out


```bash
python main.py
```

## Notes

- Data source: [CBR XML API (ЦБ РФ)](https://www.cbr.ru/development/SXML/)
- Requires active internet connection
