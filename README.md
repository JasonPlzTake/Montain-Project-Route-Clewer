# MontainProjectRouteClewer
Collect bouldering route information from mountain project website

1) This clewer is to collect route information from https://www.mountainproject.com/.

2) The main feature is to collect bouldering route information in Washington state based on the grading range provided. 

    (Route information includes: route name, route id, route grade, route location, route url)

4) The output work product is an excel file, which includes the 

    a. main tab containing all route infornation
    b. second tab including number of qualified routes in each the finest crag
    
    
# The release v0.0.1 includes below workflow:

1) generate search url, based on the searching criteria specified (get_search_url.py)

3) collect route links by using mountain project search engine (get_route_links.py)

5) visit each route link, save route info into route_info_list (get_route_info.py)

7) post process data, count qualified routes by area (post_process.py)

9) save route information in excel sheet (write_to_file.py)
