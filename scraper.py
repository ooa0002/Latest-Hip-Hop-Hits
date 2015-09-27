import requests
import bs4
import re
from multiprocessing import pool
from datetime import date, timedelta
from multiprocessing import Pool
import timeit

#url of the source website
root_url = 'http://www.hotnewhiphop.com'
index_url = root_url + '/archive/'
date_ext =""
#list that will ultimately be returned
songs = []
artistName = ""
#list of artists: this can be modified to include any artists
artistList = ["Drake", "Rick Ross"]


def get_ArtistName():
    global artistName
    return artistName

#removes duplicates that are returned when scraping the website
def duplicateRemover(inputList):
    seen = set()
    seen_add = seen.add
    return[x for x in inputList if not(x in seen or seen_add(x))]

#gets the title attributes from the hotnewhiphop webpage
#this attribute contains that song title along with the artist's name
def get_HNHH():
    global date_ext
    response = requests.get(index_url+date_ext)
    soup = bs4.BeautifulSoup(response.text)
    rawList =  [li.attrs.get('title') for li in soup.select('li.songChart a[title]')]
    return duplicateRemover(rawList)
    
def parseArtistsHNHH(artist_Name):
    songs = get_HNHH()
    songsAndArtists = {}
    for songText in songs:
        #if the song was produced by a single artist then simply get the artist name following the '-'
        if "Feat" not in songText:
            tempStringList = songText.split(' - ')
            songsAndArtists[tempStringList[1]] = [tempStringList[0]]
        #otherwise get all the artists names following 'Feat'
        else:
            if "-" not in songText:
                continue
            #list that will contain all of the artists
            artistsList = []
            #split the string from the title attribute to get the artist's name
            tempStringList = songText.split(' - ')
            artistsList.append(tempStringList[0])
            #split the resulting string
            tempStringList2 = tempStringList[1].split(' Feat. ')
            #add the artist that appears before 'Feat' to the list
            artistsString = tempStringList2[1]
            #checks to see if there are multiple artists featured on the sogn
            if ',' not in artistsString:
                artistsList.append(artistsString)
            else:
                moreArtists = artistsString.split(', |& ')
                for writer in moreArtists:
                    artistsList.append(writer)
#adds the song as the key and and the artistsList as the value
            songsAndArtists[tempStringList2[0]] = artistsList
                
    return songsAndArtists;

def get_ArtistsSongs(artistNames):
    inputArtists = artistNames
    songList = []
    songsAndArtists = parseArtistsHNHH(inputArtists)
    #adds the song to the list to be returned if the Artist appears in the list of artists
    for key, value in songsAndArtists.items():
        if inputArtists in value:
            tempStr = key + " - " + "Artists: "
            seperator = ", "
            artists = seperator.join(value)
            songList.append(tempStr + artists)
    return songList


def get_Dates():
    today = date.today()
    dates = []
    for x in range(12):
        tempDate = today - timedelta(days=x*7)
        dates.append(tempDate)
    return dates

def getDataHNHH(dateInput):
    global date_ext
    date_ext = str(dateInput)
    
    songList = get_ArtistsSongs(artistName)
    return songList

def get_Songs():
    #multiprocessing to improve speed
    pool = Pool(processes=8)
    global date_ext
    datelist = get_Dates()
    songs = pool.map(getDataHNHH, datelist)
    songs = [ent for sublist in songs for ent in sublist]
    print(songs)
    return songs

def get_SongsMultipleArtists():
    for artist in artistList:
        global artistName
        artistName = artist
        get_Songs()

#evaluates the time needed to complete the operation
tic = timeit.default_timer()
get_SongsMultipleArtists()
toc = timeit.default_timer()
print(toc-tic)


