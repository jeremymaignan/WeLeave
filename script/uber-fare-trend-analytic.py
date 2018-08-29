#!/usr/local/bin/python3.7

from time import sleep, strftime
from datetime import datetime
from tqdm import tqdm
import sys
from termcolor import colored

from utils.Geo import Geo
from utils.Uber import Uber
from utils.CsvWriter import CsvWriter
from utils.Processing import Processing

def wait(seconds):
    for _ in tqdm(range(seconds)):
        sleep(1)

def get_params():
    geo = Geo()
    from_ = geo.get_coordinates_from_address("From: ")
    if {} == from_:
        sys.exit(0)
    to = geo.get_coordinates_from_address("To: ")
    if {} == to:
        sys.exit(0)
    seat_count = int(input("Seat count: "))
    return from_, to, seat_count

def colored_fluctuation(fluctuation):
    if "-" == fluctuation["trends"]:
        return colored("{}{}€".format(fluctuation["trends"], fluctuation["value"]), 'green')
    elif "+" == fluctuation["trends"]:
        return colored("{}{}€".format(fluctuation["trends"], fluctuation["value"]), 'red')
    else:
        return fluctuation["trends"]

def print_estimation(estimation):
    print("{} {}".format(colored("[{}]".format(estimation["iter"]), "yellow"), colored(estimation["request_time"], "blue")))
    ride_information = estimation["modes"]["Pool"]["ride_information"]
    print("Distance: {}km  Duration: {}min".format(ride_information["distance"], ride_information["duration"] / 60))
    for mode in estimation["modes"]:
        prices = estimation["modes"][mode]["prices"]
        top = estimation["modes"][mode]["top"]
        fluctuation = estimation["modes"][mode]["fluctuations"]
        print('{}\t {}€ \t Range: {}-{}€ \t Trend: {} \t Global: {} \t Min: {}€ \t Max: {}€'.format(
            mode,
            prices["estimation"],
            prices["low"],
            prices["high"],
            colored_fluctuation(fluctuation["dynamic"]),
            colored_fluctuation(fluctuation["global"]),
            top["min"],
            top["max"]
        ))


if __name__ == '__main__':
    from_, to, seat_count = get_params()
    estimations = []
 
    uber = Uber()
    csv_writer = CsvWriter(from_["input"], to["input"])
    processing = Processing()
    while True:
        estimations.append(uber.get_estimation(from_, to, seat_count))
        estimations = processing.calc_variations(estimations)
        print_estimation(estimations[-1])
        estimation_dict = csv_writer.convert_to_csv(estimations)
        csv_writer.write_csv(estimation_dict)
        wait(60)
