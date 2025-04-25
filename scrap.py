from urllib import request, error
import re

starting_page = "https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=London&useLocationIdentifier=true&locationIdentifier=REGION%5E87490&rent=To+rent&radius=0.0&propertyTypes=flat&_includeLetAgreed=on/"
url_start = "https://www.rightmove.co.uk/"

def scrape(page, start, end):
    data_list = []
    right_data_list = page.decode('utf-8').split(start)[1:]
    for right_data in right_data_list:
        data = right_data.split(end)[0]
        data_list.append(data)
    if len(data_list) == 1:
        return data_list[0]
    else: return data_list

#output = open("appartments.txt", "w")
#output.write('Comic, Number, Title\n')

appartment_links_list = []
appartment_links_list_ex = ['https://www.rightmove.co.uk//properties/160619321', 'https://www.rightmove.co.uk//properties/160687214', 'https://www.rightmove.co.uk//properties/160959065', 'https://www.rightmove.co.uk//properties/160617632', 'https://www.rightmove.co.uk//properties/159990269', 'https://www.rightmove.co.uk//properties/161155151', 'https://www.rightmove.co.uk//properties/159978746', 'https://www.rightmove.co.uk//properties/159478985', 'https://www.rightmove.co.uk//properties/160227788', 'https://www.rightmove.co.uk//properties/158884949', 'https://www.rightmove.co.uk//properties/159186707', 'https://www.rightmove.co.uk//properties/161155013', 'https://www.rightmove.co.uk//properties/160394129', 'https://www.rightmove.co.uk//properties/161154677', 'https://www.rightmove.co.uk//properties/161154926', 'https://www.rightmove.co.uk//properties/161154296', 'https://www.rightmove.co.uk//properties/161154434', 'https://www.rightmove.co.uk//properties/161154269', 'https://www.rightmove.co.uk//properties/161154266', 'https://www.rightmove.co.uk//properties/159704990', 'https://www.rightmove.co.uk//properties/157622354', 'https://www.rightmove.co.uk//properties/160587920', 'https://www.rightmove.co.uk//properties/160297301', 'https://www.rightmove.co.uk//properties/161153993', 'https://www.rightmove.co.uk//properties/161153996']

target = request.urlopen(starting_page)
find_page = target.read()

pre_link = find_page.decode('utf-8').split('<a data-testid="property-details-lozenge" href="')[1:]

for data in pre_link:
    link = data.split('#/?')[0]
    appartment_links_list.append(url_start + link)

print(len(appartment_links_list_ex))

"""
for i in range(50):
    try:
        target = target_start + str(i+1)
        response = request.urlopen(target)
        data = response.read()
        comic_name = data.decode('utf-8').split('<div id="ctitle">')[1].split("</div>")[0]
        #output.write("xkcd, " + str(i+1)+ ", \"" + comic_name + "\"\n")
    except:
        print("Mistake in", i+1)
"""

# Find properties links:
# <a data-testid="property-details-lozenge" href="  
# #/?

# Find number of pages: 
# of <!-- -->
# </span>
