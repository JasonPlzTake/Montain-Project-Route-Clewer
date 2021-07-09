# file name: get_route_info.py
# notes: this file includes functions which are able to collect route information from the route url link
# currently route name, route id, route location, boulder name, url is collected

from bs4 import BeautifulSoup
from get_html_text import get_html_text


def get_route_info(route_link):
    # function description:
    #       by given route link, collect route name, grade, location
    # input:
    #       route_link = string (route url)
    # output:
    #       [string, string, string, ...] ([route id, route name, route grade, route location, route link])
    #
    # Note:
    #       output can easily be convert to dictionary for other functions by using any info in the list as key
    #
    html_text = get_html_text(route_link)
    route_html_soup = BeautifulSoup(html_text, 'html.parser')

    # collect information from sub-functions
    route_id = get_route_id(route_link)
    route_name = get_route_name(route_html_soup)
    route_grade = get_route_grade(route_html_soup)
    route_location_raw = get_route_location(route_html_soup)

    # post process location_list.
    #  split location list below to location and boulder name
    # location list = [state, sub-location1, sub-location2, ..., finest sub-location, boulder name]
    boulder_name = route_location_raw.pop()  # last location name is the boulder name
    route_location = route_location_raw
    return [route_id, route_name, route_grade, "->".join(route_location), boulder_name, route_link]


def get_route_id(route_link):
    # function description:
    #       get the basename of any given link,which is the route name
    # input:
    #       route_link: string
    # output:
    #       route_id: string
    # todo what if the given link is not valid follow below format
    # route_link example:
    # https://www.mountainproject.com/route/106806101/kellys-fly
    #
    route_id = route_link.rsplit('/', 1)[-2].rsplit('/', 1)[-1]  # split twice by '/'
    if route_id.isdecimal():
        return route_id
    else:
        print("error in get route id in below link")
        print(route_link)
        return "invalid ID"


def get_route_name(html_soup):
    # target section is as below example:
    #
    # < title > Climb Horse Fly, Olympics & amp; Pacific Coast < / title >
    #
    name_section = html_soup.find('title')
    name = str(name_section).split(',')[0].split(' ', 1)[1]  # split by 'Climb' and ',' which remains the problem name
    return name


def get_route_grade(html_soup):
    # target area is as below example:
    #
    # < h2 class ="inline-block mr-2" >
    #   < span class ='rateYDS' > V6
    #       < a href="https://www.mountainproject.com/international-climbing-grades" class ="font-body" >
    #           < span class ="small" > YDS
    #           < / span >
    #       < / a >
    #   < / span >
    #   < span class ='rateFont' > 7A
    #       < a href="https://www.mountainproject.com/international-climbing-grades" class ="font-body" >
    #           < span class ="small" > Font
    #           < / span >
    #       < / a >
    #   < / span >
    # < / h2 >

    grade_section = html_soup.find('h2', {'class': 'inline-block mr-2'})
    grade = grade_section.find('span', {'class': 'rateYDS'}).find_all(text=True)  # grade = [grade number, YDS]
    return grade[0]


def get_route_location(html_soup):
    # search all <a> tag which shall include location link following below sequence
    # [parent location1 link, parent location2 link, ..., finest area location link, boulder link]
    # todo are there any location name originally with '-'?
    #
    # target location area is as below example:
    #
    # < div class ="mb-half small text-warm" >
    #     < a href = "https://www.mountainproject.com/route-guide" > All Locations < / a >
    #     & gt;
    #     < a href = "https://www.mountainproject.com/area/105708966/washington" > Washington < / a >
    #     & gt;
    #     < a href = "https://www.mountainproject.com/area/108471374/central-west-cascades-seattle" > Central - W Casca & hellip; < / a >
    #     & gt;
    #     < a href = "https://www.mountainproject.com/area/108471672/skykomish-valley" > Skykomish Valley < / a >
    #     & gt;
    #     < a href = "https://www.mountainproject.com/area/105805788/gold-bar-boulders" > Gold Bar Boulders < / a >
    #     & gt;
    #     < a href = "https://www.mountainproject.com/area/105970461/zekes-trail-boulders" > Zeke &  # 039;s Trail Bo&hellip;</a>
    #     & gt;
    #     < a href = "https://www.mountainproject.com/area/118994021/jaws-boulder" > Jaws Boulder < / a >
    # < / div >
    #
    location_section = html_soup.find('div', {'class': 'mb-half small text-warm'})
    location_list = []
    index = 0
    for raw_location in location_section.find_all('a'):
        # skip the first location 'https://www.mountainproject.com/route-guide'
        index += 1
        if index <= 1:
            continue

        # add parent location -> child location ->...-> finest location into location_list
        location_link = raw_location.get('href')  # get location and parent location links
        location_name = location_link.rsplit('/', 1)[-1]  # get the last section after slash as location name
        location_list.append(location_name.replace("-", " "))  # replace '-' with space, and saved to list
    return location_list
