import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import uuid
import openai

# Initialize OpenAI API key
openai.api_key = 'your-api-key-here'

# Function to fetch content from a URL and remove HTML tags
def fetch_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Remove HTML tags and extract text
            text = soup.get_text(separator=' ')
            return text
        else:
            print(f"Failed to fetch URL: {url}")
            return None
    except Exception as e:
        print(f"Error processing URL {url}: {str(e)}")
        return None

# Function to generate summary using GPT-3.5
def generate_summary(text):
    try:
        # Generate summary using GPT-3.5
        response = openai.Completion.create(
            engine="davinci",
            prompt=text,
            max_tokens=100
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return None

# Function to fetch HTML content from a URL
def fetch_html_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to fetch HTML content from {url}")
            return None
    except Exception as e:
        print(f"Error fetching HTML content from {url}: {str(e)}")
        return None

# Function to extract information from HTML content
def extract_information(html_content):
    if html_content:
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Extract title
            title = soup.title.text.strip()
            # Extract description meta tag
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag['content'].strip() if description_tag else ""
            # Extract additional attributes
            additional_info = {}
            # You can add code here to extract additional attributes from the HTML content
            return title, description, additional_info
        except Exception as e:
            print(f"Error extracting information: {str(e)}")
            return None, None, None
    else:
        return None, None, None

# Function to analyze HTML content using GPT-3.5 and extract relevant attributes
def analyze_with_gpt(html_content):
    # Process the HTML content
    # For demonstration, let's assume we're analyzing the content for standard attributes using GPT-3.5
    gpt_predicted_attributes = {
        "status": "Open",
        "stages": "Planning",
        "procurementMethod": "Unknown",
        "budget": 0.0,
        "currency": "USD",
        "buyer": "Unknown",
        "sector": "Unknown",
        "subsector": "Unknown"
    }
    return gpt_predicted_attributes

# Function to standardize data according to Table 2
def standardize_data(title, description, additional_info, gpt_predicted_label, url):
    aug_id = str(uuid.uuid4())  # Generate UUID
    country_name = "United States"
    country_code = "USA"
    map_coordinates = {"type": "Point", "coordinates": [-122.4, 37.8]}  # Default coordinates for demonstration
    region_name = "California"
    region_code = "CA"
    status = additional_info.get("status", "Open")
    stages = additional_info.get("stages", "Planning")
    date = datetime.now().strftime("%Y-%m-%d")  # Current date
    procurement_method = additional_info.get("procurementMethod", "Unknown")
    budget = additional_info.get("budget", 0.0)
    currency = additional_info.get("currency", "USD")
    buyer = additional_info.get("buyer", "Unknown")
    sector = additional_info.get("sector", "Unknown")
    subsector = additional_info.get("subsector", "Unknown")

    # Analyze description with GPT-3.5
    gpt_predicted_label = gpt_predicted_label or analyze_with_gpt(description)

    # Construct standardized data as dictionary
    standardized_data = {
        "aug_id": aug_id,
        "country_name": country_name,
        "country_code": country_code,
        "map_coordinates": map_coordinates,
        "url": url,
        "region_name": region_name,
        "region_code": region_code,
        "title": title,
        "description": description,
        "status": status,
        "stages": stages,
        "date": date,
        "procurementMethod": procurement_method,
        "budget": budget,
        "currency": currency,
        "buyer": buyer,
        "sector": sector,
        "subsector": subsector,
        "gpt_predicted_label": gpt_predicted_label
    }
    return standardized_data

# Function to write standardized data to CSV file
def write_to_csv(data_list, file_name):
    if data_list:
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = data_list[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for data in data_list:
                    writer.writerow(data)
            print(f"Standardized data has been written to {file_name}")
        except Exception as e:
            print(f"Error writing to CSV: {str(e)}")
    else:
        print("No data to write to CSV")

# Main function
def main():
    urls = []
    with open('std_data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            urls.append(row['Source URL'])

    # Fetch content, generate summaries, and select top links based on relevance
    summaries = []
    for url in urls:
        print
