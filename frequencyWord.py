import requests
from bs4 import BeautifulSoup
import operator
import bs4
from urllib.request import urlopen
import folium as folium
from geopy.geocoders import Nominatim
import webbrowser


def start(url):
    word_list = []
    source_code = requests.get(url).text
    soup = BeautifulSoup(source_code, 'lxml')
    for post_text in soup.findAll('p'):
        content = post_text.text
        words = content.lower().split()
        for each_word in words:
            word_list.append(each_word)
    word_count = clean_up_list(word_list)
    return word_count


# clean up word-list by removing symbols and empty words
def clean_up_list(word_list):
    clean_word_list = []
    for word in word_list:
        symbols = "1234567890!@#$%^&*()-=_+{}[]|\;':\",./<>?'"
        for i in range(0, len(symbols)):
            word = word.replace(symbols[i], "")
        if len(word) > 3:
            clean_word_list.append(word)
    word_count = create_dictionary(clean_word_list)
    return word_count


# create dictionary with words as key and frequency as value, sorted by value
def create_dictionary(clean_word_list):
    word_count = {}
    for word in clean_word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


def final_result(lista_risultati):
    tot_word_count = {}
    i = 0
    while i < len(lista_risultati):
        for key, value in sorted(lista_risultati[i], key=operator.itemgetter(1)):
            if key != 'della' and key != 'delle' and key != 'dalla' and key != 'dalle' and key != 'alla' \
                    and key != 'alle' and key != 'nella' and key != 'nelle' and key != 'sulla' and key != 'sulle' \
                    and key != 'agli' and key != 'degli' and key != 'esso' and key != 'essa' and key != 'anche':
                if key in tot_word_count:
                    tot_word_count[key] += value
                else:
                    tot_word_count[key] = value
        i = i + 1
    stringList = []
    count = 0
    for key, value in sorted(tot_word_count.items(), key=operator.itemgetter(1)):
        count = count + 1
        # if value > 10:
        #    print(key, value)
        if count == len(tot_word_count) - 2:
            stringList.append(key + " " + str(value))
        if count == len(tot_word_count) - 1:
            stringList.append(key + " " + str(value))
        if count == len(tot_word_count):
            stringList.append(key + " " + str(value))
    return stringList


def extract_data_from_DBpedia(url, list_wiki_url, geoLat, geoLon):
    html = urlopen(url).read()
    doc = bs4.BeautifulSoup(html, features="html.parser")
    count = 0
    for el in doc.find_all('td'):
        if count == 0:
            list_wiki_url.append(el.text)
            count = count + 1
        elif count == 1:
            geoLat.append(el.text)
            count = count + 1
        elif count == 2:
            geoLon.append(el.text)
            count = 0


geoLat = []
geoLon = []
list_wiki_url = []
localita = input('Inserisci localita (iniz. maiuscola): ')
localita = localita.replace(" ", "_")
print("sto calcolando i risultati...")


url = "http://it.dbpedia.org/sparql?default-graph-uri=&query=%0D%0ASELECT+DISTINCT+%3Furl%2C+%3Flat%2C+%3Flong%0D%0A" \
      "WHERE+%7B%0D%0A++++%3Fbuilding+a+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2FPlace%3E+.%0D%0A%0D%0A++++%3F" \
      "building+foaf%3AisPrimaryTopicOf+%3Furl+.+%0D%0A++++%3Fbuilding+dcterms%3Asubject+%3Fname+.%0D%0A++++" \
      "Filter+%28regex+%28%3Fname%2C%22" + localita + "%22%29%29%0D%0A++++OPTIONAL+%7B%0D%0A++++++++%3F" \
      "building+geo%3Alat+%3Flat+.%0D%0A%7D%0D%0A++++OPTIONAL+%7B%0D%0A++++++++%3Fbuilding+geo%3" \
      "Along+%3Flong+.%0D%0A%7D%0D%0A%0D%0A%0D%0A%7D+&format=text%2Fhtml&debug=on"
extract_data_from_DBpedia(url, list_wiki_url, geoLat, geoLon)

#url = "http://it.dbpedia.org/sparql?default-graph-uri=&query=SELECT+DISTINCT+%3" \
#      "Furl+%0D%0AWHERE+%7B%0D%0A++++%3Fbuilding+a+%3Chttp%3A%2F%2Fdbpedia.org%2" \
#      "Fontology%2FPlace%3E+.%0D%0A++++%3Fbuilding+foaf%3AisPrimaryTopicOf+%3" \
#      "Furl+.%0D%0A++++%3Fbuilding+dcterms%3Asubject+%3Fname+.%0D%0A++++Filter+%28" \
#      "regex+%28%3Fname%2C%22" + localita + "%22%29%29%0D%0A%7D+&format=text%2Fhtml&debug=on"
#extract_link_from_DBpedia(url, list_wiki_url)


#url2 = "http://it.dbpedia.org/sparql?default-graph-uri=&query=SELECT+%3Furl%0D%0AWHERE+" \
#       "%7B%0D%0A++++%3Fbuilding+a+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2FArtwork%3E+." \
#       "%0D%0A++++%3Fbuilding+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2Flocation%3E+%3Chttp" \
#       "%3A%2F%2Fit.dbpedia.org%2Fresource%2F" + localita + "%3E+.%0D%0A++++%3Fbuilding+foaf%3A" \
#       "isPrimaryTopicOf+%3Furl.%0D%0A%7D+&format=text%2Fhtml&debug=on"
#extract_link_from_DBpedia(url2, list_wiki_url)

lista_risultati = [{}]

for i in range(0, len(list_wiki_url)):
    word_count = start(list_wiki_url[i])
    print(list_wiki_url[i])
    lista_risultati.append(word_count.items())

print()
print("Sono state analizzate " + str(len(list_wiki_url)) + " pagine.")
print()
print()
ris = final_result(lista_risultati)

if len(ris) != 0:
    localita = localita.replace("_", " ")
    geolocator = Nominatim()
    location = geolocator.geocode(localita)
    dict = location.raw

    lat = dict["lat"]
    lon = dict["lon"]
    intLat = float(lat)
    intLon = float(lon)
    strRis = str(ris)

    folium_map = folium.Map(location=[intLat, intLon],
                            zoom_start=12, tiles='CartoDB positron',
                            top='4%', left='10%',
                            width='80%',
                            height='70%', )
    marker = folium.Marker(location=[intLat, intLon],
                           popup="Le parole più frequenti a " + localita + " sono: <br>" + ris[0] + ",<br>" + ris[
                               1] + ",<br>" + ris[2])

    marker.add_to(folium_map)

    titoli = []
    for i in range(0, len(list_wiki_url)):
        titoli.append(list_wiki_url[i])
    for i in range(0, len(titoli)):
        titoli[i] = titoli[i].replace("http://it.wikipedia.org/wiki/", "")
        titoli[i] = titoli[i].replace("_", " ")
        titoli[i] = titoli[i].replace("'", " ")

    for i in range(0, len(geoLat)):
        if geoLat[i] != "":
            intGeoLat = float(geoLat[i])
            intGeoLon = float(geoLon[i])
            elem = folium.CircleMarker(location=[intGeoLat, intGeoLon], popup=titoli[i], color="red")
            elem.add_to(folium_map)

    folium_map.save("my_map.html")

    with open("my_map.html") as inf:
        txt = inf.read()
        soup = bs4.BeautifulSoup(txt, features="lxml")

    style = soup.new_tag('style', type='text/css')
    soup.head.append(style)
    soup.head.style.append('body {background-color: dodgerblue;}')
    soup.head.style.append('h1 {font-family:arial; color:navy;}')
    soup.head.style.append('p {font-family:arial; color:navy; padding-top:3%;}')
    soup.head.style.append('.folium-map {border-radius:20px; border:solid; color:navy;}')
    soup.head.style.append('h4 {font-size:15px; color:navy;}')
    soup.head.style.append('a {font-family:arial; color:navy;}')
    soup.head.style.append('b {font-family:arial; color:navy;}')

    title = soup.new_tag('title')
    soup.head.append(title)
    soup.head.title.append('risultati ' + localita)

    h1 = soup.new_tag('h1')
    h4 = soup.new_tag('h4')
    center = soup.new_tag('center')
    soup.head.append(center)
    soup.head.center.append(h1)
    soup.head.center.h1.append('VISUALIZZAZIONE RISULTATI ' + localita.upper())
    soup.head.center.append(h4)
    soup.head.center.h4.append("(clicca sul marker blu per vedere le tre parole maggiormente frequenti - "
                               "in rosso sono evidenziati i posti presi in esame per i quali la geolocalizzazione e' stata possibile)")

    soup.body.append(soup.new_tag('center'))
    soup.body.center.append(soup.new_tag('p'))
    soup.body.center.p.append('Progetto Progettazione e Produzione Multimediale - Alessandro Lemmo')

    soup.body.append(soup.new_tag('br'))
    soup.body.append(soup.new_tag('b'))
    soup.body.b.append("sono state analizzate " + str(len(list_wiki_url)) + " pagine")
    soup.body.append(soup.new_tag('br'))
    soup.body.append(soup.new_tag('br'))

    soup.body.append(soup.new_tag('ul'))
    for i in range(0, len(list_wiki_url)):
        soup.body.ul.append(soup.new_tag('li'))

    count = 0
    for li in soup.body.ul.findAll('li'):
        li.append(soup.new_tag("a", href=list_wiki_url[count]))
        li.a.append(list_wiki_url[count])
        li.append(soup.new_tag('br'))
        li.append(soup.new_tag('br'))
        count = count + 1

    with open("my_map.html", "w") as outf:
        outf.write(str(soup))

    webbrowser.open("my_map.html", new=2)
else:
    print("Non ci sono risultati per la località cercata")
