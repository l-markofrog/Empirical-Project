from urllib import request
import csv 

# Page found by hand which searches for appartments in London
starting_page = "https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=London&useLocationIdentifier=true&locationIdentifier=REGION%5E87490&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on/"
# Start of the urls on the web-site
url_start = "https://www.rightmove.co.uk"

# Function that scrapes all the instances in the HTML code between two given fragments of code. Outputs list if multiple, else single value.
def scrape(page, start, end):
    data_list = []
    right_data_list = page.decode('utf-8').split(start)[1:]
    for right_data in right_data_list:
        data = right_data.split(end)[0]
        data_list.append(data)
    if len(data_list) == 1:
        return data_list[0]
    else: return data_list

# Search for the number of pages in the search result
target = request.urlopen(starting_page)
search_page = target.read()
num_pages = int(scrape(search_page, 'of <!-- -->', '</span>'))

# File of an output
csvfile = open('appartments.csv', 'w', newline='')
    
spamwriter = csv.writer(csvfile, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)

spamwriter.writerow(['link', 'post_code', 'price_pcm', 'type', 'bedrooms', 'bathrooms'])


# Scrape links for all appartments on all search pages. Link pattern is behind "index" and was found by hand
data = []

for i in range(num_pages):
    print("page:",i+1)
    try:
        find_page = f"https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=London&useLocationIdentifier=true&locationIdentifier=REGION%5E87490&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on%2F&index={str(i*24)}&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=London-87490"
        target = request.urlopen(find_page)
        search_page = target.read()
        print(find_page)
        page_data = []

        appartment_links_list = scrape(search_page, '<a class="PropertyPrice_priceLink__b24b5" href="', '?')
        appartment_links_list = [url_start + link for link in appartment_links_list]
        print("appartment_links_list:", len(appartment_links_list))
        page_data.append(appartment_links_list)

        appartment_post_codes_list = scrape(search_page,'<address class="PropertyAddress_address__LYRPq" aria-label="Property address: ', '">')
        appartment_post_codes_list = [post_code.split(', ')[-1] for post_code in appartment_post_codes_list]
        print("appartment_post_codes_list:", len(appartment_post_codes_list))
        page_data.append(appartment_post_codes_list)
        
        appartment_price_pcm_list = scrape(search_page, '<div class="PropertyPrice_price__VL65t">£', ' pcm</div>')
        appartment_price_pcm_list = [int(price_pcm.replace(',','')) for price_pcm in appartment_price_pcm_list]
        print("appartment_price_pcm_list:", len(appartment_price_pcm_list))
        page_data.append(appartment_price_pcm_list)
        
        appartment_type_list = scrape(search_page,'<span class="PropertyInformation_propertyType__u8e76" aria-label="', '">')
        print("appartment_type_list:", len(appartment_type_list))
        page_data.append(appartment_type_list)
        studios = [j for j, x in enumerate(appartment_type_list) if "Studio" in x]

        check_missing_list = scrape(search_page,'<div class="PropertyInformation_container__2wY0G" data-testid="property-information">', '</div></div></a>')
        missing_bed = [j for j, x in enumerate(check_missing_list) if "PropertyInformation_bedContainer___rN7d" not in x]
        missing_bath = [j for j, x in enumerate(check_missing_list) if "PropertyInformation_bathContainer__ut8VY" not in x]
        
        appartment_bedrooms_list = scrape(search_page, '<span class="PropertyInformation_bedroomsCount___2b5R" aria-label="',' in property">')
        appartment_bedrooms_list = [int(beds) for beds in appartment_bedrooms_list]
        for j in missing_bed: appartment_bedrooms_list.insert(j, '')
        print("appartment_bedrooms_list:", len(appartment_bedrooms_list))
        page_data.append(appartment_bedrooms_list)

        appartment_bathrooms_list = scrape(search_page, '<span aria-label="',' in property">')
        appartment_bathrooms_list = [int(baths) for baths in appartment_bathrooms_list]
        for j in missing_bath: appartment_bathrooms_list.insert(j, '')
        print("appartment_bathrooms_list:", len(appartment_bathrooms_list))
        page_data.append(appartment_bathrooms_list)
        

        pivot_data = [list(x) for x in zip(*page_data)]

        data = data + pivot_data
        print("data on page:", len(pivot_data), "\n")

    except Exception as e:
        print(f"Error {e} on link: https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=London&useLocationIdentifier=true&locationIdentifier=REGION%5E87490&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on%2F&index={str(i*24)}&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=London-87490")
        
for listing in data:
    spamwriter.writerow(listing)

print("total listings:", len(data))


csvfile.close()
print("Finished")


"""

import pandas as pd
csvfile = open('test.csv', 'w', newline='')
    
spamwriter = csv.writer(csvfile, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)

spamwriter.writerow(['lol', 'kek', 'lmao'])
spamwriter.writerow(['cool', 'uncool', 'very, very cool'])

csvfile.close()

df = pd.read_csv("test.csv")
print(df)

"""

#<div class="PropertyInformation_container__2wY0G" data-testid="property-information">
#</div></div></a>

# HTML paterns found:
# Find properties' links:
# <a data-testid="property-details-lozenge" href="  
# #/?

# Find number of pages: 
# of <!-- -->
# </span>
