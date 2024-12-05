import requests
import re
from bs4 import BeautifulSoup


def read_file(
    link: str = 'https://www.cftc.gov/dea/futures/deanymesf.htm',
) -> list:
    """
    Fetches content in a URL and returns the text inside as a list, line by line
    """

    # get the response from link
    r = requests.get(
        url=link,
        )

    # check if request successful
    if r.status_code == 200:
        
        content = r.text

        # parse the response w BeautifulSoup
        soup = BeautifulSoup(
            markup=content,
            features='html.parser'
            )

        # from inspecting the link, data is inside the 'pre' tags
        pre_tags = soup.find_all('pre')

        # split the data by lines
        if pre_tags:

            data = pre_tags[0].get_text().split("\n")
            return data

        return []

    else:
        # ideally, use a logger instead of prints
        print(f'Request unsuccesful, error code: {r.status_code}')

        return []


def find_values(
    data: list
) -> dict:

    """
    Extract the contract name and open interest values from data
    """

    # clean up the data, could be made into its own function
    # might not even be that necessary, mostly used to trim top lines
    cleaned_data = [entry for entry in data if entry not in ['\r',' \r']]

    # initialise the empty dictionary we will append values to
    contracts = {'contract': 'open_interest'}

    # assuming the tickets come through in a standard format,
    # extract the contract name and open interest values
    # the below could be made much more robust
    for index in range(0, len(cleaned_data), 16):

        try:
            contract_name = cleaned_data[index].split('-')[0].strip()

            match = re.search(r"OPEN INTEREST:\s*([\d,]+)", cleaned_data[index+7])
            open_interest_vals = match.group(1).replace(',', '')

            contracts[contract_name] = open_interest_vals
        except:
            continue

    return contracts


def main():
    
    data = read_file()
    contracts = find_values(data=data)
    
    # print the contents line for line
    for key, val in contracts.items():
        print(f'{key},{val}')


if __name__ == '__main__':
    main()