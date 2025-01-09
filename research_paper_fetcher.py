import requests
import csv
import logging

def identify_non_academic_authors(authors):
    """
    Identify non-academic authors from a list of authors with their affiliations and emails.

    Args:
        authors (list of dict): List of author dictionaries with 'name', 'affiliation', and 'email'.

    Returns:
        tuple: (non_academic_authors, company_affiliations)
    """
    non_academic_authors = []
    company_affiliations = []

    # Define keywords for academic and non-academic institutions
    academic_keywords = r"(university|college|school|institute|academy|research|lab|center)"
    non_academic_keywords = r"(pharma|biotech|corp|inc|ltd|gmbh|company)"
    
    for author in authors:
        affiliation = author.get("affiliation", "").lower()
        email = author.get("email", "").lower()
        name = author.get("name", "Unknown")

        # Check affiliation for non-academic keywords
        if any(keyword in affiliation for keyword in non_academic_keywords):
            non_academic_authors.append(name)
            company_affiliations.append(affiliation)
        elif not any(keyword in affiliation for keyword in academic_keywords):
            # Use email domain as a secondary heuristic
            if email and not email.endswith(".edu"):
                non_academic_authors.append(name)
                company_affiliations.append(affiliation)

    return non_academic_authors, company_affiliations

def fetch_papers(query, debug=False):
    """Fetch research papers from PubMed API based on a query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    details_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    if debug:
        logging.debug(f"Fetching papers for query: {query}")

    # Search for papers
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10,
    }
    try:
        search_response = requests.get(base_url, params=search_params)
        search_response.raise_for_status()
        search_results = search_response.json()
        paper_ids = search_results["esearchresult"]["idlist"]
        if debug:
            logging.debug(f"Found paper IDs: {paper_ids}")

        # Fetch paper details
        details_params = {
            "db": "pubmed",
            "id": ",".join(paper_ids),
            "retmode": "json",
        }
        details_response = requests.get(details_url, params=details_params)
        details_response.raise_for_status()
        details_results = details_response.json()["result"]

        papers = []
        for paper_id in paper_ids:
            paper = details_results[paper_id]
            authors = paper.get("authors", [])
            
            # Identify non-academic authors
            non_academic_authors, company_affiliations = identify_non_academic_authors(authors)

            papers.append({
                "PubmedID": paper_id,
                "Title": paper["title"],
                "Publication Date": paper.get("sortpubdate", "Unknown"),
                "Non-academic Authors": "; ".join(non_academic_authors),
                "Company Affiliations": "; ".join(company_affiliations),
                "Corresponding Author Email": paper.get("elocationid", "Unknown"),
            })
        return papers
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def save_to_csv(papers, filename, debug=False):
    """Save papers to a CSV file."""
    if debug:
        logging.debug(f"Saving papers to file: {filename}")

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)

    if debug:
        logging.debug(f"Saved {len(papers)} papers to {filename}")

