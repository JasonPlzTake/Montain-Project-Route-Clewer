# file name: get_search_url.py
# notes: this file include functions generating search url based on inputs


def get_search_url(location, route_type, grade_lower_limit, grade_upper_limit):
    # function description:
    #       this function is to generate url based on the location, route type and grading range provided
    #       it functions as the same as the search engine. see below link for instance:
    #       https://www.mountainproject.com/route-guide
    # see below search link for example:
    #       start_url = "https://www.mountainproject.com/route-finder?diffMaxaid=75260&diffMaxboulder=20850&diffMaxice
    #       =38500&diffMaxmixed=60000&diffMaxrock=5500&diffMinaid=70000&diffMinboulder=20450&diffMinice=30000&diffMinmixed
    #       =50000&diffMinrock=1800&pitches=0&selectedIds=105708966&sort1=area&sort2=rating&stars=0&type=boulder&viewAll=1"
    # inputs:
    #       location: string ("washington") (# todo other states or sub-location can be supported in the future)
    #       route_type: string ("boulder") (# todo other route type as 'aid','ice', ... can be supported in the future)
    #       grade_lower_limit: string （"v0"）  (# todo other grading unit as '5.12a' can be supported in the future)
    #       grade_upper_limit： string ("v10")
    # output:
    #       url: string (search result page of qualified route)
    #
    # todo: invalid input check as well as validate output url is valid
    main_url = "https://www.mountainproject.com/route-finder?"
    area_id = get_location_id(location)
    route_type = "type=" + route_type
    grade_section = gen_grade_section(route_type, grade_lower_limit, grade_upper_limit)
    sports_type = "is_trad_climb=1&is_sport_climb=1&is_top_rope=1"  # only applicable when route type is 'rock'
    stars = "stars=0"
    pitches = "pitches=0"
    sort1 = "sort1=area"
    sort2 = "sort2=rating"
    nums_per_page = "viewAll=1"
    return "&".join(
        [main_url + grade_section, area_id, sort1, sort2, stars, route_type, sports_type, pitches, nums_per_page])


def gen_grade_section(route_type, grade_lower_limit, grade_upper_limit):
    # function description:
    #           based on the input grading limit, generate valid url portion specifying search grading range
    # inputs:
    #       route_type: string ("boulder") (# todo other route type as 'aid','ice', ... can be supported in the future)
    #       grade_lower_limit: string （"v0"）  (# todo other grading unit as '5.12a' can be supported in the future)
    #       grade_upper_limit： string ("v10")
    # outputs:
    #       string
    # todo: other grading map can be added in, route_type will be used in the future
    #
    # generate bouldering grading mapping
    bouldering_grade_map = {
        "V-B": '20000',
        "V0": '20050',
        "V1": '20150',
        "V2": '20250',
        "V3": '20350',
        "V4": '20450',
        "V5": '20550',
        "V6": '20650',
        "V7": '20750',
        "V8": '20850',
        "V9": '20950',
        "V10": '21050',
        "V11": '21150',
        "V12": '21250',
        "V13": '21350',
        "V14": '21450',
        "V15": '21550',
        "V16": '21650',
        "V17": '21750'}

    return "diffMaxboulder=" + bouldering_grade_map[grade_upper_limit] + "&" + "diffMinboulder=" + bouldering_grade_map[grade_lower_limit]


def get_location_id(location):
    # function description:
    #       based on the input grading limit, generate valid url portion specifying search location
    location_id_map = {'washington': "105708966"}  # location map can be extended to support more areas

    # return "" if location is not in the location map, otherwise return string with location code
    if location_id_map.__contains__(location):
        return "selectedIds=" + location_id_map[location]
    else:
        return ""
