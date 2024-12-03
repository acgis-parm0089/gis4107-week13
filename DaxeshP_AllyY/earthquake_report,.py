import os
import requests
 
# URL for the ATOM feed
ATOM_FEED_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.atom"
 
def get_earthquake_data(out_atom_filename):
    """
    Downloads the ATOM feed data if the local file does not already exist.
   
    :param out_atom_filename: Path to save the downloaded ATOM feed.
    """
    # Check if the file already exists
    if os.path.exists(out_atom_filename):
        print(f"{out_atom_filename} already exists. Skipping download.")
        return
 
    # Download the ATOM feed
    print(f"Downloading ATOM feed from {ATOM_FEED_URL}...")
    response = requests.get(ATOM_FEED_URL)
   
    if response.status_code == 200:
        # Save the feed to the specified file
        with open(out_atom_filename, "wb") as file:
            file.write(response.content)
        print(f"ATOM feed saved to {out_atom_filename}.")
    else:
        print(f"Failed to download ATOM feed. HTTP status code: {response.status_code}")