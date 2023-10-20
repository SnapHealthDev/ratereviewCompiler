import requests
import csv

# Base URL for the API
base_url = "https://ratereview.healthcare.gov/ratereviewservices/urr/submissions"

# List of state codes to iterate through
state_codes = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

# Get the year from the user
year = input("Which year are you searching for? ")

# Market type
market_type = "Individual"

# Initialize a list to store the results
results = []

# Iterate through each state code
for state_code in state_codes:
    # Create the URL for the request
    url = f"{base_url}?state={state_code}&year={year}&marketType={market_type}"
    
    # Make the request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Iterate through each submission
        for submission in data.get("submissionsList", []):
            # Add full URL to the files
            if submission.get('redactedActuarialMemorandumURL'):
                submission['redactedActuarialMemorandumURL'] = 'https://ratereview.healthcare.gov/' + submission['redactedActuarialMemorandumURL']
            if submission.get('cjnURL'):
                submission['cjnURL'] = 'https://ratereview.healthcare.gov/' + submission['cjnURL']
            # Add the result to the list
            results.append(submission)
    else:
        print(f"Failed to get data for state code {state_code}. Status code: {response.status_code}")

# Write the results to a CSV file
with open(year + ' Plan Data from RateReview_Healthcare_gov.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = [
        'submissionIdentifier', 'effectiveDate', 'redactedActuarialMemorandumURL', 
        'currentStatusDate', 'finalDetermination', 'issuerCode', 'issuerName', 
        'issuerResponseComments', 'marketType', 'modifiedRate', 'cjnURL', 
        'narrativeComments', 'ffmPlans', 'primCode', 'reviewPeriod', 'reviewStatus', 
        'reviewStatusCode', 'reviewerComments', 'stateCode', 'stateName', 
        'threshold_rate_min_increase', 'threshold_rate_max_increase', 
        'submission_average_rate_prelim', 'submission_average_rate_final', 'productCount'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print("Results have been saved to " + year + " Plan Data from RateReview_Healthcare_gov.csv")
