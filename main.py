# Readme
# this function is to collect route information from https://www.mountainproject.com/
# the workflow is as below:
# 1) generate search url, based on the searching criteria specified (get_search_url.py)
# 2) collect route links by using mountain project search engine (get_route_links.py)
# 3) visit each route link, save route info into route_info_list (get_route_info.py)
# 4) post process data, count qualified routes by area (post_process.py)
# 5) save route information in excel sheet (write_to_file.py)

# import python lib
import time

# import custom functions
from get_route_links import get_route_link
from get_route_info import get_route_info
from get_search_url import get_search_url
import write_to_file
import post_process


def main(name):
    # generate search url, based on the search criteria
    print("generate search url ...")
    area_name = "washington"
    route_type = "boulder"
    grading_from = "V4"  # grade low bound is not included
    grading_end = "V8"  # grade upper bound is included
    start_url = get_search_url(area_name, route_type, grading_from, grading_end)  # grading range is (low, high]
    print(start_url)

    #  collect route links by using mountain project search engine
    print("get qualified route links from search engine ...")
    link_list = get_route_link(start_url)
    print("search complete!")

    # visit each route link, save route info into route_info_list
    # update max length of each route information, which will be used to set excel column width
    route_info_list = []
    # define default column length for the excel sheet
    max_col_len = [len("Route ID"), len("Route Name"), len("Route Grade"), len("Route Location"), len("Boulder Name"),
                   len("Route URL")]
    # iterate and open each route link and collect route info saved in route_info_list
    # route_info: [route_id, route_name, route_grade, route_location, route_link]
    for link in link_list:
        print("get info from:" + link)
        # get each route info from visiting the route web page
        route_info = get_route_info(link)
        # add each route info into the route info list
        route_info_list.append(route_info)
        # update max column length for the excel sheet
        max_col_len = post_process.update_max_excel_column_len(max_col_len, route_info)

    # post process data, sort routes by area
    # todo: post process data can be done by read from excel data first,
    # todo: and then post process. In this case, excel main sheet can be treat as a data base
    route_info_list_by_area = post_process.categorize_by_area(route_info_list)

    # save to excel sheet
    # todo: write to file everytime vs save to file after every N route info is collected.
    # todo: when number of routes are getting large, it requires more cache space
    write_to_file.gen_new_excel(route_info_list, route_info_list_by_area, max_col_len, "demo.xlsx")

    print(f"main end...")


if __name__ == '__main__':
    start_time = time.time()
    main('it is main!')
    print("\n --- %s seconds ---" % (time.time() - start_time))
