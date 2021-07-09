import requests


def get_html_text(start_url):
    # function description: read url content using requests lib
    # inputs:
    #        start_url: string (url link)
    # output:
    #        html text
    #
    try:
        r = requests.get(start_url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding  # ? double check it can be decoded
        return r.text
    except:
        return ""
