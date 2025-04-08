import json
import random


def load_conf(conf_path):
    with open(conf_path, 'r') as file:
        return json.load(file)


def generate_versions(version):
    symbols = version.split('.')
    versions = [[str(random.randint(0, 9)) if symbol == '*' else symbol for symbol in symbols] for _ in range(2)]
    return versions


def show_sort(my_list):
    for vers in my_list:
        print('.'.join(vers))


def old_versions(my_vers, my_sort):
    old_vers = []
    my_vers = my_vers.split('.')
    my_sort.append(my_vers)
    new_sort = sorted(my_sort)
    for i_list in new_sort:
        if i_list != my_vers:
            old_vers.append(i_list)
        else:
            break
    return old_vers


if __name__ == "__main__":
    conf = load_conf('config.json')
    new_versions = []
    for key, value in conf.items():
        new_value = generate_versions(value)
        new_versions.extend(new_value)
        print(f'{key}: {conf[key]} -> {new_value}' )
    sort_vers = sorted(new_versions)
    print('\nОтсортированный список:')
    show_sort(sort_vers)
    new_sorted = old_versions("2.7.3", sort_vers)
    print('\nВерсии старше', "2.7.3")
    show_sort(new_sorted)
