# file name: post_process.py
# notes: include any post process function
# todo: consider read from excel separating data scraping and post processing


def categorize_by_area(route_info_list):
    # description:
    #            categorized route by area, return a dictionary/hashmap with
    #            key: area name;  val: route_info list in the area
    # input:
    #       route_info_list: [route_info1, ..., route_infoN]
    #       route_info1: [route id, route name, route grade, route location, route link]
    # output:
    #       route_info_by_area: {area1 : [route_info1, route_info2, ..., ],
    #                            area2 : [route_info3, route_info4, ..., ],
    #                            ...}
    #
    route_info_by_area = {}
    for route_info in route_info_list:
        if route_info[3] not in route_info_by_area:
            route_info_by_area[route_info[3]] = []
        route_info_by_area[route_info[3]].append(route_info)

    return route_info_by_area


def update_max_excel_column_len(max_col_len, route_info):
    index = 0
    for info in route_info:
        max_col_len[index] = max(len(info), max_col_len[index])
        index += 1
    return max_col_len