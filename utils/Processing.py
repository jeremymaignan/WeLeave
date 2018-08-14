
class Processing():
    def calc_top(self, estimations):
        if 1 == len(estimations):
            for mode in estimations[0]["modes"]:
                estimations[0]["modes"][mode]["top"] = {
                    "min": estimations[0]["modes"][mode]["prices"]["low"],
                    "max": estimations[0]["modes"][mode]["prices"]["low"]
                }
        else:
            for mode in estimations[-1]["modes"]:
                if estimations[-1]["modes"][mode]["prices"]["low"] < estimations[-2]["modes"][mode]["top"]["min"]:
                    estimations[-1]["modes"][mode]["top"]["min"] = estimations[-1]["modes"][mode]["prices"]["low"]
                else:
                    estimations[-1]["modes"][mode]["top"]["min"] = estimations[-2]["modes"][mode]["top"]["min"]
                if estimations[-1]["modes"][mode]["prices"]["low"] > estimations[-2]["modes"][mode]["top"]["max"]:
                    estimations[-1]["modes"][mode]["top"]["max"] = estimations[-1]["modes"][mode]["prices"]["low"]
                else:
                    estimations[-1]["modes"][mode]["top"]["max"] = estimations[-2]["modes"][mode]["top"]["max"]
        return estimations

    def calc_dynamic_trends(self, estimations):
        if 1 != len(estimations):
            for mode in estimations[-1]["modes"]:
                if estimations[-1]["modes"][mode]["prices"]["low"] < estimations[-2]["modes"][mode]["prices"]["low"]:
                    print("- {}".format(mode))
                    estimations[-1]["modes"][mode]["fluctuations"]["dynamic"] = {
                        "trends": "-",
                        "value": estimations[-2]["modes"][mode]["prices"]["low"] - estimations[-1]["modes"][mode]["prices"]["low"]
                    }
                elif estimations[-1]["modes"][mode]["prices"]["low"] > estimations[-2]["modes"][mode]["prices"]["low"]:
                    print("+ {}".format(mode))
                    estimations[-1]["modes"][mode]["fluctuations"]["dynamic"] = {
                        "trends": "+",
                        "value": estimations[-1]["modes"][mode]["prices"]["low"] - estimations[-2]["modes"][mode]["prices"]["low"]
                    }
                else:
                    estimations[-1]["modes"][mode]["fluctuations"]["dynamic"] = {
                        "trends": "=",
                        "value": 0
                    }
        return estimations

    def calc_global_trends(self, estimations):
        if 1 != len(estimations):
            for mode in estimations[-1]["modes"]:
                if estimations[-1]["modes"][mode]["prices"]["low"] < estimations[0]["modes"][mode]["prices"]["low"]:
                    estimations[-1]["modes"][mode]["fluctuations"]["global"] = {
                        "trends": "-",
                        "value": estimations[0]["modes"][mode]["prices"]["low"] - estimations[-1]["modes"][mode]["prices"]["low"]
                    }
                elif estimations[-1]["modes"][mode]["prices"]["low"] > estimations[0]["modes"][mode]["prices"]["low"]:
                    estimations[-1]["modes"][mode]["fluctuations"]["global"] = {
                        "trends": "+",
                        "value": estimations[-1]["modes"][mode]["prices"]["low"] - estimations[0]["modes"][mode]["prices"]["low"]
                    }
                else:
                    estimations[-1]["modes"][mode]["fluctuations"]["global"] = {
                        "trends": "=",
                        "value": 0
                    }
        return estimations

    def calc_iteration(self, estimations):
        estimations[-1]["iter"] = len(estimations)
        return estimations
 
    def calc_variations(self, estimations):
        estimations = self.calc_top(estimations)
        estimations = self.calc_dynamic_trends(estimations)
        estimations = self.calc_global_trends(estimations)
        estimations = self.calc_iteration(estimations)
        return estimations
