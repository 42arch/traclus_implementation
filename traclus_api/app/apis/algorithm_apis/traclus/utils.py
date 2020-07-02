import math

EARTH_REDIUS = 6378.137 * 1000
# EARTH_REDIUS = 6371 * 1000


def calc_distance(lat_a, lng_a, lat_b, lng_b):
    lat_a, lng_a, lat_b, lng_b = map(math.radians, [float(lat_a), float(lng_a), float(lat_b), float(lng_b)])
    d_lon = lng_b - lng_a  # 经度弧度差
    d_lat = lat_b - lat_a  # 纬度弧度差
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat_a) * math.cos(lat_b) * math.sin(d_lon / 2) ** 2
    distance = 2 * math.asin(math.sqrt(a)) * EARTH_REDIUS
    return distance


if __name__ == '__main__':
    d = calc_distance(35.300766422258725, -120.66332459449767, 35.30052125043002, -120.65981626510619)
    print(d)
