# third-party
import urllib.request
from bs4 import BeautifulSoup


def search_yt(textToSearch):
    """Searches youtube for a given song

    Args:
        textToSearch (Str): text that is going to be searched for
                            on youtube

    Returns:
        Str: url for song that was found
    """
    query = urllib.parse.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    vid = soup.find(attrs={'class':'yt-uix-tile-link'})
    return ('https://www.youtube.com' + vid['href'])
