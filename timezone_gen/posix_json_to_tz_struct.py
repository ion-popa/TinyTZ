
import json

import pyperclip
'''
Input data example:
{
    "Africa/Abidjan","GMT0",
    "Asia/Baghdad","<+03>-3",
    "Etc/GMT-1","<+01>-1",
}

C++ TZ struct:
typedef struct
{
    const char *region; // e.g. "America"
    const char *city; // e.g. "New_York"
    const char *posix_tz; // e.g. "EST5EDT,M3.2.0,M11.1.0"
}tinytz_posix_tz_t;
'''

def posix_json_to_tz_struct(json_data):
    tz_structs = {}
    for k,v in json_data.items():
        region_city = k
        posix_tz = v
        if '/' in region_city:
            region, city = region_city.split('/', 1)
        else:
            region, city = 'Etc', region_city
        if region not in tz_structs:
            tz_structs[region] = []
        
        tz_structs[region].append({
            'region': region,
            'city': city,
            'posix_tz': posix_tz
        })
    return tz_structs

def tz_struct_to_c_array(tz_structs):
    c_array = "static const tinytz_posix_tz_t tz_data[] = \n{\n"
    for region, tzs in tz_structs.items():
        if region != 'Etc':
            c_array += "#ifdef TINYTZ_{}\n".format(region.upper())
        for tz in tzs:
            c_array += '    {{"{}", "{}", "{}"}},\n'.format(tz['region'], tz['city'], tz['posix_tz'])
        if region != 'Etc':
            c_array += "#endif /* TINYTZ_{} */\n".format(region.upper())
    c_array+= '    {"", "", ""}\n'
    c_array += "};\n"
    return c_array

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        json_data = json.load(f)
    return json_data


def main():
    json_file_path = 'posix_tz_db.json'  # Path to your JSON file
    json_data = read_json_file(json_file_path)
    tz_structs = posix_json_to_tz_struct(json_data)
    c_array = tz_struct_to_c_array(tz_structs)
    print(c_array)
    pyperclip.copy(c_array)

if __name__ == "__main__":
    main()