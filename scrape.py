from urllib import request
import csv 

# Page found by hand which searches for appartments in London

all_regions = []
E_page = "https://www.rightmove.co.uk/property-to-rent/find.html?useLocationIdentifier=true&locationIdentifier=REGION%5E92825&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on%2F&index=0&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=East-London"
all_regions.append(E_page)
N_page = "https://www.rightmove.co.uk/property-to-rent/find.html?useLocationIdentifier=true&locationIdentifier=REGION%5E92826&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on%2F&index=0&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=North-London"
all_regions.append(N_page)
SE_page = "https://www.rightmove.co.uk/property-to-rent/find.html?useLocationIdentifier=true&locationIdentifier=REGION%5E92828&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on%2F&index=0&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=South-East-London"
all_regions.append(SE_page)
SW_page = "https://www.rightmove.co.uk/property-to-rent/find.html?useLocationIdentifier=true&locationIdentifier=REGION%5E92829&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on%2F&index=0&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=South-West-London"
all_regions.append(SW_page)
NW_page = "https://www.rightmove.co.uk/property-to-rent/find.html?useLocationIdentifier=true&locationIdentifier=REGION%5E92827&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on%2F&index=0&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=North-West-London"
all_regions.append(NW_page)
W_page = "https://www.rightmove.co.uk/property-to-rent/find.html?useLocationIdentifier=true&locationIdentifier=REGION%5E92830&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on%2F&index=0&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=West-London"
all_regions.append(W_page)
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


# File of an output
csvfile = open('appartments.csv', 'w', newline='')
    
spamwriter = csv.writer(csvfile, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)

spamwriter.writerow(['link', 'region', 'price_pcm', 'type', 'bedrooms', 'bathrooms'])

data = []

for starting_page in all_regions:
    # Search for the number of pages in the search result
    target = request.urlopen(starting_page)
    search_page = target.read()
    num_pages = int(scrape(search_page, 'of <!-- -->', '</span>'))


    # Scrape links for all appartments on all search pages


    for i in range(num_pages):
        print("page:",i+1)
        try:
            find_page = ("index="+str(i*24)).join(starting_page.split("index=0"))
            target = request.urlopen(find_page)
            search_page = target.read()
            print(find_page)
            page_data = []

            appartment_links_list = scrape(search_page, '<a class="PropertyPrice_priceLink__b24b5" href="', '?')
            appartment_links_list = [url_start + link for link in appartment_links_list]
            print("appartment_links_list:", len(appartment_links_list))
            page_data.append(appartment_links_list)

            appartment_regions_list = scrape(starting_page.encode('utf-8'),'displayLocationIdentifier=', '-London')
            appartment_regions_list = ["".join([region.replace("-"," ") for region in appartment_regions_list])] * len(appartment_links_list)
            print("appartment_regions_list:", len(appartment_regions_list), appartment_regions_list[0])
            page_data.append(appartment_regions_list)
            
            appartment_price_pcm_list = scrape(search_page, '<div class="PropertyPrice_price__VL65t">£', ' pcm</div>')
            appartment_price_pcm_list = [int(price_pcm.replace(',','')) for price_pcm in appartment_price_pcm_list]
            print("appartment_price_pcm_list:", len(appartment_price_pcm_list))
            page_data.append(appartment_price_pcm_list)
            
            appartment_type_list = scrape(search_page,'<span class="PropertyInformation_propertyType__u8e76" aria-label="', '">')
            print("appartment_type_list:", len(appartment_type_list))
            page_data.append(appartment_type_list)

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
