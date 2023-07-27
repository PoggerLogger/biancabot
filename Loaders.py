import csv
import yaml


def csv_loader(filepath):
    """Load csv file and return"""
    with open(filepath, 'r', newline='') as file:
        data = csv.reader(file)
        taylist = [[row[0], int(row[1])] for row in data]
    return taylist


def csv_writer(filepath, taylist):
    """Write to csv file in path provided"""
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(taylist)


def yaml_loader(filepath):
    """Load YAML file and return"""
    with open(filepath, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data
