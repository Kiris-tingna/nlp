from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Simple Ratio
r = fuzz.ratio("this is a test", "this is a test!")
print(r)
# Partial Ratio
r = fuzz.partial_ratio("this is a test", "this is a test!")
print(r)
# Token Sort Ratio
r1 = fuzz.ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")
r2 = fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")
print(r1, r2)
# Token Set Ratio
r1 = fuzz.token_sort_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
r2 = fuzz.token_set_ratio("fuzzy was a bear", "fuzzy fuzzy was a bear")
print(r1, r2)
