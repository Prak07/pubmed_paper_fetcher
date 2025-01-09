import argparse
import logging
from research_paper_fetcher import *


# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
parser.add_argument("query", type=str, help="Search query for PubMed and add double quotes if u are writing a query containing spaces.")
parser.add_argument("-f", "--file", type=str, help="Filename to save results as CSV.This is an opptional argument if not entered all the data will be printed in the shell.")
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.To see the flow of execution of the program.")
args = parser.parse_args()

if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)

try:
    papers = fetch_papers(args.query, debug=args.debug)
    if args.file:
        save_to_csv(papers, args.file, debug=args.debug)
        logging.info(f"Results saved to {args.file}")
    else:
        for paper in papers:
            print(paper)
except Exception as e:
    logging.error("An error occurred", exc_info=args.debug)

