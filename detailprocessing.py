# Try to apply multinomial logit model
# But some responses had chosen several preferring vehicles
import pandas as pd
import numpy as np

df_x = pd.DataFrame()
df_y = pd.DataFrame()

df = pd.read_csv("preprocessresult.csv", header=0)
df["id"] = df.index + 1     # R 需要 id，但是 python 不用

# Results are binaries of various of vehicles
df_y["mrt"] = df.rent_MRT + df.dorm_MRT + df.home_MRT
df_y["bus"] = df.rent_bus + df.dorm_bus + df.home_bus
df_y["car"] = df.rent_car + df.dorm_car + df.home_car
df_y["motorpri"] = df.rent_motorpri + df.dorm_motorpri + df.home_motorpri
df_y["motorsha"] = df.rent_motorsha + df.dorm_motorsha + df.home_motorsha
df_y["bikepri"] = df.rent_bikepri + df.dorm_bikepri + df.home_bikepri
df_y["bikesha"] = df.rent_bikesha + df.dorm_bikesha + df.home_bikesha
df_y["walk"] = df.rent_walk + df.dorm_walk + df.home_walk
df_y["shuttle"] = df.dorm_shuttle

# Add the variables we may use
live_condition = [(df["current_living"]=="rent"),
                  (df["current_living"]=="dormitory"),
                  (df["current_living"]=="bot"),
                  (df["current_living"]=="together"),
                  (df["current_living"]=="home")]
rent_output = [1,0,0,0,0]
dorm_output = [0,1,1,0,0]
home_output = [0,0,0,1,1]
df_x["live_rent"] = np.select(live_condition, rent_output)
df_x["live_dorm"] = np.select(live_condition, dorm_output)
df_x["live_home"] = np.select(live_condition, home_output)

df_x["own_1280"] = df.rent_1280 + df.home_1280
df_x["own_car"] = df.rent_own_car + df.dorm_own_car + df.home_own_car
df_x["own_motor"] = df.rent_own_motor + df.dorm_own_motor + df.home_own_motor
df_x["own_bike"] = df.rent_own_bike + df.dorm_own_bike + df.home_own_bike
df_x["own_license"] = df.rent_veh_license + df.dorm_veh_license + df.home_veh_license
df_x["own_plan_bike"] = df["own_plan_bike"]
df_x["own_plan_motor"] = df["own_plan_motor"]

df_x["rent_month"] = df["rent_month"]
df_x["rent_satisfy"] = df["current_ideal"]
df_x["rent_experience"] = df["experience_rent"]
df_x["if_lottery"] = df.rent_if_lottery + df.home_if_lottery
df_x["dorm_if_out"] = df["dorm_if_out"]
df_x["home_if_rent"] = df["home_if_rent"]

df_x["consider_time"] = df.rent_consider_time + df.dorm_rent_consider_time + df.home_rent_consider_time
df_x["consider_cost"] = df.rent_consider_cost + df.dorm_rent_consider_cost + df.home_rent_consider_cost
df_x["consider_rely"] = df.rent_consider_rely + df.dorm_rent_consider_rely + df.home_rent_consider_rely
df_x["consider_flex"] = df.rent_consider_flex + df.dorm_rent_consider_flex + df.home_rent_consider_flex
df_x["consider_conv"] = df.rent_consider_conv + df.dorm_rent_consider_conv + df.home_rent_consider_conv
df_x["consider_safe"] = df.rent_consider_safe + df.dorm_rent_consider_safe + df.home_rent_consider_safe
df_x["consider_cozy"] = df.rent_consider_cozy + df.dorm_rent_consider_cozy + df.home_rent_consider_cozy
df_x["consider_envi"] = df.rent_consider_envi + df.dorm_rent_consider_envi + df.home_rent_consider_envi
df_x["consider_heal"] = df.rent_consider_heal + df.dorm_rent_consider_heal + df.home_rent_consider_heal

df_x["prefer_time"] = df["prefer_time"]
df_x["prefer_dist"] = df["prefer_dist"]
df_x["prefer_cost"] = df["prefer_cost"]


df_x["gender"] = df["gender"]
df_x["grade"] = df["grade"]
df_x["income"] = df["income"]
df_x["familyeco"] = df["familyeco"]
df_x["job"] = df["job"]
df_x["single"] = df["single"]
df_x["pets"] = df["pets"]

# df_x["rent_cheap_5000"] = np.where(df["rent_month"] == 1, 1, 0)
# df_x["rent_expen_10000"] = np.where(df["rent_month"] > 4, 1, 0)

# drop 刪掉指定 column，pop 只留指定 column




df_x.to_csv("finalprocess_x.csv", index=False)
df_y.to_csv("finalprocess_y.csv", index=False)		
print(df_x)
print(df_y)