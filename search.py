import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import csv
import time
import urllib.parse

# Set up OAuth credentials. Replace 'YOUR_CLIENT_ID' and 'YOUR_CLIENT_SECRET' with your actual credentials.
CLIENT_ID = 'YOUR CLIENT ID'
CLIENT_SECRET = 'YOUR CLIENT SECRET'
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Initialize the YouTube Data API client
def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", SCOPES)
    credentials = flow.run_local_server()
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Function to search for the most popular video for an artist
def search_artist_dj_set(service, artist):
    encoded_artist = urllib.parse.quote(artist)
    search_response = service.search().list(
        q=f"{encoded_artist} dj set",
        type='video',
        part='id',
        maxResults=1,
        order='viewCount'
    ).execute()

    # Wait for a few seconds before the next request
    time.sleep(10)

    if 'items' in search_response and search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return video_url
    else:
        return None

# Load the list of artists from the CSV file
artists_file = r'Your list location goes here'
artists = []
with open(artists_file, 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        artists.extend(row)

# Authenticate and authorize with OAuth
youtube_service = get_authenticated_service()

# Create a CSV file to write the results
output_file = 'results.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Artist', 'Most Popular DJ Set Video']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


    # Search for the most popular video for each artist and write the results to the CSV file
    for artist in artists:
        video_url = search_artist_dj_set(youtube_service, artist)
        if video_url:
            writer.writerow({'Artist': artist, 'Most Popular DJ Set Video': video_url})

print(f'Results written to {output_file}')
