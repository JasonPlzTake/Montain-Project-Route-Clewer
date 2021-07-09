# MontainProjectRouteClewer
Collect bouldering route information from mountain project website

# this function is to collect route information from https://www.mountainproject.com/
# the workflow is as below:
# 1) generate search url, based on the searching criteria specified (get_search_url.py)
# 2) collect route links by using mountain project search engine (get_route_links.py)
# 3) visit each route link, save route info into route_info_list (get_route_info.py)
# 4) post process data, count qualified routes by area (post_process.py)
# 5) save route information in excel sheet (write_to_file.py)
