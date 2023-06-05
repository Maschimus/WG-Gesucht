from wg_gesucht import WGGesuchtScraper
from google_api import GoogleAPI
from database_management import DatabaseManager
#from gpt_api import GPTAPI

# Create list for wgs
wgs=[]
# Create list for filtered flats
filtered_wgs=[]


# Define the streets and distances
origin_general = 'Target adress'            # workspace
origin_nymp="Circle 1 adress"               # first hotspot
origin_schwab="Circle 2 adress"             # second hotspot
# Define distances to locations
max_distance_general=5.8
max_distance_nymp=3.1
max_distance_schwab=2.5

# Open/create database 
db_file_name="wg-search-database.db"

# Create an instance of DatabaseManager
db_manager = DatabaseManager('wg-search-database.db')
db_manager.create_connection()
db_manager.create_table()


#Loop through pages
n_pages=11
#todo generate link form parameters
first_url="https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1."
second_url=".html?csrf_token=0cf03976da5ec4f6a5bad1c87422d02824e7e5ab&offer_filter=1&city_id=90&sort_order=0&noDeact=1&dFr=1685527200&dTo=1688378400&categories[]=0&rent_types[]=2&rent_types[]=2&rMax=700&wgMnF=1&wgMxT=5&pagination=1&pu="
print("Starting search")
for j in range(0,n_pages):
    url=first_url+str(j)+second_url
    print("Search page "+ str(j))
    # Load conrent
    content=WGGesuchtScraper.fetch_url_content(url).decode('utf-8')

    # Split text to parts at wgg_card offer_list_item, remove fist
    split_html = content.split("wgg_card offer_list_item")
    split_html = split_html[1:]  # Remove the first element since it has only advertisment
    split_html[-1]=split_html[-1].split("Jetzt kostenlos WG inserieren")[0] # Remove the other ends so we only have the offers

    for wg in split_html:
        # Get title, price
        title, price, size, location, availability, link=WGGesuchtScraper.extract_offer_details(wg)

        #print_outputs([title, price, size, location, availability, link])
        # Format the inputs
        wg_size, quarter, address=WGGesuchtScraper.extract_address_components(location)
        # Pack all information in a dict
        wg={
            'title':title,
            'price':price, # convert to srt for json
            'size':size,   # convert to str for json
            'wg-size':wg_size,
            'quater':quarter,
            'address':address,
            'availability':availability,
            'link':link,
            'distance': str(0),
            'contacted':False
        }
        wgs.append(wg)
        
#Loop over the wgs and calculate distace 
for wg in wgs:
    destination=wg["address"]
    try:
        # Calculate radius for all
        distance_general = GoogleAPI.calculate_distance(origin_general, destination)
        distance_general=float(distance_general.split()[0])
        
        distance_nymp = GoogleAPI.calculate_distance(origin_nymp, destination)
        distance_nymp=float(distance_nymp.split()[0])
        
        distance_schwab = GoogleAPI.calculate_distance(origin_schwab, destination)
        distance_schwab=float(distance_schwab.split()[0])
        #print(distance_general,distance_nymp, distance_schwab)
        
        # Write distance
        wg['distance']=str(distance_general)
        
        # if distance check
        if(distance_general<max_distance_general and (distance_nymp<max_distance_nymp or distance_schwab<max_distance_schwab)): 
            print("Found a flat that maches your criteria")
            filtered_wgs.append(wg)
            #Add wg to dictionary and check if it is already in list
            if not db_manager.entry_exists( wg['link']):
                        db_manager.insert_dictionary(wg)
                        print("Added new databas entry")
            else:
                print("WG seems to be in already in the list ")
                print(wg["link"])

    except Exception as e:
        #todo Make better to save code
        print("No address data available now taking the quater")
        try:
            destination=wg['quater']
             # Calculate radius for all
            distance_general = GoogleAPI.calculate_distance(origin_general, destination)
            distance_general=float(distance_general.split()[0])
            
            distance_nymp = GoogleAPI.calculate_distance(origin_nymp, destination)
            distance_nymp=float(distance_nymp.split()[0])
            
            distance_schwab = GoogleAPI.calculate_distance(origin_schwab, destination)
            distance_schwab=float(distance_schwab.split()[0])
            
            # Write distance
            wg['distance']=distance_general
            
            # if distance check
            if(distance_general<max_distance_general and (distance_nymp<max_distance_nymp or distance_schwab<max_distance_schwab)): 
                #Add wg to dictionary and check if it is already in list
                print("Found a good quater for you!")
                filtered_wgs.append(wg)
                if not db_manager.entry_exists( wg['link']):
                            db_manager.insert_dictionary(wg)
                            print("Added new databas entry")
        except Exception as e:
            print("No address data available  at all. Remove from list")

       
print("\n \n ")                         
print(" I finished the search for you. I did not pass it to GPT4, yet. here you have to pay.")
print("\n \n ") 
print("I found "+ str(int(len(filtered_wgs)))+" possible new flats. Check out the database for the list")
print("\n \n")   
print("I wish you all the best luck. The rest is up to you. Humans can not yet be automated!")      
db_manager.close_connection()




# todo pay again and readd text
'''
print("Now consulting GPT, please wait")
chat=GPTAPI()
evaluation=chat.get_evaluation_of_fit(wg_text)
if(evaluation>5):
    print("Now writing text.")
    text=chat.write_text(wg_text)
    print(text)
else:
    print("This was nothing dor you")
'''


