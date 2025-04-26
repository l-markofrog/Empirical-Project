from urllib import request

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
output = open("appartments_links.txt", "w")

# Scrape links for all appartments on all search pages. Link pattern is behind "index" and was found by hand
for i in range(num_pages):
    try:
        find_page = f"https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=London&useLocationIdentifier=true&locationIdentifier=REGION%5E87490&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on%2F&index={str(i*24)}&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=London-87490"
        target = request.urlopen(find_page)
        search_page = target.read()
        appartment_links_list = scrape(search_page, '<a data-testid="property-details-lozenge" href="', '#/?')
        for item in appartment_links_list:
            output.write(url_start + item + "\n")
    except:
        print(f"Error on link: https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=London&useLocationIdentifier=true&locationIdentifier=REGION%5E87490&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on%2F&index={str(i*24)}&sortType=6&channel=RENT&transactionType=LETTING&displayLocationIdentifier=London-87490")
        
print("Finished")


# HTML paterns found:
# Find properties' links:
# <a data-testid="property-details-lozenge" href="  
# #/?

# Find number of pages: 
# of <!-- -->
# </span>
