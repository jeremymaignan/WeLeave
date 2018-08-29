from time import sleep, strftime
from datetime import datetime
import csv

class CsvWriter:
    def __init__(self, from_, to):
        self.filename = "{}_{}_{}.csv".format(from_, to, datetime.now().strftime("%Y-%m-%d_%H-%M"))

    def convert_to_csv(self, estimations):
        estimation_dict = {}
        for estimation in estimations:
            time = estimation["request_time"]
            for mode in estimation["modes"]:
                if mode not in estimation_dict.keys():
                    estimation_dict[mode] = {}
                tmp = estimation["modes"][mode]
                estimation_dict[mode][time] = {
                    "low": tmp['prices']["low"],
                    "high": tmp['prices']["high"],
                    "trend": tmp["fluctuations"]["dynamic"]['trends'].replace("=", "") + str(tmp["fluctuations"]["dynamic"]['value']),
                    "global": tmp["fluctuations"]["global"]['trends'].replace("=", "") + str(tmp["fluctuations"]["global"]['value']),
                    "min": tmp["top"]["min"],
                    "max": tmp["top"]["max"]
                }
        return estimation_dict

    def write_csv(self, estimations):
        with open(self.filename, 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["Modes", "time", "low_estimation", "high_estimation", "dynamic_trend", "global_trend", "min", "max"])
            for mode in estimations.keys():
                for hour in estimations[mode]:
                    line = [
                        mode,
                        hour,
                        estimations[mode][hour]["low"],
                        estimations[mode][hour]["high"],
                        estimations[mode][hour]["trend"],
                        estimations[mode][hour]["global"],
                        estimations[mode][hour]["min"],
                        estimations[mode][hour]["max"]
                    ]
                    spamwriter.writerow(line)