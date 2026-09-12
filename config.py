GRAVITY = 9.81
SAFETY_FACTOR = 2.0

# Example 6-axis robot. Replace these values with O1 data later.
LINKS = [
    {"name": "J1", "length": 0.30, "mass": 1.2, "com": 0.15},
    {"name": "J2", "length": 0.40, "mass": 1.8, "com": 0.20},
    {"name": "J3", "length": 0.30, "mass": 1.0, "com": 0.15},
    {"name": "J4", "length": 0.20, "mass": 0.7, "com": 0.10},
    {"name": "J5", "length": 0.15, "mass": 0.5, "com": 0.075},
    {"name": "J6", "length": 0.10, "mass": 0.3, "com": 0.05},
]

PAYLOAD = {"mass": 5.0, "distance": 0.80}

# Candidate motor/gearbox data for the calculator demo.
# These are example engineering values, not purchase recommendations.
MOTOR_OPTIONS = [
    {"name": "Motor A", "continuous_nm": 1.5, "peak_nm": 3.0, "rpm": 3000},
    {"name": "Motor B", "continuous_nm": 3.0, "peak_nm": 6.0, "rpm": 3000},
    {"name": "Motor C", "continuous_nm": 5.0, "peak_nm": 10.0, "rpm": 2000},
]

GEARBOX_OPTIONS = [
    {"name": "Gear 10:1", "ratio": 10.0, "efficiency": 0.90},
    {"name": "Gear 20:1", "ratio": 20.0, "efficiency": 0.85},
    {"name": "Gear 50:1", "ratio": 50.0, "efficiency": 0.80},
]
