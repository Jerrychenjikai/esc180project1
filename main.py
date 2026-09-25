"""
The following rules apply to how the battery charge, temperature and health are updated:

• Initial battery charge is set by the initialize() function. Battery begins in good
health, at 50% charge and at 20°C temperature.

• The battery is always charging, being used, or sitting idle.

• Charging can be fast or slow. Fast charging increases the charge by 3% per minute, slow
charging by 1% per minute.
• Slow charging increases the temperature by 0.25°C per minute. Fast charging increases
the temperature by 0.5°C per minute.
• Fast charging occurs when the temperature is between 0-40°C, battery charge is below
80%, and battery health is good.

• If fast charging is possible, it will occur. Charging can switch from fast to slow charging
in a single session.

• Usage discharges the battery by 2% per minute. Temperature increases by 1°C per minute
during usage.

• Sitting idle discharges the battery by 0.5% per minute and decreases the temperature by
1°C per minute. The temperature can never go below 0°C.

• If the battery charge reaches 0% during usage or idling, its temperature will decrease by
1°C per minute that it is dead (not going below 0°C), while the charge does not decrease
past 0%.

• Charging at or past 90% reduces the battery health. If this happens 3 times within 6
hours, the battery is in a bad health state.

• Batteries in bad health state cannot charge past 80%. If the battery initially switches to a
bad health state, it will not charge further until discharged below 80%.

• If the battery charge reaches 100% during charging, its temperature will continue to
increase by 0.25°C per minute, while the charge does not increase past 100%. The same
logic applies to if the battery is in a bad health state and reaches 80% during charging, or
if the battery switches to a bad health state and is at or above 90%: the temperature will
increase by 0.25°C per minute, while the battery charge will not increase further.
"""

temp = 20.0
charge = 50.0
health = True
time_elapsed = 0

# these variables define the exact time when the overcharge ENDS
# we are going to be finding the difference between
# the START of the third overcharge and the END of the first
first_overcharge = -9999999999
second_overcharge = -9999999999

def update_overcharge_record(first_instant_over_90): # call this function when the battery is overcharged
    global time_elapsed, first_overcharge, second_overcharge, health

    if (first_instant_over_90 - first_overcharge) <= 360:
        health = False

    first_overcharge = second_overcharge
    second_overcharge = time_elapsed

def get_cur_temp():
    #This function returns the current temperature of the battery, as a float
    
    global temp
    return float(temp)

def get_cur_charge():
    #This function returns the current charge level of the battery, as a float.
    
    global charge
    return float(charge)

def get_cur_battery_health():
    #This function returns the health of the battery, as a boolean. It returns True if the battery is in
    #good health and False if the battery is in bad health.
    
    global health
    return health

def duration_fast_charge_possible():
    #This function returns the duration for which fast charge is possible based on the current battery
    #health, temperature, and charge as a starting point

    global temp
    global charge
    global health

    charge_time = (80 - charge)/3
    temp_time = (40 - temp)/0.5

    charge_time = max(charge_time , 0)
    temp_time = max(temp_time, 0)

    return health * min(charge_time, temp_time)

def fast_charge(charging_time):
    global temp, charge

    charge += charging_time * 3
    temp += charging_time * 0.5

def slow_charge(charging_time):
    global temp, charge

    charge += charging_time * 1.0
    temp += charging_time * 0.25

def max_charge_reached(charging_time):
    global temp

    temp += charging_time * 0.25
    

def simulate_activity(activity, duration):
    #This function simulates the battery performing the activity for duration minutes. Assume
    #duration is a positive int. If the activity is not one of “charge”, “use”, or “idle”, running the
    #function should have no effect.

    global temp, charge, health, time_elapsed

    time_elapsed += duration

    if activity == "charge":
        time_left = duration
        
        # 1. 尝试快充 (Fast Charging)
        # fast charging cannot reach 90%, so no need to consider overcharge
        if health is True and temp < 40 and charge < 80:
            max_fast_time = duration_fast_charge_possible()
            fast_time = min(time_left, max_fast_time)
            
            fast_charge(fast_time)
            time_left -= fast_time
            
        # 2. 慢充 (Slow Charging) - 只有在还有剩余时间时继续
        if time_left > 0:
            target_max_charge = 80.0 if not health else 90.0
            
            if charge < target_max_charge:
                # 计算充到上限还需要多长时间
                # overcharge will only happen here
                time_to_full = (target_max_charge - charge) / 1.0  # 慢充 1%/min
                charging_time = min(time_left, time_to_full)
                
                slow_charge(charging_time)
                time_left -= charging_time

            if charge >= 90:
                instant_at_90 = time_elapsed - time_left - (charge - 90) / 1.0
                instant_at_90 = max(instant_at_90, time_elapsed - duration) #if the battery starts over 90%, then the instant over 90 is at the start of the charging process
                update_overcharge_record(instant_at_90)

            if health:
                target_max_charge = 100.0
                time_to_full = (target_max_charge - charge) / 1.0
                charging_time = min(time_left, time_to_full)

                slow_charge(charging_time)
                time_left -= charging_time
            
            # 3. 达到上限后的处理 (电量不再增加，但温度继续上升)
            if time_left > 0:
                max_charge_reached(time_left)
                time_left = 0

        # 注意：在此处需要补充触发“电量>=90%衰减健康度”的检测逻辑        
    elif activity == "use":
        pass
    elif activity == "idle":
        pass

    
def charge_time_needed(minutes):
    #This function returns the duration needed for charging to enable use for a specific activity
    #duration of minutes afterwards. Based on a future journey, how long does the battery need to
    #charge now to have sufficient battery for minutes use duration? If the battery already has
    #sufficient charge, return 0. If it is impossible for the battery in its current state to be charged to a
    #point where usage for minutes duration can be performed, return None
    
    pass

def initialize():
    #This function initializes all the global variables in the program. The following code should run
    #two independent simulations, with both SIMULATION 1 and SIMULATION 2 starting from the
    #beginning.
    
    global temp
    global charge
    global health
    global time_elapsed
    global first_overcharge, second_overcharge

    temp = 20.0
    charge = 50.0
    health = True
    time_elapsed = 0

    first_overcharge = -9999999999
    second_overcharge = -9999999999

if __name__=="__main__":
    print("hello world")

