import requests
import kml2geojson as kg
import xml.dom.minidom as md
import pandas as pds
from shapely.geometry import shape, Point
from haversine import haversine
import shapely.wkt
import pprint as pp
import json
import os
from dotenv import load_dotenv, find_dotenv

# load the .env file content into the system environment variables
load_dotenv(find_dotenv())

# converts a string to geoJSON
def convert2geojson(x):
    x1 = x.replace("'",'"')
    x2 = json.loads(x1)
    return(x2)

# returns centroid for specific geoJSON object
def getcentroid(obj): #get a centroid from a polygon
    geom = shape(obj)
    centroid_wkt = geom.centroid.wkt
    centroid1 = str(shapely.wkt.loads(centroid_wkt))
    centroid2 = centroid1.replace("POINT", "")
    centroid3 = centroid2.replace("(", "")
    centroid3bis = centroid3.replace(")", "")
    tt = centroid3bis.strip()
    rez = tt.split(" ")
    return(rez)

# returns max distance between the centroid and the farthest point within a specific object
def getradius(obj): #get the distance from the polygon centroid
    #print(getcentroid(zone_list[0][2]),zone_list[0][2]['coordinates'][0])
    centroid = getcentroid(obj)
    distances = []
    for i in range(len(obj['coordinates'][0])):
        try:
            distances.append(haversine((float(centroid[1]),float(centroid[0])),(obj['coordinates'][0][i][1],obj['coordinates'][0][i][0]),miles=False))
        except TypeError:
            distances.append(1.5)
    return(float(max(distances)))

def getrestaurants(obj):
    polygon = shape(obj)
    centroid = getcentroid(obj)
    radius = getradius(obj)
    url = 'https://api.tripadvisor.com/api/internal/1.14/location/' + \
          str(centroid[1]) + "," + str(centroid[0]) + \
          '/restaurants?base_geocodes_on=google&combined_food=all&currency=GBP' + \
          '/&dietary_restrictions=all' + \
          '&distance=' + str(radius) + \
          '&is_restaurant_filters_v2=true&lang=en_GB' + \
          '&limit=50' + \
          '&lunit=km&neighborhood=all' + \
          '&offset=0'\
          '&restaurant_mealtype=all&' + \
          '&show_filters=true&show_review_highlights=true&' + \
          'sort=distance' + \
          '&supports_relevance=true'
    token = os.environ.get('TRIPADVISOR_TOKEN')
    key = os.environ.get('TRIPADVISOR_KEY')
    print(token,key)
    headers = {
            'Host': 'api.tripadvisor.com'
            , 'Authorization': token
            , 'X-TripAdvisor-API-Key': key
            # , 'X-TripAdvisor-Unique': '%1%enc%3A2DsNmqCvaHfIJF2zdNjNXpxT94rVEsRiPhiQmo60zvrwMRbPLBBMzQ%3D%3D'
            # , 'X-TripAdvisor-UUID': 'F618386F-663E-4C81-9B53-67DA3829E9E8'
            }
    results = []
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    for k in range(len(data['data'])):
        name = data['data'][k]['name']
        try:
            phone = data['data'][k]['phone']
        except:
            phone = ''
        try:
            street = data['data'][k]['address_obj']['street1']
            postalcode = data['data'][k]['address_obj']['postalcode']
            city = data['data'][k]['address_obj']['city']
        except:
            street = ''
            postalcode = ''
            city = ''
        try:
            b = data['data'][k]['cuisine']
            c = ''
            for cuisine_types in b:
                c += (cuisine_types['name'] + '; ')
            cuisine = c
        except:
            cuisine = ''
        try:
            b = data['data'][k]['dietary_restrictions']
            c = ''
            for diet_types in b:
                c+=(diet_types['name'] + '; ')
            dietary_restrictions = c
        except:
            dietary_restrictions = ''
        try:
            b = data['data'][k]['subcategory']
            c = ''
            for subcategory in b:
                c += (subcategory['name'] + '; ')
            subcat = c
        except:
             subcat = ''
        try:
            lat = data['data'][k]['latitude']
            long = data['data'][k]['longitude']
        except:
            lat = ''
            long = ''
        try:
            tripadvisor_id =  data['data'][k]['location_id']
        except:
            tripadvisor_id = ''
        try:
            tripadvisor_url = data['data'][k]['web_url']
        except:
            tripadvisor_url = ''
        try:
            price_level = data['data'][k]['price_level']
        except:
            price_level = ''
        try:
            ranking = data['data'][k]['ranking']
        except:
            ranking = ''
        try:
            ranking_position = data['data'][k]['ranking_position']
        except:
            ranking_position = ''
        try:
            ranking_denominator = data['data'][k]['ranking_denominator']
        except:
            ranking_denominator = ''
        try:
            num_reviews = data['data'][k]['num_reviews']
        except:
            num_reviews = ''
        try:
            rating = data['data'][k]['rating']
        except:
            rating = ''
        point = Point(float(long),float(lat))
        if polygon.contains(point):
            results.append(dict([('name',name),('phone',phone),('street',street),('postalcode',postalcode),('city',city),('cuisine',cuisine),('dietary_restrictions',dietary_restrictions),('subcategory',subcat),('coord',(lat,long)),('tripadvisor_id',tripadvisor_id),('tripadvisor_url',tripadvisor_url),('price_level',price_level),('ranking',ranking),('ranking_position',ranking_position),('ranking_denominator',ranking_denominator),('num_reviews',num_reviews),('rating',rating)]))
    while data['paging']['next'] is not None:
        response = requests.request("GET", data['paging']['next'], headers=headers)
        data = response.json()
        for i in range(len(data['data'])):
            try:
                name = data['data'][i]['name']
            except:
                name=''
            try:
                phone = data['data'][i]['phone']
            except:
                phone = ''
            try:
                street = data['data'][i]['address_obj']['street1']
                postalcode = data['data'][i]['address_obj']['postalcode']
                city = data['data'][i]['address_obj']['city']
            except:
                street = ''
                postalcode = ''
                city = ''
            try:
                b = data['data'][i]['cuisine']
                c = ''
                for cuisine_types in b:
                    c += (cuisine_types['name'] + '; ')
                cuisine = c
            except:
                cuisine = ''
            try:
                b = data['data'][i]['dietary_restrictions']
                c = ''
                for diet_types in b:
                    c += (diet_types['name'] + '; ')
                dietary_restrictions = c
            except:
                dietary_restrictions = ''
            try:
                b = data['data'][i]['subcategory']
                c = ''
                for subcategory in b:
                    c += (subcategory['name'] + '; ')
                subcat = c
            except:
                subcat = ''
            try:
                lat = data['data'][i]['latitude']
                long = data['data'][i]['longitude']
            except:
                lat = ''
                long = ''
            try:
                tripadvisor_id = data['data'][i]['location_id']
            except:
                tripadvisor_id = ''
            try:
                tripadvisor_url = data['data'][i]['web_url']
            except:
                tripadvisor_url = ''
            try:
                price_level = data['data'][i]['price_level']
            except:
                price_level = ''
            try:
                raking = data['data'][i]['ranking']
            except:
                raking = ''
            try:
                raking_position = data['data'][i]['ranking_position']
            except:
                raking_position = ''
            try:
                raking_denominator = data['data'][i]['ranking_denominator']
            except:
                raking_denominator = ''
            try:
                num_reviews = data['data'][i]['num_reviews']
            except:
                num_reviews = ''
            try:
                rating = data['data'][i]['rating']
            except:
                rating = ''
            point = Point(float(long), float(lat))
            if polygon.contains(point):
                results.append(dict(
                    [('name', name), ('phone', phone), ('street', street), ('postalcode', postalcode), ('city', city),
                     ('cuisine', cuisine), ('dietary_restrictions', dietary_restrictions), ('subcategory', subcat),
                     ('coord', (lat, long)), ('tripadvisor_id', tripadvisor_id), ('tripadvisor_url', tripadvisor_url),
                     ('price_level', price_level), ('ranking', ranking), ('ranking_position', ranking_position),
                     ('ranking_denominator', ranking_denominator), ('num_reviews', num_reviews), ('rating', rating)]))


    return(results)

#opens the kml file
with open('filename.kml') as myfile: #INPUT REQUIRED: Change file name
    doc=md.parseString(myfile.read())

features = kg.build_layers(doc)[0]['features']

end_data = []
# loops over the elements in the kml file
for i in range(len(features)):
    sector = features[i]['geometry']
    name = features[i]['properties']['name']
    print(name)
    try:
        ta_data = getrestaurants(sector)
        pp.pprint(ta_data)
        for j in range(len(ta_data)):
            x = ta_data[j].copy()
            y = {'extension-name':name}
            y.update(x)
            end_data.append(y)
        #pp.pprint(y)
    except:
        pass

df_results = pds.DataFrame(end_data)
print(df_results)
df_results.to_csv('scraping_results.csv') #INPUT REQUIRED: Change output name


