import re

STACK = 64


def extract_coords(text):
    nums = re.findall(r"-?\d+", text)
    if len(nums) >= 3:
        return nums[:3]
    return None


def extract_quantity(text):
    if "stack" in text:
        m = re.search(r"\d+", text)
        if m:
            return int(m.group()) * STACK
        return STACK
    m = re.search(r"\d+", text)
    if m:
        return int(m.group())
    return 1
