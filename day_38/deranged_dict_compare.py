large_dict_one = {"one": 1, "two": 2, "three": 3, "deep": {"d1one": 1, "d1two": 2, "d1three": 3, "d1deep": {"d2one": 1}}}
subset_dict_one = {"one": 1}
subset_dict_two = {"one": 1, "two": 2, "deep": {"d1one": 1}}
subset_dict_three = {"one": 1, "two": 2, "deep": {"d1deep": {"d2one": 1}}}
not_subset_dict_one = {"one": "fred"}
not_subset_dict_two = {"one": 1, "two": 2, "deep": "fred"}
not_subset_dict_three = {"one": 1, "two": 2, "deep": {"d1deep": {"d2one": "fred"}}}

deranged_compare_dicts = lambda mass_dict, subset_dict: all(list(map(lambda compare_item: type(compare_item[1]) is dict and deranged_compare_dicts(mass_dict[compare_item[0]], compare_item[1]) or mass_dict.get(compare_item[0], None) == compare_item[1], subset_dict.items())))

print("Should be TRUE -> {}".format(deranged_compare_dicts(large_dict_one, subset_dict_one)))
print("Should be TRUE -> {}".format(deranged_compare_dicts(large_dict_one, subset_dict_two)))
print("Should be TRUE -> {}".format(deranged_compare_dicts(large_dict_one, subset_dict_three)))

print("Should be FALSE -> {}".format(deranged_compare_dicts(large_dict_one, not_subset_dict_one)))
print("Should be FALSE -> {}".format(deranged_compare_dicts(large_dict_one, not_subset_dict_two)))
print("Should be FALSE -> {}".format(deranged_compare_dicts(large_dict_one, not_subset_dict_three)))

