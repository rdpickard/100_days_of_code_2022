large_dict_one = {"one": 1, "two": 2, "three": 3, "deep": {"d1one": 1, "d1two": 2, "d1three": 3, "d1deep": {"d2one": 1}}}
subset_dict_one = {"one": 1}
subset_dict_two = {"one": 1, "two": 2, "deep": {"d1one": 1}}
subset_dict_three = {"one": 1, "two": 2, "deep": {"d1deep": {"d2one": 1}}}
not_subset_dict_one = {"one": "fred"}
not_subset_dict_two = {"one": 1, "two": 2, "deep": "fred"}
not_subset_dict_three = {"one": 1, "two": 2, "deep": {"d1deep": {"d2one": "fred"}}}

deranged_compare_dicts = lambda source_dict, compare_item: type(compare_item[1]) is dict and all(list(map(lambda nested_dict_value: deranged_compare_dicts(source_dict[compare_item[0]], nested_dict_value), compare_item[1].items()))) or source_dict.get(compare_item[0],None) == compare_item[1]

print("Should be TRUE -> {}".format(all(list(map(lambda compare_item: deranged_compare_dicts(large_dict_one, compare_item), subset_dict_one.items())))))
print("Should be TRUE -> {}".format(all(list(map(lambda compare_item: deranged_compare_dicts(large_dict_one, compare_item), subset_dict_two.items())))))
print("Should be TRUE -> {}".format(all(list(map(lambda compare_item: deranged_compare_dicts(large_dict_one, compare_item), subset_dict_three.items())))))

print("Should be FALSE -> {}".format(all(list(map(lambda compare_item: deranged_compare_dicts(large_dict_one, compare_item), not_subset_dict_one.items())))))
print("Should be FALSE -> {}".format(all(list(map(lambda compare_item: deranged_compare_dicts(large_dict_one, compare_item), not_subset_dict_two.items())))))
print("Should be FALSE -> {}".format(all(list(map(lambda compare_item: deranged_compare_dicts(large_dict_one, compare_item), not_subset_dict_three.items())))))
