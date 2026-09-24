print("Hello world")
print("Hello again")

"""
ESC180 Project #1 – Battery Simulator Fall 2026
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
