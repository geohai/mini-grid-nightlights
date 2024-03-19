# this code gives quantitative measures of the difference between the test and control groups.
# The code is written in Python and uses the pandas and numpy libraries.
# The code is written by Charles Sweetland and is used to calculate the mean absolute percentage difference (MAPD) between the test and control groups.
# Proves statistically that they're valid

import numpy as np
import pandas as pd

def calculate_mapd(tc_data):
    regression_window_size = 12 # Hard-coded here for now: use the previous 12 months to fit the regression
    hm = tc_data.pivot(index="Timestamp", columns="Subset", values="Consumption")
    hm['xTx'] = hm["Test"] * hm["Test"]
    hm["xTx"] = hm["xTx"].rolling(regression_window_size).sum()
    hm['xTy'] = hm["Test"] * hm["Control"]
    hm["xTy"] = hm["xTy"].rolling(regression_window_size).sum()
    hm["beta"] = hm["xTy"] / hm["xTx"]
    # Report beta and check it is steady. 
    print(hm["beta"])
    hm["next 1 control"] = hm["Control"].shift(-1) 
    hm["next 1 test"] = hm["Test"].shift(-1)
    hm["1 APD"] = np.abs(1 - hm["next 1 control"]/(hm["beta"] * hm["next 1 test"])) * 100
 
    hm["next 3 control"] = hm["Control"].rolling(3).sum().shift(-3)
    hm["next 3 test"] = hm["Test"].rolling(3).sum().shift(-3)
    hm["3 APD"] = np.abs(1 - hm["next 3 control"]/(hm["beta"] * hm["next 3 test"])) * 100
 
    hm["next 6 control"] = hm["Control"].rolling(6).sum().shift(-6)
    hm["next 6 test"] = hm["Test"].rolling(6).sum().shift(-6)
    hm["6 APD"] = np.abs(1 - hm["next 6 control"]/(hm["beta"] * hm["next 6 test"])) * 100
    regression_results = hm[["1 APD", "3 APD", "6 APD"]].mean()
 
    foo = tc_data.pivot(index="Timestamp", columns="Subset", values="Scaled Consumption")
    month_scaled = np.mean(np.abs(1 - foo["Control"]/foo["Test"])) * 100
 
    foo = tc_data.pivot(index="Timestamp", columns="Subset", values="Average Consumption")
    month_average = np.mean(np.abs(1 - foo["Control"]/foo["Test"])) * 100
 
    tc_data = tc_data.loc[("2019-09-30" < tc_data["Timestamp"]) & (tc_data["Timestamp"] < "2021-06-15"), :]
    tc_data.loc[:, "Year"] = tc_data["Timestamp"].dt.year
    tc_data.loc[:, "Quarter"] = tc_data["Timestamp"].dt.quarter
 
    foo = tc_data.pivot_table(index=["Year", "Quarter"], columns="Subset", values="Scaled Consumption", aggfunc=np.sum)
    quarter_scaled = np.mean(np.abs(1 - foo["Control"]/foo["Test"])) * 100
    foo = tc_data.pivot_table(index=["Year", "Quarter"], columns="Subset", values="Average Consumption", aggfunc=np.sum)
    quarter_average = np.mean(np.abs(1 - foo["Control"]/foo["Test"])) * 100
 
    tc_data = tc_data.loc["2019-12-30" < tc_data["Timestamp"], :]
    tc_data.loc[:, "Half"] = 2
    tc_data.loc[(tc_data["Quarter"] == 1) | (tc_data["Quarter"] == 2)] = 1
 
    foo = tc_data.pivot_table(index=["Year", "Half"], columns="Subset", values="Scaled Consumption", aggfunc=np.sum)
    half_scaled = np.mean(np.abs(1 - foo["Control"]/foo["Test"])) * 100
    foo = tc_data.pivot_table(index=["Year", "Half"], columns="Subset", values="Average Consumption", aggfunc=np.sum)
    half_average = np.mean(np.abs(1 - foo["Control"]/foo["Test"])) * 100
 
    return pd.DataFrame({
        "Regression, one month window": [regression_results["1 APD"]],
        "Regression, three month window": regression_results["3 APD"],
        "Regression, six month window": regression_results["6 APD"],
        "Scaled, one month window": month_scaled,
        "Scaled, three month window": quarter_scaled,
        "Scaled, six month window": half_scaled,
        "Average, one month window": month_average,
        "Average, three month window": quarter_average,
        "Average, six month window": half_average,
    })
 
def run_backtest(backtest_data, num_trials, test_fraction):
    zones = backtest_data["Zone Name"].unique().tolist()
 
    num_zones = len(zones)
    test_size = math.floor(num_zones * test_fraction)
    control_size = num_zones - test_size
 
    test_scaling_factor = num_zones / test_size
    control_scaling_factor = num_zones / control_size
    scales = pd.DataFrame({"Subset": ["Test", "Control"], "Scaling Factor":[test_scaling_factor, control_scaling_factor]})
 
    results = []
 
    for i in range(num_trials):
        test = sample(zones, test_size)
        test_df = pd.DataFrame({"Zone Name":test})
 
        tc_data = backtest_data.merge(test_df, on="Zone Name", how="outer", indicator=True)
        tc_data.loc[tc_data["_merge"] == "both", "Subset"] = "Test"
        tc_data.loc[tc_data["_merge"] != "both", "Subset"] = "Control"
        tc_data = tc_data.drop(columns=["_merge"])
 
        tc_data = tc_data.groupby(["Subset", "Timestamp"], as_index=False).agg(
            No_Accs = ("No_Accs", "sum"), Consumption= ("Consumption", "sum")
        )
 
        tc_data = tc_data.merge(scales, on="Subset")
        tc_data.loc[:, "Scaled Consumption"] = tc_data["Consumption"] * tc_data["Scaling Factor"]
        tc_data.loc[:, "Average Consumption"] = tc_data["Consumption"] / tc_data["No_Accs"]
 
        results.append(calculate_mapd(tc_data))
    foo = pd.concat(results)
    return foo.mean()
 
# Creating a function for stratification sampling for specific zones to test. 
def match_elements(list_a, list_b):
    match = []
    for i in list_a:
        if i in list_b:
            match.append(i)
    return match
 
# My concern here is that we're merging all of the tests into one master data frame. 
# Should we be comparing each cluster at a time and taking the variability between test and control that way? 
# This is something I'd like to clear up and answer asap!
 
def run_specific_backtest(backtest_data, zones_tested, num_clusters, test_fraction):
    master_tc_data = pd.DataFrame()
    dummy_zones = []
 
    for i in range(num_clusters):
        cluster_df = backtest_data[backtest_data["Labels"] == i]
        zones = cluster_df["Zone Name"].unique().tolist()
        num_zones = len(zones)
        test_size = math.floor(num_zones * test_fraction)
        if (test_size == 0):
            test_size = 1
        control_size = num_zones - test_size
        test_scaling_factor = num_zones / test_size
        control_scaling_factor = num_zones / control_size
 
        scales = pd.DataFrame({"Subset": ["Test", "Control"], "Scaling Factor":[test_scaling_factor, control_scaling_factor]})
 
        test = match_elements(zones, zones_tested)
        test_df = pd.DataFrame({"Zone Name":test})
        tc_data = cluster_df.merge(test_df, on="Zone Name", how="outer", indicator=True)
        tc_data.loc[tc_data["_merge"] == "both", "Subset"] = "Test"
        tc_data.loc[tc_data["_merge"] != "both", "Subset"] = "Control"
        tc_data = tc_data.drop(columns=["_merge"])
 
        # Losing Zone Name 
        dummy_zones.append(tc_data[["Zone Name", "Subset"]].drop_duplicates())
 
        tc_data = tc_data.groupby(["Subset", "Timestamp"], as_index=False).agg(
            No_Accs = ("No_Accs", "sum"), Consumption= ("Consumption", "sum")
        ).reset_index()
 
        tc_data = tc_data.merge(scales, on = "Subset")
        tc_data.loc[:, "Scaled Consumption"] = tc_data["Consumption"] * tc_data["Scaling Factor"]
        tc_data.loc[:, "Average Consumption"] = tc_data["Consumption"] / tc_data["No_Accs"]
        # I'm unsure if this line is problematic!?
        master_tc_data = pd.concat([master_tc_data, tc_data])
 
    master_tc_data2 = master_tc_data.groupby(["Subset", "Timestamp"], as_index=False)["Consumption", "Scaled Consumption", "Average Consumption"].sum().reset_index(drop = True)
    return calculate_mapd(master_tc_data2).sum()