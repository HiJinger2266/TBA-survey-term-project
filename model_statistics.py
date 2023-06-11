# Pure statistics

#In[1]
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#In[2]
df_x = pd.read_csv("finalprocess_x.csv")
df_y = pd.read_csv("finalprocess_y.csv")

X = df_x

y_mrt = pd.DataFrame(df_y.pop("mrt"))
y_bus = pd.DataFrame(df_y.pop("bus"))
y_car = pd.DataFrame(df_y.pop("car"))
y_motorpri = pd.DataFrame(df_y.pop("motorpri"))
y_motorsha = pd.DataFrame(df_y.pop("motorsha"))
y_bikepri = pd.DataFrame(df_y.pop("bikepri"))
y_bikesha = pd.DataFrame(df_y.pop("bikesha"))
y_walk = pd.DataFrame(df_y.pop("walk"))
y_shuttle = pd.DataFrame(df_y.pop("shuttle"))



#In[3] 簡單畫圖而已
data = [30.3, 17.9, 28.1, 17.3, 3.4, 2.2]
keys = ['Motorcycle', 'Automobile', 'MRT', 'Bus', 'Bicycle', 'Walk']

plt.rcParams.update({'font.size': 14})
palette_color = sns.color_palette("pastel")
plt.pie(data, labels=keys, colors=palette_color, autopct='%.0f%%')
plt.show()



#In[4] Simple logit model
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

z = np.arange(-7, 7, 0.1)
phi_z = sigmoid(z)

plt.plot(z, phi_z)
plt.axvline(0.0, color='k')
plt.ylim(-0.1, 1.1)
plt.xlabel('z')
plt.ylabel('$\phi (z)$')

# y axis ticks and gridline
plt.yticks([0.0, 0.5, 1.0])
ax = plt.gca()
ax.yaxis.grid(True)

plt.tight_layout()
# plt.savefig('./figures/sigmoid.png', dpi=300)
plt.show()



#In[5] Response from survey

c_total = df_y.shape[0]
c_mrt = y_mrt.value_counts()[1]
c_bus = y_bus.value_counts()[1]
c_car = y_car.value_counts()[1]
c_motorpri = y_motorpri.value_counts()[1]
c_motorsha = y_motorsha.value_counts()[1]
c_bikepri = y_bikepri.value_counts()[1]
c_bikesha = y_bikesha.value_counts()[1]
c_walk = y_walk.value_counts()[1]
c_shuttle = y_shuttle.value_counts()[1]

print(c_total)
print(c_mrt)
print(c_bus)
print(c_car)
print(c_motorpri)
print(c_motorsha)
print(c_bikepri)
print(c_bikesha)
print(c_walk)
print(c_shuttle)




#In[6]
# palette = sns.color_palette("Greens_d", 10)
counts = [c_mrt, c_bus, c_car, c_motorpri, c_motorsha, c_bikepri, c_bikesha, c_walk, c_shuttle]
plotdata = pd.DataFrame({
    "vehicle": counts},
    index=["MRT", "Bus", "Private Car", "Private Motorcycle", "Shared Motorcycle", "Private Bicycle", "Shared Bicycle", "Walk", "Shuttle Bus"])
plotdata.plot(kind="bar",figsize=(16, 8), color="purple")
# plt.title("")
# plt.xlabel("Vehicle Choices")
plt.ylabel("Num of Respondents")
plt.rcParams.update({'font.size': 18})
plt.show()

counttable = pd.concat([y_mrt.value_counts(),
                       y_bus.value_counts(),
                       y_car.value_counts(),
                       y_motorpri.value_counts()], axis=1)
print(counttable)




#In[7]
df_old = pd.read_csv("preprocessresult.csv", header=0)
c_rent = df_old["current_living"].value_counts()["rent"]
c_dorm = df_old["current_living"].value_counts()["dormitory"]
c_bot = df_old["current_living"].value_counts()["bot"]
c_toge = df_old["current_living"].value_counts()["together"]
c_home = df_old["current_living"].value_counts()["home"]

countlive = [c_rent, c_dorm, c_bot, c_toge, c_home]
plotdata2 = pd.DataFrame({
    "vehicle": countlive},
    index=["Rent", "Dormitory", "BOT", "Live together", "Home"])
plotdata2.plot(kind="bar",figsize=(16, 8), color="purple")
# plt.title("")
# plt.xlabel("Vehicle Choices")
plt.ylabel("Num of Respondents")
plt.rcParams.update({'font.size': 18})
plt.show()

# %%
