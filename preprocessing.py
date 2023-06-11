import pandas as pd
import numpy as np
import openpyxl

# import pip
# pip.main(["install", "openpyxl"])

# Second row will be the real headers, but I had added new column names in the file
df = pd.read_excel("survey_result_resident_0526.xlsx", header=2)

df.drop_duplicates()

# The first 4 rows have  over 50% missing values, which should be deleted
# This can be done by manual
# df.drop([0,1,2,3], axis=0, inplace=True)

# Living type
df["current_living"].mask(df["current_living"] == "At home", "home", inplace=True)
df["current_living"].mask(df["current_living"] == "School dormitory", "dormitory", inplace=True)
df["current_living"].mask(df["current_living"] == "Rent a house by myself", "rent", inplace=True)
df["current_living"].mask(df["current_living"] == "Relatives and friends home", "together", inplace=True)
df["current_living"].mask(df["current_living"] == "BOT", "bot", inplace=True)

df["current_ideal"] = np.where(df["current_ideal"] == 'Yes', 1, 0)
df["experience_rent"] = np.where(df["experience_rent"] == 'Yes', 1, 0)





# Rent: Monthly rent
rent_month_condition = [(df['rent_month'].isna()),
                        (df['rent_month']=="Below NT$ 5,000"),
                        (df['rent_month']=="NT$ 5,001 ~ NT$ 7,000"),
                        (df['rent_month']=="NT$ 7,001 ~ NT$ 9,000"),
                        (df['rent_month']=="NT$ 9,001 ~ NT$ 11,000"),
                        (df['rent_month']=="NT$ 11,001 ~ NT$ 13,000"),
                        (df['rent_month']=="NT$ 13,001 ~ NT$ 15,000"),
                        (df['rent_month']=="NT$15,001 or above")]
rent_month_value = [0,4,6,8,10,12,14,16]    # 0 indicates nothing here
df['rent_month'] = np.select(rent_month_condition, rent_month_value)

# Rent: If attend lottery of dormitory
rent_iflot_condition = [(df['rent_if_lottery'].isna()),
                        (df['rent_if_lottery']=="Yes, I have won the lottery, but I voluntarily gave up my accommodation or moved out due to various reasons."),
                        (df['rent_if_lottery']=="Yes, but I did not win the lottery or could not live in the dorm/BOT due to various reasons."),
                        (df['rent_if_lottery']=="No, I have never participated in a lottery.")]
rent_iflot_value = [0,1,2,0]    # 0 indicates nothing here
df['rent_if_lottery'] = np.select(rent_iflot_condition, rent_iflot_value)

##### Rent: Vehicle Choice
# https://www.statology.org/pandas-check-if-string-contains-multiple-substrings/
df.insert(df.columns.get_loc("rent_veh_usually"), "rent_MRT", df["rent_veh_usually"].str.contains("MRT"))
df.insert(df.columns.get_loc("rent_veh_usually"), "rent_bus", df["rent_veh_usually"].str.contains("Bus"))
df.insert(df.columns.get_loc("rent_veh_usually"), "rent_car", df["rent_veh_usually"].str.contains("Car"))
df.insert(df.columns.get_loc("rent_veh_usually"), "rent_motorpri", df["rent_veh_usually"].str.contains(r'^(?=.*motorcycle)(?=.*private)'))
df.insert(df.columns.get_loc("rent_veh_usually"), "rent_motorsha", df["rent_veh_usually"].str.contains(r'^(?=.*motorcycle)(?=.*sharing)'))
df.insert(df.columns.get_loc("rent_veh_usually"), "rent_bikepri", df["rent_veh_usually"].str.contains(r'^(?=.*Bicycle)(?=.*private)'))
df.insert(df.columns.get_loc("rent_veh_usually"), "rent_bikesha", df["rent_veh_usually"].str.contains(r'^(?=.*Bicycle)(?=.*sharing)'))
df.insert(df.columns.get_loc("rent_veh_usually"), "rent_walk", df["rent_veh_usually"].str.contains("Walking"))
df["rent_MRT"] = np.where(df["rent_MRT"] == True, 1, 0)
df["rent_bus"] = np.where(df["rent_bus"] == True, 1, 0)
df["rent_car"] = np.where(df["rent_car"] == True, 1, 0)
df["rent_motorpri"] = np.where(df["rent_motorpri"] == True, 1, 0)
df["rent_motorsha"] = np.where(df["rent_motorsha"] == True, 1, 0)
df["rent_bikepri"] = np.where(df["rent_bikepri"] == True, 1, 0)
df["rent_bikesha"] = np.where(df["rent_bikesha"] == True, 1, 0)
df["rent_walk"] = np.where(df["rent_walk"] == True, 1, 0)

# Rent: Do you own something?
df["rent_1280"] = np.where(df["rent_1280"] == 'Yes', 1, 0)

df.insert(df.columns.get_loc("rent_veh_own"), "rent_own_car", df["rent_veh_own"].str.contains("Car"))
df.insert(df.columns.get_loc("rent_veh_own"), "rent_own_motor", df["rent_veh_own"].str.contains("motorcycle"))
df.insert(df.columns.get_loc("rent_veh_own"), "rent_own_bike", df["rent_veh_own"].str.contains("Bicycle"))
df["rent_own_car"] = np.where(df["rent_own_car"] == True, 1, 0)
df["rent_own_motor"] = np.where(df["rent_own_motor"] == True, 1, 0)
df["rent_own_bike"] = np.where(df["rent_own_bike"] == True, 1, 0)

dorm_veh_license_condition = [(df['rent_veh_license'].isna()),
                              (df['rent_veh_license']=="neither of them"),
                              (df['rent_veh_license']=="I hold both a scooter/motorcycle and car license"),
                              (df['rent_veh_license']=="I only have a car license")]
dorm_veh_license_value = [0,0,1,1]
df['rent_veh_license'] = np.select(dorm_veh_license_condition, dorm_veh_license_value)

# Rent: Consideration of vehicle, 只要有排到前三名都被視為重要
df["rent_consider_time"] = np.where(df["rent_consider_time"].isna(), 0, 1)
df["rent_consider_cost"] = np.where(df["rent_consider_cost"].isna(), 0, 1)
df["rent_consider_rely"] = np.where(df["rent_consider_rely"].isna(), 0, 1)
df["rent_consider_flex"] = np.where(df["rent_consider_flex"].isna(), 0, 1)
df["rent_consider_conv"] = np.where(df["rent_consider_conv"].isna(), 0, 1)
df["rent_consider_safe"] = np.where(df["rent_consider_safe"].isna(), 0, 1)
df["rent_consider_cozy"] = np.where(df["rent_consider_cozy"].isna(), 0, 1)
df["rent_consider_envi"] = np.where(df["rent_consider_envi"].isna(), 0, 1)
df["rent_consider_heal"] = np.where(df["rent_consider_heal"].isna(), 0, 1)

# Rent: Deletion
df = df.drop('rent_why_notdorm', axis=1)
df = df.drop('rent_why_dorm', axis=1)
df = df.drop('rent_consider_other', axis=1)
df = df.drop('rent_veh_usually', axis=1)
df = df.drop('rent_veh_time', axis=1)
df = df.drop('rent_veh_cost', axis=1)
df = df.drop('rent_veh_own', axis=1)







# Dormitory: Type
dorm_type_condition = [(df['dorm_type'].isna()),
                       (df['dorm_type']=="School dormitory, less than NT$10,000 per semester"),
                       (df['dorm_type']=="School dormitory, NT$10,001 or more per semester"),
                       (df['dorm_type']=="BOT Single room"),
                       (df['dorm_type']=="BOT Twin room")]
dorm_type_value = [0,1,2,3,4]
df['dorm_type'] = np.select(dorm_type_condition, dorm_type_value)
df["dorm_if_out"] = np.where(df["dorm_if_out"] == "Yes", 1, 0)

##### Dormitory: Vehicle Choice
df.insert(df.columns.get_loc("dorm_veh_usually"), "dorm_MRT", df["dorm_veh_usually"].str.contains("MRT"))
df.insert(df.columns.get_loc("dorm_veh_usually"), "dorm_bus", df["dorm_veh_usually"].str.contains("Bus"))
df.insert(df.columns.get_loc("dorm_veh_usually"), "dorm_car", df["dorm_veh_usually"].str.contains("Car"))
df.insert(df.columns.get_loc("dorm_veh_usually"), "dorm_motorpri", df["dorm_veh_usually"].str.contains(r'^(?=.*motorcycle)(?=.*private)'))
df.insert(df.columns.get_loc("dorm_veh_usually"), "dorm_motorsha", df["dorm_veh_usually"].str.contains(r'^(?=.*motorcycle)(?=.*sharing)'))
df.insert(df.columns.get_loc("dorm_veh_usually"), "dorm_bikepri", df["dorm_veh_usually"].str.contains(r'^(?=.*Bicycle)(?=.*private)'))
df.insert(df.columns.get_loc("dorm_veh_usually"), "dorm_bikesha", df["dorm_veh_usually"].str.contains(r'^(?=.*Bicycle)(?=.*sharing)'))
df.insert(df.columns.get_loc("dorm_veh_usually"), "dorm_walk", df["dorm_veh_usually"].str.contains("Walking"))
df.insert(df.columns.get_loc("dorm_veh_usually"), "dorm_shuttle", df["dorm_veh_usually"].str.contains("Shuttle bus"))
df["dorm_MRT"] = np.where(df["dorm_MRT"] == True, 1, 0)
df["dorm_bus"] = np.where(df["dorm_bus"] == True, 1, 0)
df["dorm_car"] = np.where(df["dorm_car"] == True, 1, 0)
df["dorm_motorpri"] = np.where(df["dorm_motorpri"] == True, 1, 0)
df["dorm_motorsha"] = np.where(df["dorm_motorsha"] == True, 1, 0)
df["dorm_bikepri"] = np.where(df["dorm_bikepri"] == True, 1, 0)
df["dorm_bikesha"] = np.where(df["dorm_bikesha"] == True, 1, 0)
df["dorm_walk"] = np.where(df["dorm_walk"] == True, 1, 0)
df["dorm_shuttle"] = np.where(df["dorm_shuttle"] == True, 1, 0)

# Dormitory: If you wish to rent...
dorm_rent_cost_condition = [(df['dorm_rent_cost'].isna()),
                            (df['dorm_rent_cost']=="Below NT$ 5,000"),
                            (df['dorm_rent_cost']=="NT$ 5,001 ~ NT$ 7,000"),
                            (df['dorm_rent_cost']=="NT$ 7,001 ~ NT$ 9,000"),
                            (df['dorm_rent_cost']=="NT$ 9,001 ~ NT$ 11,000"),
                            (df['dorm_rent_cost']=="NT$ 11,001 ~ NT$ 13,000"),
                            (df['dorm_rent_cost']=="NT$ 13,001 ~ NT$ 15,000"),
                            (df['dorm_rent_cost']=="NT$15,001 or above")]
dorm_rent_cost_value = [0,4,6,8,10,12,14,16]    # 0 indicates nothing here
df["dorm_rent_cost"] = np.select(dorm_rent_cost_condition, dorm_rent_cost_value)

# Dormitory: Consider vehicle when rent... 只要有排到前三名都被視為重要
df["dorm_rent_consider_time"] = np.where(df["dorm_rent_consider_time"].isna(), 0, 1)
df["dorm_rent_consider_cost"] = np.where(df["dorm_rent_consider_cost"].isna(), 0, 1)
df["dorm_rent_consider_rely"] = np.where(df["dorm_rent_consider_rely"].isna(), 0, 1)
df["dorm_rent_consider_flex"] = np.where(df["dorm_rent_consider_flex"].isna(), 0, 1)
df["dorm_rent_consider_conv"] = np.where(df["dorm_rent_consider_conv"].isna(), 0, 1)
df["dorm_rent_consider_safe"] = np.where(df["dorm_rent_consider_safe"].isna(), 0, 1)
df["dorm_rent_consider_cozy"] = np.where(df["dorm_rent_consider_cozy"].isna(), 0, 1)
df["dorm_rent_consider_envi"] = np.where(df["dorm_rent_consider_envi"].isna(), 0, 1)
df["dorm_rent_consider_heal"] = np.where(df["dorm_rent_consider_heal"].isna(), 0, 1)

# Dormitory: Do you own something?
df.insert(df.columns.get_loc("dorm_veh_own"), "dorm_own_car", df["dorm_veh_own"].str.contains("Car"))
df.insert(df.columns.get_loc("dorm_veh_own"), "dorm_own_motor", df["dorm_veh_own"].str.contains("motorcycle"))
df.insert(df.columns.get_loc("dorm_veh_own"), "dorm_own_bike", df["dorm_veh_own"].str.contains("Bicycle"))
df["dorm_own_car"] = np.where(df["dorm_own_car"] == True, 1, 0)
df["dorm_own_motor"] = np.where(df["dorm_own_motor"] == True, 1, 0)
df["dorm_own_bike"] = np.where(df["dorm_own_bike"] == True, 1, 0)

dorm_veh_license_condition = [(df['dorm_veh_license'].isna()),
                              (df['dorm_veh_license']=="neither of them"),
                              (df['dorm_veh_license']=="I hold both a scooter/motorcycle and car license"),
                              (df['dorm_veh_license']=="I only have a car license")]
dorm_veh_license_value = [0,0,1,1]
df['dorm_veh_license'] = np.select(dorm_veh_license_condition, dorm_veh_license_value)

# Dormitory: Deletion
df = df.drop('dorm_why_dorm', axis=1)
df = df.drop('dorm_why_if_out', axis=1)
df = df.drop('dorm_veh_usually', axis=1)        # 前面已經轉換成各類運具
df = df.drop('dorm_veh_time', axis=1)
df = df.drop('dorm_veh_cost', axis=1)
df = df.drop('dorm_rent_cost', axis=1)
df = df.drop('dorm_rent_veh', axis=1)
df = df.drop('dorm_rent_veh_time', axis=1)
df = df.drop('dorm_rent_veh_cost', axis=1)
df = df.drop('dorm_rent_consider_other', axis=1)
df = df.drop('dorm_veh_own', axis=1)






# Home: If attend lottery of dormitory
home_iflot_condition = [(df['home_if_lottery'].isna()),
                        (df['home_if_lottery']=="Yes, I have won the lottery, but I voluntarily gave up my accommodation or moved out due to various reasons."),
                        (df['home_if_lottery']=="Yes, but I did not win the lottery or could not live in the dorm/BOT due to various reasons."),
                        (df['home_if_lottery']=="No, I have never participated in a lottery.")]
home_iflot_value = [0,1,2,0]    # 0 indicates nothing here
df['home_if_lottery'] = np.select(home_iflot_condition, home_iflot_value)

# Home: If considered to rent
df["home_if_rent"] = np.where(df["home_if_rent"] == 'Yes', 1, 0)


##### Home: Vehicle Choice
df.insert(df.columns.get_loc("home_veh_usually"), "home_MRT", df["home_veh_usually"].str.contains("MRT"))
df.insert(df.columns.get_loc("home_veh_usually"), "home_bus", df["home_veh_usually"].str.contains("Bus"))
df.insert(df.columns.get_loc("home_veh_usually"), "home_car", df["home_veh_usually"].str.contains("Car"))
df.insert(df.columns.get_loc("home_veh_usually"), "home_motorpri", df["home_veh_usually"].str.contains(r'^(?=.*motorcycle)(?=.*private)'))
df.insert(df.columns.get_loc("home_veh_usually"), "home_motorsha", df["home_veh_usually"].str.contains(r'^(?=.*motorcycle)(?=.*sharing)'))
df.insert(df.columns.get_loc("home_veh_usually"), "home_bikepri", df["home_veh_usually"].str.contains(r'^(?=.*Bicycle)(?=.*private)'))
df.insert(df.columns.get_loc("home_veh_usually"), "home_bikesha", df["home_veh_usually"].str.contains(r'^(?=.*Bicycle)(?=.*sharing)'))
df.insert(df.columns.get_loc("home_veh_usually"), "home_walk", df["home_veh_usually"].str.contains("Walking"))
df["home_MRT"] = np.where(df["home_MRT"] == True, 1, 0)
df["home_bus"] = np.where(df["home_bus"] == True, 1, 0)
df["home_car"] = np.where(df["home_car"] == True, 1, 0)
df["home_motorpri"] = np.where(df["home_motorpri"] == True, 1, 0)
df["home_motorsha"] = np.where(df["home_motorsha"] == True, 1, 0)
df["home_bikepri"] = np.where(df["home_bikepri"] == True, 1, 0)
df["home_bikesha"] = np.where(df["home_bikesha"] == True, 1, 0)
df["home_walk"] = np.where(df["home_walk"] == True, 1, 0)

# Home: Consider vehicle when rent... 只要有排到前三名都被視為重要
df["home_rent_consider_time"] = np.where(df["home_rent_consider_time"].isna(), 0, 1)
df["home_rent_consider_cost"] = np.where(df["home_rent_consider_cost"].isna(), 0, 1)
df["home_rent_consider_rely"] = np.where(df["home_rent_consider_rely"].isna(), 0, 1)
df["home_rent_consider_flex"] = np.where(df["home_rent_consider_flex"].isna(), 0, 1)
df["home_rent_consider_conv"] = np.where(df["home_rent_consider_conv"].isna(), 0, 1)
df["home_rent_consider_safe"] = np.where(df["home_rent_consider_safe"].isna(), 0, 1)
df["home_rent_consider_cozy"] = np.where(df["home_rent_consider_cozy"].isna(), 0, 1)
df["home_rent_consider_envi"] = np.where(df["home_rent_consider_envi"].isna(), 0, 1)
df["home_rent_consider_heal"] = np.where(df["home_rent_consider_heal"].isna(), 0, 1)

# Home: Do you own something?
df["home_1280"] = np.where(df["home_1280"] == 'Yes', 1, 0)

df.insert(df.columns.get_loc("home_veh_own"), "home_own_car", df["home_veh_own"].str.contains("Car"))
df.insert(df.columns.get_loc("home_veh_own"), "home_own_motor", df["home_veh_own"].str.contains("motorcycle"))
df.insert(df.columns.get_loc("home_veh_own"), "home_own_bike", df["home_veh_own"].str.contains("Bicycle"))
df["home_own_car"] = np.where(df["home_own_car"] == True, 1, 0)
df["home_own_motor"] = np.where(df["home_own_motor"] == True, 1, 0)
df["home_own_bike"] = np.where(df["home_own_bike"] == True, 1, 0)

dorm_veh_license_condition = [(df['home_veh_license'].isna()),
                              (df['home_veh_license']=="neither of them"),
                              (df['home_veh_license']=="I hold both a scooter/motorcycle and car license"),
                              (df['home_veh_license']=="I only have a car license")]
dorm_veh_license_value = [0,0,1,1]
df['home_veh_license'] = np.select(dorm_veh_license_condition, dorm_veh_license_value)

# Home: Deletion
df = df.drop('home_why_rent', axis=1)
df = df.drop('home_why_notdorm', axis=1)
df = df.drop('home_why_dorm', axis=1)
df = df.drop('home_veh_usually', axis=1)
df = df.drop('home_veh_time', axis=1)
df = df.drop('home_veh_cost', axis=1)
df = df.drop('home_rent_cost', axis=1)
df = df.drop('home_rent_veh', axis=1)
df = df.drop('home_rent_veh_time', axis=1)
df = df.drop('home_rent_veh_cost', axis=1)
df = df.drop('home_rent_consider_other', axis=1)
df = df.drop('home_veh_own', axis=1)





# Skip the scenarios
df = df.drop('s01_choice', axis=1)
df = df.drop('s01_veh', axis=1)
df = df.drop('s02_choice', axis=1)
df = df.drop('s02_veh', axis=1)
df = df.drop('s03_choice', axis=1)
df = df.drop('s03_veh', axis=1)
df = df.drop('s04_choice', axis=1)
df = df.drop('s04_veh', axis=1)
df = df.drop('s05_choice', axis=1)
df = df.drop('s05_veh', axis=1)
df = df.drop('s06_choice', axis=1)
df = df.drop('s06_veh', axis=1)
df = df.drop('s07_choice', axis=1)
df = df.drop('s07_veh', axis=1)
df = df.drop('s08_choice', axis=1)
df = df.drop('s08_veh', axis=1)
df = df.drop('s09_choice', axis=1)
df = df.drop('s09_veh', axis=1)
df = df.drop('s10_choice', axis=1)
df = df.drop('s10_veh', axis=1)
df = df.drop('s11_choice', axis=1)
df = df.drop('s11_veh', axis=1)
df = df.drop('s12_choice', axis=1)
df = df.drop('s12_veh', axis=1)





# Preferences (0 Very unimportant, 5 Very important)
def preference_score(df, columnname):
    condition = [(df[columnname]=="Very unimportant"),
                 (df[columnname]=="Unimportant"),
                 (df[columnname]=="Neutral"),
                 (df[columnname]=="Important"),
                 (df[columnname]=="Very important")]
    output = [-2,-1,0,1,2]
    return np.select(condition, output)

df["prefer_rent_price"] = preference_score(df, "prefer_rent_price")
df["prefer_time"] = preference_score(df, "prefer_time")
df["prefer_dist"] = preference_score(df, "prefer_dist")
df["prefer_cost"] = preference_score(df, "prefer_cost")
df["prefer_roomtype"] = preference_score(df, "prefer_roomtype")
df["prefer_together"] = preference_score(df, "prefer_together")
df["prefer_food"] = preference_score(df, "prefer_food")
df["prefer_mall"] = preference_score(df, "prefer_mall")
df["prefer_shop"] = preference_score(df, "prefer_shop")
df["prefer_agency"] = preference_score(df, "prefer_agency")
df["prefer_finance"] = preference_score(df, "prefer_finance")
df["prefer_hospital"] = preference_score(df, "prefer_hospital")
df["prefer_metro"] = preference_score(df, "prefer_metro")
df["prefer_bus"] = preference_score(df, "prefer_bus")
df["prefer_motorshare"] = preference_score(df, "prefer_motorshare")
df["prefer_youbike"] = preference_score(df, "prefer_youbike")
df["prefer_youbikeE"] = preference_score(df, "prefer_youbikeE")
df["prefer_bikefac"] = preference_score(df, "prefer_bikefac")
df["prefer_pedfac"] = preference_score(df, "prefer_pedfac")
df["prefer_accident"] = preference_score(df, "prefer_accident")
df["prefer_route"] = preference_score(df, "prefer_route")
df["prefer_nightride"] = preference_score(df, "prefer_nightride")
df["prefer_clean"] = preference_score(df, "prefer_clean")
df["prefer_quiet"] = preference_score(df, "prefer_quiet")
df["prefer_park"] = preference_score(df, "prefer_park")
df["prefer_safe"] = preference_score(df, "prefer_safe")
df["prefer_balcony"] = preference_score(df, "prefer_balcony")
df["prefer_legalhouse"] = preference_score(df, "prefer_legalhouse")
df["prefer_elevator"] = preference_score(df, "prefer_elevator")
df["prefer_gender"] = preference_score(df, "prefer_gender")
df["prefer_emergency"] = preference_score(df, "prefer_emergency")
df["prefer_post"] = preference_score(df, "prefer_post")
df["prefer_pets"] = preference_score(df, "prefer_pets")
df["prefer_cook"] = preference_score(df, "prefer_cook")
df["prefer_counting"] = preference_score(df, "prefer_counting")
df["prefer_garbage"] = preference_score(df, "prefer_garbage")
df["prefer_appli"] = preference_score(df, "prefer_appli")





# About Motorcycles (1 Strongly disagree, 5 Strongly agree)
def agree_score(df, columnname):
    condition = [(df[columnname]=="Strongly disagree"),
                 (df[columnname]=="Disagree"),
                 (df[columnname]=="Neither agree nor disagree"),
                 (df[columnname]=="Agree"),
                 (df[columnname]=="Strongly agree")]
    output = [-2,-1,0,1,2]
    return np.select(condition, output)

df["motor_status"] = agree_score(df, "motor_status")
df["motor_enjoy"] = agree_score(df, "motor_enjoy")
df["motor_need"] = agree_score(df, "motor_need")
df["motor_everyone"] = agree_score(df, "motor_everyone")
df["motor_further"] = agree_score(df, "motor_further")
df["motor_flex"] = agree_score(df, "motor_flex")
df["motor_conv"] = agree_score(df, "motor_conv")
df["motor_no_danger"] = agree_score(df, "motor_no_danger")
df["motor_rely"] = agree_score(df, "motor_rely")
df["motor_no_alter"] = agree_score(df, "motor_no_alter")
df["share_envi"] = agree_score(df, "share_envi")
df["share_cool"] = agree_score(df, "share_cool")
df["share_cheap"] = agree_score(df, "share_cheap")
df["share_cozy"] = agree_score(df, "share_cozy")
df["share_altermotor"] = agree_score(df, "share_altermotor")
df["share_no_empty"] = agree_score(df, "share_no_empty")
df["share_no_full"] = agree_score(df, "share_no_full")
df["own_motor"] = np.where(df["own_motor"] == "Yes", 1, 0)  # Yes and No
df["own_plan_motor"] = agree_score(df, "own_plan_motor")

# About Bicycles (1 Strongly disagree, 5 Strongly agree)
df["bike_enjoy"] = agree_score(df, "bike_enjoy")
df["bike_heal"] = agree_score(df, "bike_heal")
df["bike_envi"] = agree_score(df, "bike_envi")
df["bike_no_leisure"] = agree_score(df, "bike_no_leisure")
df["bike_need"] = agree_score(df, "bike_need")
df["bike_everyone"] = agree_score(df, "bike_everyone")
df["bike_time"] = agree_score(df, "bike_time")
df["bike_flex"] = agree_score(df, "bike_flex")
df["bike_conv"] = agree_score(df, "bike_conv")
df["bike_no_danger"] = agree_score(df, "bike_no_danger")
df["bike_rely"] = agree_score(df, "bike_rely")
df["youbike_station"] = agree_score(df, "youbike_station")
df["youbike_envi"] = agree_score(df, "youbike_envi")
df["youbike_no_empty"] = agree_score(df, "youbike_no_empty")
df["youbike_no_full"] = agree_score(df, "youbike_no_full")
df["youbike_alterbike"] = agree_score(df, "youbike_alterbike")
df["youbike_easy"] = agree_score(df, "youbike_easy")
df["own_bike"] = np.where(df["own_bike"] == "Yes", 1, 0)  # Yes and No
df["own_plan_bike"] = agree_score(df, "own_plan_bike")





# Basic Info
df["gender"] = np.where(df["gender"] == "Male (physiologically)", 1, 0)  # 1: Male, 0: Female
df = df.drop('gender_psycho', axis=1)
NTUs_condition = [(df["university"]=="National Taiwan University"),
                  (df["university"]=="National Taiwan University of Science and Technology"),
                  (df["university"]=="National Taiwan Normal University")]
NTUs_output = [1,1,1]       # 0 if not from above three universities，這邊我先幹掉
df["university"] = np.select(NTUs_condition, NTUs_output)
df = df.loc[df["university"] != 0]

df = df.drop('dept', axis=1)
grade_condition = [(df["grade"]=="Freshman"),
                   (df["grade"]=="Sophomore"),
                   (df["grade"]=="Junior"),
                   (df["grade"]=="Senior"),
                   (df["grade"]=="Fifth year undergraduate"),
                   (df["grade"]=="Sixth year or above undergraduate"),
                   (df["grade"]=="Graduate student (first year)"),
                   (df["grade"]=="Graduate student (second year)"),
                   (df["grade"]=="Graduate student (third year)"),
                   (df["grade"]=="Graduate student (fourth year or above)"),
                   (df["grade"]=="Ph.D. program")]
grade_output = [1,2,3,4,5,6,5,6,7,8,9]     # 0 不應該出現在這，這邊我先幹掉
df["grade"] = np.select(grade_condition, grade_output)
df = df.loc[df["grade"] != 0]

income_condition = [(df["income"]=="Below NT$ 5,000"),
                    (df["income"]=="NT$ 5,001~7,500"),
                    (df["income"]=="NT$ 7,501~10,000"),
                    (df["income"]=="NT$ 10,001~12,500"),
                    (df["income"]=="NT$ 12,501~15,000"),
                    (df["income"]=="NT$ 15,001~17,500"),
                    (df["income"]=="NT$ 17,501~20,000"),
                    (df["income"]=="NT$ 20,001~22,500"),
                    (df["income"]=="NT$ 22,501~25,000"),
                    (df["income"]=="NT$ 25,001~27,500"),
                    (df["income"]=="NT$ 27,501~30,000"),
                    (df["income"]=="NT$ 30,001 or above")]
income_output = [3.75, 6.25, 8.75, 11.25, 13.75, 16.25, 18.75, 21.25, 23.75, 26.25, 28.75, 31.25]
df["income"] = np.select(income_condition, income_output)

familyeco_condition = [(df["familyeco"]=="Extremely difficult"),
                       (df["familyeco"]=="Difficult"),
                       (df["familyeco"]=="Average"),
                       (df["familyeco"]=="Moderate"),
                       (df["familyeco"]=="Affluent"),
                       (df["familyeco"]=="Prefer not to disclose"),]        # 視為普通人
familyeco_output = [1,2,3,4,5,3]
df["familyeco"] = np.select(familyeco_condition, familyeco_output)

df["job"] = np.where(df["job"] == "Yes", 1, 0)              # 非是即非
df["single"] = np.where(df["single"] == "Yes", 1, 0)        # 非是即非
df["pets"] = np.where(df["pets"] == "Yes", 1, 0)            # 非是即非



pd.set_option("display.max_rows", 10)
pd.set_option("display.max_columns", 14)
print(df)


df.to_csv("preprocessresult.csv", index=False)

# print(df["familyeco"].value_counts())
# print(df.loc[df["income"] == 0])