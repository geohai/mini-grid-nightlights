
# Change Point Analysis

# Key Code for Change Point Analysis

#   tsd = np.array(specific_meter['consump_kwh'])
#         detector = rpt.Pelt(model="rbf").fit(tsd)
#         change_points = detector.predict(pen=penalty)
# has context menu

#  changepoint library in R

import pandas as pd
import numpy as np
import ruptures as rpt
import plotly.express as px
import plotly.graph_objects as go


def create_changepoint_summary_df(df, penalty = 2, show_fig = True):
    # Run through each of the meter_id and then run the change point detection on each of them
    # Then plot the change points for each of the meter_id
    meter_ids = df["meter_id"].unique()
 
    for j in meter_ids:
        # Grab the specific meter
        specific_meter = df[df["meter_id"] == j].reset_index(drop=True)
        # Run the change point detection on the specific meter
 
        tsd = np.array(specific_meter['consump_kwh'])
 
        detector = rpt.Pelt(model="rbf").fit(tsd)
        change_points = detector.predict(pen=penalty)
        ################### penalty #######################
        # plot_change_points_ruptures(tsd, tsd, change_points[:-1], 'Detecting changes in behaviour in daily consuption of electricity')
        # I need to add 0 at the start and then the last value at the end.
        change_points_index = [0] + list(change_points)
        # Remove the last value in change_points_index
        change_points_index = change_points_index[:-1]
        # Add the last value into change_points_index
        change_points_index = change_points_index + [len(tsd) - 1]
 
        # Creating the data frame for the plot
        # Take the specific_meter and then look to aggregate based on the change points.
        for i in change_points_index:
            # Grab the data from the specific_meter between the first and second vlaue in change_points_index
            # Then create the summary metrics for each event detected
            # Then append to a new data frame
            # Then plot the new data frame
            if change_points_index.index(i) == len(change_points_index)-1:
                break
            sum_consump = (specific_meter.iloc[i:change_points_index[change_points_index.index(i)+1]]["consump_kwh"].sum())
            mean_consump = (specific_meter.iloc[i:change_points_index[change_points_index.index(i)+1]]["consump_kwh"].mean())
            var_consump = (specific_meter.iloc[i:change_points_index[change_points_index.index(i)+1]]["consump_kwh"].var())
            payment_sum = (specific_meter.iloc[i:change_points_index[change_points_index.index(i)+1]]["revenue_lc"].sum())
            first_date = specific_meter.iloc[i]["timestamp"]
            second_date = specific_meter.iloc[change_points_index[change_points_index.index(i)+1]]["timestamp"]
            duration = second_date - first_date
 
            # Create a new data frame
            if change_points_index.index(i) == 0:
                new_df = pd.DataFrame({"sum_consump": sum_consump, "mean_consump": mean_consump, "var_consump": var_consump, "duration": duration, "first_date": first_date, }, index=[0])
            else:
                new_df = pd.concat([new_df, (pd.DataFrame({"sum_consump": sum_consump, "mean_consump": mean_consump, "var_consump": var_consump, "duration": duration, "first_date": first_date}, index=[0]))], axis=0)
                # new_df = new_df.append(pd.DataFrame({"sum_consump": sum_consump, "mean_consump": mean_consump, "var_consump": var_consump, "duration": duration, "first_date": first_date}, index=[0]), ignore_index=True)
           
            # new_df.columns = ["Consumption (kWh)", "ACPU (kWh)", "Variance of Consumption", "Duration", "First Date"]
 
            # Check that both for loops are not at the start
            if (change_points_index.index(i) == 0) & (meter_ids[0] == j):
                meter_changepoints = pd.DataFrame({"sum_consump": sum_consump, "mean_consump": mean_consump, "var_consump": var_consump, "duration": duration, "first_date": first_date, "Meter_ID": specific_meter["meter_id"][0], "payment" : payment_sum}, index=[0])
            else:
                # meter_changepoints = meter_changepoints.append(pd.DataFrame({"sum_consump": sum_consump, "mean_consump": mean_consump, "var_consump": var_consump, "duration": duration, "first_date": first_date, "Meter_ID": specific_meter["meter_id"][0], "payment" : payment_sum}, index=[0]), ignore_index=True)
                meter_changepoints = pd.concat([meter_changepoints, (pd.DataFrame({"sum_consump": sum_consump, "mean_consump": mean_consump, "var_consump": var_consump, "duration": duration, "first_date": first_date, "Meter_ID": specific_meter["meter_id"][0], "payment" : payment_sum}, index=[0]))] ,axis = 0)
        new_df.columns = ["Consumption (kWh)", "ACPU (kWh)", "Variance of Consumption", "Duration", "First Date"]
 
        ACPU_Line_df = pd.DataFrame({"First Date": new_df["First Date"], "ACPU (kWh)": new_df["ACPU (kWh)"]})
        # ACPU_Line_df = ACPU_Line_df.append(ACPU_Line_df)
        ACPU_Line_df = pd.concat([ACPU_Line_df, (ACPU_Line_df)], axis=0)
        # print(ACPU_Line_df)
        # Order the data frame by the first date
        ACPU_Line_df = ACPU_Line_df.sort_values(by=["First Date"]).reset_index(drop=True)
        # Move the ACPU values down by 1 index
        ACPU_Line_df["ACPU (kWh)"] = ACPU_Line_df["ACPU (kWh)"].shift(1)
        # Duplicate the last line
        #ACPU_Line_df = ACPU_Line_df.append(ACPU_Line_df.iloc[len(ACPU_Line_df)-1]).reset_index(drop=True)
        # new_ACPU_line_df = (ACPU_Line_df.iloc[(len(ACPU_Line_df)-1)]).reset_index(drop=True)
        # Create a new record for the last line
        new_ACPU_line_df = pd.DataFrame(columns = ["First Date", "ACPU (kWh)"])
        new_ACPU_line_df["First Date"] = ACPU_Line_df["First Date"][len(ACPU_Line_df)-1]
        new_ACPU_line_df["ACPU (kWh)"] = ACPU_Line_df["ACPU (kWh)"][len(ACPU_Line_df)-1]
        ACPU_Line_df = pd.concat([ACPU_Line_df, new_ACPU_line_df], axis = 0)
 
        # Add in a new row to the end of the data frame that takes the last time from specifc meter and the last ACPU value from new_df from ACPU_line_df
        new_ACPU_line_df = pd.DataFrame(columns = ["First Date", "ACPU (kWh)"])
        new_ACPU_line_df["First Date"] = specific_meter["timestamp"][len(specific_meter)-1]
        new_ACPU_line_df["ACPU (kWh)"] = ACPU_Line_df["ACPU (kWh)"][len(new_df)-1]
 
        ACPU_Line_df = pd.concat([ACPU_Line_df, new_ACPU_line_df], axis = 0)
       
        if show_fig == True:
            fig = px.bar(specific_meter, x = "timestamp", y = "consump_kwh", color = "meter_id")
            fig.update_layout(title = f"Electric Consumption (kWh) over time for Meter ID {j}")
            fig.update_yaxes(title = "Consumtpion (kWh)")
            fig.update_xaxes(title = "Date")
 
            # for x in specific_meter["timestamp"][change_points_index]:
            #     fig.add_vline(x, line_width=4, line_dash="dash", line_color="red")
 
            fig.add_trace(go.Scatter(x=ACPU_Line_df["First Date"], y=ACPU_Line_df["ACPU (kWh)"], mode='lines', name='ACPU (kWh)', line=dict(color="seagreen")))
 
            fig.show()
 
        # Append the meter id from the specific_meter to the new_df
        # all_meter_changepoints["Meter ID"] = specific_meter["meter_id"][0]
   
    meter_changepoints.columns = ["Consumption (kWh)", "ACPU (kWh)", "Variance of Consumption", "Duration", "First Date", "Meter ID", "Payment (lc)"]
    meter_changepoints["Duration"] = meter_changepoints["Duration"].dt.days
    meter_changepoints["cost_per_kWh"] = meter_changepoints["Payment (lc)"] / meter_changepoints["Consumption (kWh)"]
    return meter_changepoints