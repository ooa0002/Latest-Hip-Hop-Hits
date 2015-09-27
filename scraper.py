import requests
import bs4
import re
from multiprocessing import pool
from datetime import date, timedelta
from multiprocessing import Pool
import timeit

root_url = 'http://www.hotnewhiphop.com'
index_url = root_url + '/archive/'
date_ext =""
songs = []
artistName = ""
artistList = ["Drake", "Rick Ross"]


def get_ArtistName():
    global artistName
    return artistName

def duplicateRemover(inputList):
    seen = set()
    seen_add = seen.add
    return[x for x in inputList if not(x in seen or seen_add(x))]

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
        #print(songText)
        if "Feat" not in songText:
            tempStringList = songText.split(' - ')
            songsAndArtists[tempStringList[1]] = [tempStringList[0]] 
        else:
            if "-" not in songText:
                continue
            artistsList = []
            tempStringList = songText.split(' - ')
            artistsList.append(tempStringList[0])
            #artists = []
            tempStringList2 = tempStringList[1].split(' Feat. ')
            artistsString = tempStringList2[1]
            if ',' not in artistsString:
                artistsList.append(artistsString)
            else:
                moreArtists = artistsString.split(', |& ')
                for writer in moreArtists:
                    artistsList.append(writer)

            songsAndArtists[tempStringList2[0]] = artistsList
                
    return songsAndArtists;

def get_ArtistsSongs(artistNames):
    inputArtists = artistNames
    songList = []
    songsAndArtists = parseArtistsHNHH(inputArtists)
    #print(songsAndArtists)
    for key, value in songsAndArtists.items():
        if inputArtists in value:
            tempStr = key + " - " + "Artists: "
            seperator = ", "
            artists = seperator.join(value)
            songList.append(tempStr + artists)
    #print(songList)
    return songList



#print (get_ArtistSongs(artistName))
#print (parseArtistsHNHH(artistName))

def get_Dates():
    today = date.today()
    dates = []
    for x in range(12):
        tempDate = today - timedelta(days=x*7)
        dates.append(tempDate)
    return dates

#print(datesList)


def getDataHNHH(dateInput):
    global date_ext
    date_ext = str(dateInput)
    print(date_ext)
    #print(get_ArtistSongs(artistName))
    songList = get_ArtistsSongs(artistName)
    return songList

def get_Songs():
    pool = Pool(processes=8)
    global date_ext
    datelist = get_Dates()
    # for x in range(len(datelist)):
    #     date_ext = str(datelist[x])
    #     print(date_ext)
    #     songs.extend(get_ArtistSongs(artistName))
    songs = pool.map(getDataHNHH, datelist)
    songs = [ent for sublist in songs for ent in sublist]
    print(songs)
    return songs

def get_SongsMultipleArtists():
    for artist in artistList:
        global artistName
        artistName = artist
        get_Songs()

tic = timeit.default_timer()
get_SongsMultipleArtists()
toc = timeit.default_timer()
print(toc-tic)


