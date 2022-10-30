import sys
import json
import requests
from termcolor import colored
from prettytable import PrettyTable


def checking_requirements():
    # check python version
    python_version = sys.version_info[0]
    if python_version != 3:
        print(colored("[-] Python 3.x is required.", "red"))
        print(colored("[-] Run it with python3", "red"))
        exit()
    else:
        pass


def ip_lookup(ip_address: str) -> None:
    """Function to print table of IP address information such as country, ISP and much more :)

    Args:
        ip_address (str): The Target external ipaddress
    """

    try:
        print(colored(f"[+] Getting geolocation for {colored(ip_address, 'yellow')}", "green"))
        api_response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        ip_info = json.loads(api_response.content) # reading API response
        table = PrettyTable(["Attribute", "Value"])
        table.add_row(["IP Address", ip_info['ip']])
        table.add_row(["Country Name", ip_info['country_name']])
        table.add_row(["City", ip_info['city']])
        table.add_row(["Region", ip_info['region']])
        table.add_row(["Region Code", ip_info['region_code']])
        table.add_row(["Country Capital", ip_info['country_capital']])
        table.add_row(["Longitude", ip_info['longitude']])
        table.add_row(["Latitude", ip_info['latitude']])
        table.add_row(["Time Zone", ip_info['timezone']])
        table.add_row(["Country Calling Code", ip_info['country_calling_code']])
        table.add_row(["Currency", ip_info['currency']])
        table.add_row(["Currency Name", ip_info['currency_name']])
        table.add_row(["Country Language", ip_info['languages']])
        table.add_row(["Country Area (KM)", ip_info['country_area']])
        table.add_row(["Country Population (Person)", int(ip_info['country_population'])])
        table.add_row(["Asn", ip_info['asn']])
        table.add_row(["ISP-ORG", ip_info['org']])
    except Exception as error_msg:
        print(colored(f"[-] Error MSG:\n{error_msg}\n", "red"))
        exit(0)
    finally:
        print(colored(table, "green"))
