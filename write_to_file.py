# file name: write_to_file.py
# notes: this file includes functions which are used to save data into excel sheet
# todo: depend on the number of routes returned from the search engine, as well as scraping time,
#       consider to save data into excel sheet every n route_info in order to manage the run-time cache usage

import pandas as pd
# from openpyxl import load_workbook
# (mac numbers can't open excel opened and saved by openpyxl 3.0.7)
# issue reference: https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1615


def gen_new_excel(route_info_list, route_info_list_by_area,  max_col_len, file_name):
    # function description:
    #        call sub functions to generate tabs in the excel file with the given file name
    #
    # inputs: route_info_list = [route_info1, route_info2, ...,]
    #         route_info_list_by_area = { 'area1' : [route_info1, route_info2, ..., ],
    #                                     'area2' : [route_info3, route_info4, ..., ],
    #                                     ... }
    #         (route_info = [id, name, grade, location, boulder name, url])
    #
    #         max_col_len = [id col, name col, grade col, location col, boulder name col, url col]
    #         file_name = '****.xlsx'
    # outputs: void
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')  # create new file and writer
    gen_main_sheet(route_info_list, writer)  # generate main sheet including all route info
    gen_route_count_by_area(route_info_list_by_area, writer)  # generate number of routes in each sub-area
    auto_cell_width(max_col_len, writer)  # auto adjust column length
    writer.save()


def gen_main_sheet(route_info_list, writer):
    # function description:
    #         create the main tab collecting all route info from route_info_list
    # inputs:
    #         see parent function
    # output:
    #         void
    # excel tab template is as below:
    # Route ID       Route Name     Route Grade        Route Location              Boulder Name           URL
    # 118640514      The Upsetter          V7        washington->...->five star    five star boulder    http://...
    # 113906598	     El Compadre	      V8-9 	     washington->...->lower main         ...               ...
    # ...
    data_dict = {}
    for route_info in route_info_list:
        data_dict[route_info[0]] = route_info

    df1 = pd.DataFrame.from_dict(data=data_dict, orient='index',
                                 columns=['Route ID', 'Route Name', 'Route Grade', 'Route Location', 'Boulder Name', 'Route URL'])
    df1.to_excel(writer, sheet_name='mainSheet', index=False)


def gen_route_count_by_area(route_info_list_by_area, writer):
    # function description:
    #         create the 'numOfRouteByArea' tab count the number of qualified routes per sub-area
    # inputs:
    #         dictionary (see parent function)
    # output:
    #         void
    # excel tab 'numOfRouteByArea' template is as below:
    #            Location Name                          Number of Routes Qualified
    #   washington->...->bridge of the gods boulders              6
    #   washington->...->skykomish valley                         5
    #                ...                                         ...
    #
    data_dict_sec_sheet = {}
    for area, route_info_list in route_info_list_by_area.items():
        data_dict_sec_sheet[area] = [area, route_info_list.__len__()] # list length indicates the number of qualified routes
    # save data frame for second sheet
    df2 = pd.DataFrame.from_dict(data_dict_sec_sheet, orient='index', columns=['Area Name', 'Route Number'])
    df2.to_excel(writer, sheet_name='numOfRouteByArea', index=False)


def auto_cell_width(max_col_len, writer):
    # function description:
    #       update column length with the max content length in that column
    # inputs:
    #       max_col_len : list (see parent function)
    # outputs:
    #       void
    #
    # set cell width for sheet 'mainSheet'
    worksheet = writer.sheets['mainSheet']
    col_index = 0
    for max_len in max_col_len:
        worksheet.set_column(col_index, col_index, max_len)
        col_index += 1
    # set cell width for sheet 'numOfRouteByArea'
    worksheet = writer.sheets['numOfRouteByArea']
    worksheet.set_column(0, 0, max_col_len[3])


# def gen_route_count_table_by_area(route_info_list_by_area, file_name):
#     # reference:
#     # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.from_dict.html
#     # https://stackoverflow.com/questions/42370977/how-to-save-a-new-sheet-in-an-existing-excel-file-using-pandas
#     # OPEN ISSUE reference: https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1615
#     book = load_workbook("demo.xlsx")
#     writer = pd.ExcelWriter(file_name, engine='openpyxl')
#     writer.book = book
#
#     data_dict = {"area1": 1,
#                  "area2": 2}
#     # for area, route_info_list in route_info_list_by_area.items():
#     #     data_dict[area] = route_info_list.__len__()
#
#     df = pd.DataFrame.from_dict({}, orient='index')
#     df.to_excel(writer, sheet_name='routeNumberByArea', index=False)
#     writer.save()
#     writer.close()


# def gen_sub_location_sheet(route_info_list, file_name):
    # open issue reference: https://foss.heptapod.net/openpyxl/openpyxl/-/issues/1615
    # inputs:
    #       route_info_list = [list1, list2, ... ,listN]
    #           (list1 = [route ID, route name, route grade, route location, route URL])
    #       file_name =  string ('demo.xlsx' for example)
    # outputs:
    #        void
    #
    # Description:
    # generate sub-location sheet which includes routes in that area the sub-location is choose as the finest location,
    # but not the boulder's location. The sheet will be used to fast filter out route info by location and grading.
    #
    # Notes:
    # see below example for sheet name clarification:
    # "washington->olympics pacific coast->olympic national park->olympic bouldering->jefferson lake->roadside boulder"
    # "jefferson lake" will be the sheet name
    #
    # excel sheet template example:
    #              A           B           C       ...      P             Q
    #  col1       v0          v1          v2      ...      v16          v17           (can be extended)
    #  col2      route1     route3      route4    ...     routeN
    #  col3      route2                 route5
    #  ...                              route6
    #                                ...
    #
    # \ tab_name : area name / (not boulder name)
    # example ends
    #
    # writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    # data_dict = {}  # use dictionary data type for excel write
    # for route_info in route_info_list:
    #     data_dict[route_info[0]] = route_info
    #
    # df = pd.DataFrame.from_dict(data=data_dict, orient='index',
    #                             columns=['Route ID', 'Route Name', 'Route Grade', 'Route Location', 'Route URL'])
    # df.to_excel(writer, sheet_name='mainSheet', index=False)
    #
    # # set width for each column
    # worksheet = writer.sheets['mainSheet']
    # col_index = 0
    # for max_len in max_col_len:
    #     worksheet.set_column(col_index, col_index, max_len)
    #     col_index += 1
    #
    # writer.save()