# PubMed Fetcher

A Python-based command-line tool for fetching and analyzing research papers from PubMed, with a focus on identifying non-academic authors and their affiliations.

## Features

- Search PubMed database using custom queries
- Fetch detailed paper information including titles, authors, and publication dates
- Identify non-academic authors and their company affiliations
- Export results to CSV format
- Debug mode for detailed execution logging
- Intelligent author affiliation analysis based on institution keywords

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Prak07/pubmed_paper_fetcher.git
```

2. Install required dependencies:
```bash
pip install -r requirements.txt 
```

## Usage

The tool can be run from the command line with various options:

```bash
python command_line.py "your search query" [-f FILENAME] [-d]
```

### Arguments

- `query`: Required. The search query for PubMed. Use double quotes for queries containing spaces.
- `-f, --file`: Optional. Specify a filename to save results as CSV. If not provided, results will be printed to the console.
- `-d, --debug`: Optional. Enable debug mode to see detailed execution flow.

### Examples

Search for papers about machine learning and display results in console:
```bash
python command_line.py "Cancer"
```

Search for COVID-19 papers and save to CSV with debug mode:
```bash
python command_line.py "COVID-19" -f covid_papers.csv -d
```

## Output Format

The tool provides the following information for each paper:
- PubMed ID
- Title
- Publication Date
- Non-academic Authors (if any)
- Company Affiliations
- Corresponding Author Email

## Author Affiliation Analysis

The tool automatically identifies non-academic authors by analyzing:
- Institution keywords (university, company, etc.)
- Email domains
- Affiliation text

### Keywords Used for Classification

Academic institutions:
- university
- college
- school
- institute
- academy
- research
- lab
- center

Non-academic institutions:
- pharma
- biotech
- corp
- inc
- ltd
- gmbh
- company

## Error Handling

- Includes comprehensive error logging
- Debug mode provides detailed error information
- Graceful handling of API request failures
- UTF-8 encoding support for international character sets

## Requirements

- Python 3.6+
- requests library
- Internet connection for PubMed API access
