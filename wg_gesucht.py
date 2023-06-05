import requests
import re
from bs4 import BeautifulSoup
class WGGesuchtScraper:
    @staticmethod
    def login_to_wg_gesucht():
        # URL of the login page
        login_url = 'https://www.wg-gesucht.de/#'

        # Credentials for logging in
        username = 'your username'
        password = 'your password'

        # Create a session object
        session = requests.Session()

        # Perform the login
        login_data = {
            'username': username,
            'password': password
        }
        response = session.post(login_url, data=login_data)

        # Check if the login was successful (optional)
        if response.status_code == 200:
            print('Login successful')
        else:
            print('Login failed')
            


    @staticmethod
    def fetch_url_content(url):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                content = response.content

                # Print the content for inspection
                return content

            else:
                print(f"Request failed with status code: {response.status_code}")
                return None

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def exclude_first_lines(html_content, num_lines):
        lines = html_content.split('\n')
        excluded_lines = lines[num_lines:]
        excluded_html = '\n'.join(excluded_lines)
        return excluded_html
    
    
    
    def get_price(offer):
            # Define the regular expression pattern
            pattern = r'(\d+)\s+&euro;'
            
            # Find the first matching pattern in the HTML text
            match = re.search(pattern, offer)

            # Extract the number from the match
            if match:
                price = int(match.group(1))
                return price
            else:
                print("No price found.")
                return None
            
    @staticmethod
    def extract_address_components(location):
        address = location.strip()
        address = address.replace("Ã¼", "ü")
        address = address.replace("Ã¶", "ö")
        address = address.replace("Ã¤", "ä")
        address = address.replace("Ã\x9f", "ß")
        address = address.replace("Ã„", "Ä")
        address = address.replace("Ã–", "Ö")
        address = address.replace("Ãœ", "Ü")
        address = " ".join(address.split())
        parts = address.split("|")
        if len(parts) != 3:
            raise ValueError("Invalid address format. Address must contain exactly three parts separated by '|'.")
        wg_size = parts[0].strip()
        quarter = parts[1].strip()
        address = parts[2].strip()
        address = AddressFormatter.format_address(address)
        address = AddressFormatter.add_munich(address)
        quarter = AddressFormatter.add_munich(quarter)
        return wg_size, quarter, address
    
        
    
    def extract_dates(html_data):
        start_index = html_data.find('>')
        end_index = html_data.find('</div>')
        
        if start_index != -1 and end_index != -1:
            date = html_data[start_index + 1:end_index].strip()
            return date
        else:
            return None
        
    def get_title(offer):
        offer=BeautifulSoup(offer, 'html.parser')
        return offer.find('h3', class_='truncate_title').text.strip()

    def get_size(offer):
        pattern = r'(\d+)\s+m&sup2;'
        # Find the first matching pattern in the HTML text
        match = re.search(pattern, offer)

        # Extract the number from the match
        if match:
            area = int(match.group(1))
            return(area)
        else:
            print("No match for size found.")
            return None
        
    def get_link(offering):
        offer=BeautifulSoup(offering, 'html.parser')
        return offer.find('a', class_='detailansicht')['href']

    def get_availability(offering):
        offer=BeautifulSoup(offering, 'html.parser')
        all_dates=offer.find('div', class_='col-xs-5 text-center')
        return WGGesuchtScraper.extract_dates(str(all_dates))
        
        

    def get_location(offer):
        soup = BeautifulSoup(offer, 'html.parser')
        col_xs_11_div = soup.find('div', class_='col-xs-11')
        if col_xs_11_div:
            span_content = col_xs_11_div.span.get_text(separator='|', strip=True)
            return span_content
        else:
            return None



    def extract_offer_details(offering):
        try:
            title =WGGesuchtScraper.get_title(offering)
            price=WGGesuchtScraper.get_price(offering)
            size=WGGesuchtScraper.get_size(offering)
            link=WGGesuchtScraper.get_link(offering)
            availability=WGGesuchtScraper.get_availability(offering)
            location=WGGesuchtScraper.get_location(offering)
        

            return title, price, size, location, availability, link

        except Exception as e:
            # Exception handling code for other exceptions
            print("An error occurred:", str(e))
            return None
        
    def fetch_url_content(url):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                content = response.content

                # Print the content for inspection
                return content

            else:
                print(f"Request failed with status code: {response.status_code}")
                return None

        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    def print_outputs(list):
        for i in list:
            print(i)

        
        
        
class AddressFormatter:
    @staticmethod
    def format_address(data):
        parts = data.split(' ')
        if len(parts) >= 2:
            first_part = parts[0]
            second_part = ' '.join(parts[1:])
            if first_part.isdigit():
                formatted_data = f"{second_part} {first_part}"
                return formatted_data
            else:
                return data
        elif len(parts) == 1:
            name = parts[0]
            formatted_data = f"{name} 10"
            return formatted_data
        else:
            return data

    @staticmethod
    def add_munich(data):
        additional_string = ", München"
        return "{}{}".format(data, additional_string)