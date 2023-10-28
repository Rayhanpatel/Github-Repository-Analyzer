import subprocess

# Define the command to install matplotlib
install_command = "pip install matplotlib"

# Run the command using subprocess
subprocess.run(install_command, shell=True)


import streamlit as st
import requests
import json
import matplotlib.pyplot as plt

# Create a Streamlit app
st.title("GitHub Repository Analyzer")

# Input fields for owner and repo
owner = st.text_input("Enter owner name:")
repo = st.text_input("Enter repository name:")

if owner and repo:
    # Step 1: Set up authentication
    token = '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'
    headers = {'Authorization': f'token {token}'}

    # Step 2: Make an API request to get repository information
    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.get(url, headers=headers)

    # Step 3: Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # Step 4: Extract relevant information
        repository_info = {
            "Repository Name": data['name'],
            "Description": data['description'],
            "Stargazers Count": data['stargazers_count'],    # Stargazers highlight the GitHub users' profiles who starred the repository
            "Forks Count": data['forks_count'],
            "Watchers Count": data['watchers_count'],
            "Primary Language": data['language']
        }

        # Display repository information in the app
        st.subheader("Repository Information")
        st.write("Repository Name:", repository_info["Repository Name"])
        st.write("Description:", repository_info["Description"])
        st.write("Stargazers Count:", repository_info["Stargazers Count"])
        st.write("Forks Count:", repository_info["Forks Count"])
        st.write("Watchers Count:", repository_info["Watchers Count"])
        st.write("Primary Language:", repository_info["Primary Language"])

        # Step 10: Visualize the Data
        st.subheader("Repository Engagement Metrics")
        st.bar_chart({
            'Stargazers': repository_info["Stargazers Count"],
            'Forks': repository_info["Forks Count"],
            'Watchers': repository_info["Watchers Count"]
        })

        # Step 11: Draw Conclusions
        stargazers_count = repository_info["Stargazers Count"]
        forks_count = repository_info["Forks Count"]

        if stargazers_count > 0 and forks_count > 0:
            stargazers_per_fork = stargazers_count / forks_count

            if stargazers_per_fork > 5:
                conclusion = "This repository has a high ratio of stargazers to forks, indicating strong interest from the community."
            else:
                conclusion = "The ratio of stargazers to forks suggests moderate community interest in this repository."
        else:
            conclusion = "Insufficient data to draw conclusions."

        # Display the conclusion
        st.subheader("Conclusion")
        st.write(conclusion)

    else:
        st.error(f"Error: Unable to retrieve repository information. Status code {response.status_code}")
