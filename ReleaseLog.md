# Rlease Logs:
# v_0_0_1
this project revision is to collect route information from https://www.mountainproject.com/
current feature inlcudes collect bouldering route information in Washington state based on the grading range provided. 
the output work product is an excel file which includes the main page containing all route infornation, and second tab including number of qualified routes in each the finest crag

the workflow is as below:
1) generate search url, based on the searching criteria specified (get_search_url.py)
2) collect route links by using mountain project search engine (get_route_links.py)
3) visit each route link, save route info into route_info_list (get_route_info.py)
4) post process data, count qualified routes by area (post_process.py)
5) save route information in excel sheet (write_to_file.py)
notes: it currently only supports setting the grading inputs in the main() function instead of using an UI.
