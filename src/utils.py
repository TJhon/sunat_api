import re

test = ["2933.11.10.00	", "2933.33.90.00	- - -"]


def clean_hs(hs):
    hs = str(hs)
    numbers = re.findall(r"\d+", hs)
    hs_code = "".join(numbers)
    return hs_code
