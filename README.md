# WG-Gesucht
This is an small programm to crawl WG gesucht with CPT and Google APIs to boost your search (or make it less effective)




# Goals
My goal was not to go more then 25 min by bike, share some interests and being close to certain centers of the city (here Munich).


# Make the code work

## Fromal things
run pip install -r requirements.txt


## Google
- Add your API key to the api_keys.py
- Replace the locations (define as many circles as wanted)
  - # Define the streets and distances
  origin_general = 'Target adress'            # workspace
  origin_nymp="Circle 1 adress"  
  origin_schwab="Circle 2 adress"  
 - Choose max distance or distance in minutes

## ChatGPT
- Make connection aitomated (did it by hand still, had no credits, by clicking the wg link page and feed all the text wg-text)
- Add your API key to the api_keys.py
- Write something about you as a comparison in self.my_text

## WG Gesucht
- Add specific crawling parameters (city, wg size, age, .....) in WG gesucht and copy the linke
- Divide the link at the right place (see in code)
- Choose number of pages (n_pages)
- Maybe change the databas (e.g. add viewed)
- Run the code and let the wgs be added
