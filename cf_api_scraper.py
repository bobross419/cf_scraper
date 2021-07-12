import json
import requests
from bs4 import BeautifulSoup
from pysondb import db
from threading import thread

athlete_db = 'db/athlete.json'
affiliate_db = 'db/affiliate.json'
affiliate_url = 'https://games.crossfit.com/affiliate/'

def add_athlete_to_db( athlete ):
    db.getDb(athlete_db).add(athlete)

def add_athletes_to_db( atheletes ):
    db.getDB(affiliate_db).addMany(athletes)

def add_affiliate_to_db( affiliate ):
    db.getDb(affiliate_db).add(affiliate)

def get_athletes_from_db():
    return db.getDb(athlete_db).getAll()

def get_affiliates_from_db():
    return db.getDb(affiliate_db).getAll()

def fetch_page( url ):
    rec = requests.get(url)
    return rec

def fetch_affiliate( affiliate_id ):
    pdata = fetch_page( affiliate_url + affiliate_id )
    soup = BeautifulSoup(pdata.text)
    infobar = soup.find(class_='infobar')
    for i in infobar.find_all('li'):
        if i.find(class_='item-label').text == 'LOCATION':
            return i.find(class_='text').text
    return "Unable to find location"

def get_total_pages( url ):
    pdata = fetch_page( url ).json()
    return pdata['pagination']['totalPages']

def get_competition_threaded( year, division, scaled ):
    api_years = { 
            '2018': 'v1',
            '2019': 'v1',
            '2020': 'v1',
            '2021': 'v2' }
    api_roots = {
            'v1': 'https://games.crossfit.com/competitions/api/v1',
            'v2': 'https://c3po.crossfit.com/api/competitions/v2'}
    api_comp_string =  '/competitions/open/'
    api_search_string = '/leaderboards?scaled=' + str(scaled) + '&division=' + str(division) + '&page='

    api_root = api_roots[api_years[year]]
    api_url = api_root + api_comp_string + year + api_search_string

    athletes = []

    total_pages = get_total_pages( api_url + '1' )
    threads = 4

    for i in range(1, threads + 1):
        start = ( total_pages * (i - 1) ) + 1
        end = total_pages


    for page in range(1, get_total_pages( api_url + '1') + 1):
        pdata = fetch_page( api_url + str(page) ).json()
        for row in pdata['leaderboardRows']:
            athlete = row['entrant']
            athlete.update({ 'overallRank': row['overallRank']})
            athletes.append(athlete)
            #add_athlete_to_db(athlete)
        add_athletes_to_db(athletes)
def get_competition( year, division, scaled ):

    api_years = { 
            '2018': 'v1',
            '2019': 'v1',
            '2020': 'v1',
            '2021': 'v2' }
    api_roots = {
            'v1': 'https://games.crossfit.com/competitions/api/v1',
            'v2': 'https://c3po.crossfit.com/api/competitions/v2'}
    api_comp_string =  '/competitions/open/'
    api_search_string = '/leaderboards?scaled=' + str(scaled) + '&division=' + str(division) + '&page='

    api_root = api_roots[api_years[year]]
    api_url = api_root + api_comp_string + year + api_search_string

    athletes = []

    for page in range(1, get_total_pages( api_url + '1') + 1):
        pdata = fetch_page( api_url + str(page) ).json()
        for row in pdata['leaderboardRows']:
            athlete = row['entrant']
            athlete.update({ 'overallRank': row['overallRank']})
            athletes.append(athlete)
            #add_athlete_to_db(athlete)
        add_athletes_to_db(athletes)

def in_affiliate_db(affiliate_id, affiliates):
    return any(d['id'] == affiliate_id for d in affiliates)
    #if affiliate_id in affiliates["id"]: return true
    #return false

def populate_athletes():
    div, scale, page = 0, 0, 0
    years = ['2018', '2019', '2020', '2021']
    divisions = [ '0', '1' ]
    scales = [ '0', '1' ]
    for year in years:
        for division in divisions:
            for scale in scales:
                get_competition( year, division, scale )

def populate_affiliates():
    athletes = get_athletes_from_db()
    affiliates = get_affiliates_from_db()
    for athlete in athletes:
        affiliate_id = athlete['affiliateId']
        if in_affiliate_db(affiliate_id, affiliates):
            next
        affiliate = fetch_affiliate(affiliate_id)
        add_affiliate_to_db(affiliate)
        
#populate_athletes()
populate_affiliates()
