"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie - Datový analytik s pythonem

author: Monika Matějková
email: moncinas@centrum.cz
"""

import requests
from bs4 import BeautifulSoup
import argparse
import re
import csv
import os
import locale

locale.setlocale(locale.LC_NUMERIC, "cs_CZ.UTF-8")

def validate_url(url: str) -> bool:
    """Validates URL by making a GET request and checking for a 200 response."""
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def validate_command_line_arguments() -> tuple:
    """Validates command-line arguments for URL and file name."""
    parser = argparse.ArgumentParser(description="Validate command-line arguments.")
    parser.add_argument("url", type=str, help="URL to be validated.")
    parser.add_argument("file_name", type=str, help="File name to be validated.")
    args = parser.parse_args()

    url, file_name = args.url, args.file_name

    expected_core_url = "https://www.volby.cz/pls/ps2017nss/"
    if not url.startswith(expected_core_url):
        raise ValueError(f'Invalid URL. Expected it to start with "{expected_core_url}", but got "{url}"')

    if not file_name.endswith(".csv"):
        raise ValueError(f"Invalid file type. Expected .csv, but got {os.path.splitext(file_name)[1]}")

    if not validate_url(url):
        raise ValueError(f"Invalid URL: {url}")

    return url, file_name

def scrape_city_names(url: str) -> tuple:
    """Scrapes city codes and names from the given URL."""
    response = requests.get(url)
    doc = BeautifulSoup(response.text, "html.parser")
    
    city_codes = [city.text.strip() for city in doc.find_all("td", class_="cislo")]
    city_names = [city.text.strip() for city in doc.find_all("td", class_="overflow_name")]
    
    return city_codes, city_names

def get_city_urls(url: str) -> list:
    """Extracts city-specific URLs from the base election results page."""
    core_url = "https://www.volby.cz/pls/ps2017nss/"
    response = requests.get(url)
    doc = BeautifulSoup(response.text, "html.parser")
    city_urls = [core_url + a["href"] for a in doc.select("td.cislo a")]

    return city_urls

def collect_voter_turnout_data(city_urls: list) -> tuple:
    """Collects voter turnout data from each city."""
    registered_voters, ballot_papers, valid_votes = [], [], []

    for url in city_urls:
        response = requests.get(url)
        doc = BeautifulSoup(response.text, "html.parser")

        registered_voters.append(doc.find("td", headers="sa2").text.replace("\xa0", ""))
        ballot_papers.append(doc.find("td", headers="sa3").text.replace("\xa0", ""))
        valid_votes.append(doc.find("td", headers="sa6").text.replace("\xa0", ""))

    return registered_voters, ballot_papers, valid_votes

def get_political_parties(city_url: str) -> list:
    """Extracts a list of political parties from the first city URL."""
    response = requests.get(city_url)
    doc = BeautifulSoup(response.text, "html.parser")
    
    parties = [party.text.strip() for party in doc.select("td.overflow_name[headers*=t]")]
    return parties

def collect_vote_counts(city_urls: list, num_parties: int) -> list:
    """Collects vote counts for each political party in every city."""
    total_votes = []

    for url in city_urls:
        response = requests.get(url)
        doc = BeautifulSoup(response.text, "html.parser")

        votes = [vote.text.replace("\xa0", "") for vote in doc.select("td.cislo[headers*=t]")]

        while len(votes) < num_parties:
            votes.append("0")

        total_votes.append(votes)
    
    return total_votes

def write_to_csv(file_name: str, city_codes: list, city_names: list, data_collection: tuple, political_parties: list, total_votes: list) -> None:
    """Writes the collected data into a CSV file with properly formatted output."""
    headers = ["City Code", "City Name", "Registered Voters", "Issued Ballots", "Valid Votes"] + political_parties

    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=";")  
        writer.writerow(headers)

        for i in range(len(city_codes)):
            row = [
                city_codes[i], city_names[i],
                data_collection[0][i], data_collection[1][i], data_collection[2][i]
            ] + total_votes[i]

            writer.writerow(row)

    print(f"File '{file_name}' has been successfully created and saved.")

def main() -> None:
    """Main function orchestrating data extraction and CSV writing."""
    try:
        url, file_name = validate_command_line_arguments()
        print(f'Initializing program with URL "{url}" and file name "{file_name}"\nExtracting data...')

        city_codes, city_names = scrape_city_names(url)
        city_urls = get_city_urls(url)
        data_collection = collect_voter_turnout_data(city_urls)
        political_parties = get_political_parties(city_urls[0])
        total_votes = collect_vote_counts(city_urls, len(political_parties))

        print(f"Expected columns: {len(political_parties) + 5}")
        print(f"First row columns: {len([city_codes[0], city_names[0]] + data_collection[0][0:1] + data_collection[1][0:1] + data_collection[2][0:1] + total_votes[0])}")

        write_to_csv(file_name, city_codes, city_names, data_collection, political_parties, total_votes)

    except ValueError as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()
