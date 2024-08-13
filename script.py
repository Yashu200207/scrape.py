import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL
url = 'https://hprera.nic.in/PublicDashboard'

try:
    # Send a GET request to the website with SSL verification disabled (for debugging)
    response = requests.get(url, verify=False)
    response.raise_for_status()  # Raise HTTPError for bad responses
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the section containing the projects
    projects_section = soup.find('section', {'id': 'registered_projects'})  # Update the ID or class as needed

    # Ensure the projects_section is not None
    if projects_section:
        # Get the list of projects
        projects = projects_section.find_all('a', class_='project-link')  # Update the class as needed

        data = []
        for project in projects[:6]:
            project_url = project['href']
            project_response = requests.get(project_url, verify=False)
            project_response.raise_for_status()  # Raise HTTPError for bad responses
            project_soup = BeautifulSoup(project_response.content, 'html.parser')
            
            # Extract details from the project page
            gstin_no = project_soup.find(text='GSTIN No')
            pan_no = project_soup.find(text='PAN No')
            name = project_soup.find(text='Name')
            permanent_address = project_soup.find(text='Permanent Address')

            # Check if elements are found and extract text
            gstin_no = gstin_no.find_next().text.strip() if gstin_no and gstin_no.find_next() else 'N/A'
            pan_no = pan_no.find_next().text.strip() if pan_no and pan_no.find_next() else 'N/A'
            name = name.find_next().text.strip() if name and name.find_next() else 'N/A'
            permanent_address = permanent_address.find_next().text.strip() if permanent_address and permanent_address.find_next() else 'N/A'

            data.append({
                'GSTIN No': gstin_no,
                'PAN No': pan_no,
                'Name': name,
                'Permanent Address': permanent_address
            })

        # Save the data to a CSV file
        df = pd.DataFrame(data)
        df.to_csv('projects_details.csv', index=False)

        print('Scraping complete. Data saved to projects_details.csv')
    else:
        print('Projects section not found on the webpage.')

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
