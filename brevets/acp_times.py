"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

def calculate(control_dist_km, speed):
    hours = control_dist_km // speed
    minutes = round(minutes * 60)
    arrow.shift(hours = hours, minutes = minutes)

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    time_intervals = {200: 34, 200-400: 32, 400-600: 30, 600-1000: 28, 1000-1300: 26} 
    hrs = 0.0
    if control_dist_km > brevet_dist_km:
        return 0
    if control_dist_km <= 0 or control_dist_km >1000:
        return 0
    for interval, i in time_intervals:
        distance = min(control_dist_km, interval)
        hours += dist / i
        control_dist_km -= interval
    mins = (hrs - int(hrs)) * 60
    return brevet_start_time.shift(hours = int(hrs), minutes = mins)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    hrs = 0.0
    if control_dist_km < 0:
        return 0;
    if control_dist_km == 0:
        return brevet_start_time.shift(hours = 1)
    if control_dist_km >= brevet_dist_km:
        if brevet_dist_km == 200:
            return brevet_start_time.shift(hours = 13, minutes = 30)
        elif brevet_dist_km == 300:
            return brevet_start_time.shift(hours = 20)
        elif brevet_dist_km == 400:
            return brevet_start_time.shift(hours = 27)
        elif brevet_dist_km == 600:
            return brevet_start_time.shift(hours = 40)
        elif brevet_dist_km == 1000:
            return brevet_start_time.shift(hours = 70)
    if control_dist_km <= 60:
        dist = min(control_dist_km, 60)
        min_speed = 20
        hrs += (dist / min_speed) +1
        control_dist_km -= 60
    else:
        time_intervals = {200: 15, 200-400: 15, 400-600: 15, 600-1000: 11.428, 1000-1300: 13.333}
    for interval, i in time_intervals:
        dist += dist / i
        control_dist_km -= interval
    mins = (hours - int(hrs)) * 60 
    return brevet_start_time.shift(hours = int(hrs), minutes = mins)

