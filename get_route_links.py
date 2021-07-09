from bs4 import BeautifulSoup
from get_html_text import get_html_text


def get_route_link(start_url):
    # function description:
    #       from the search page, get all route links
    # inputs:
    #       start_url: string
    # output:
    #       route_link_list: [string, string, ...]
    #
    # target search tag is as below :
    # < a href = "https://www.mountainproject.com/route/118575376/minus-man-sit-start" class ="text-black route-row" >
    #   < div class ="float-xs-right text-xs-right" >
    #       < span class ='rateYDS' > V10 < / span > < span class ='rateFont' > 7C+ < / span >
    # ...
    #   < / div >
    # < / a >
    #
    html_text = get_html_text(start_url)
    html_soup = BeautifulSoup(html_text, 'html.parser')
    route_link_list = []
    route_link_sections = div = html_soup.findAll('a', {'class': 'text-black route-row'})
    for each_link_section in route_link_sections:
        try:
            route_link = each_link_section.get('href')
            route_link_list.append(route_link)
        except:
            print("error in get route link in below <a> tag")
            print(each_link_section)
            continue

    return route_link_list
