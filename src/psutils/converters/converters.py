import math


def from_deg_to_rad(angle_deg):
    return  angle_deg*math.pi/180


if __name__ == '__main__':
    print(from_deg_to_rad(180))
