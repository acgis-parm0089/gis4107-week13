# -*- coding: UTF-8 -*-
# ------------------------------------------------------------------------------
# Name:        water_stn_converter.py
#
# Purpose:
#    Converts a JSON file created using the water_stn_downloader module to
#    CSV or KML.
#    For the CSV, the output columns will be:
#      {Station_Number}, {Station_Name}, {Longitude}, {Latitude}, LINK
#
#    where LINK is
#    https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={Station_Number}
#
#    Header for CSV will be:
#      StationNumber, StationName, Longitude, Latitude, WaterOfficeLink
#
#    For the KML, the <Placemark> element will have the following sub-elements:
#              <name>{Station_Name}</name>
#              <description>
#                 link
#              </description>
#              <Point>
#                <coordinates>{Longitude},{Latitude},0</coordinates>
#              </Point>
#
#   Items enclosed by { } are the keys in the dictionary associated with
#   each feature (a key:value dictionary of values).
#
# Author:      Your name(s)
#
# Created:     dd/mm/yyyy
# ------------------------------------------------------------------------------

import json

in_json_filename = ''
out_csv_filename = ''
out_kml_filename = ''

def json_to_csv():
    """Converts a JSON file created using the water_stn_downloader module
    to CSV"""

    # Call load_json_file_to_dict()
    #
    water_stns = load_json_file_to_dict()

    # Create a unicode format string for 5 comma-separated values terminated
    # with a new line character (e.g. u'abc' is a unicode string)
    #
    fmt = u'{},{},{},{},{}\n'

    # Use with to open out_csv_filename
    #
    with open (out_csv_filename, 'w') as out_file:
        # Write the header to the CSV file
        #
        out_file.write('StationNumber, StationName, Longitude, \
                        Latitude, WaterOfficeLink\n')
        # Loop through all the features and write the results to the CSV file
        # NOTE:  use .encode('utf-8') on the string before writing to the file
        #
        for feature in water_stns['features']:
            stn, stn_name, longitude, latitude = get_values_from_feature(feature)
            link = get_wateroffice_link(stn)
            out_rec = fmt.format(stn, stn_name, longitude, latitude, link).encode('utf-8')
            out_file.write(out_rec)


def json_to_kml():
    """Converts a JSON file created using the water_stn_downloader module
    to KML"""

    water_stns = load_json_file_to_dict()

    with open(out_kml_filename, 'w') as kml_file:
        kml_file.write(get_kml_header())
        for feature in water_stns['features']:
            stn, stn_name, longitude, latitude = get_values_from_feature(feature)
            link = get_wateroffice_link(stn)
            kml_file.write(get_placemark(stn_name,longitude, latitude, link))
        kml_file.write(get_kml_footer())
        kml_file.close()


def load_json_file_to_dict():
    """Use json.load(file_object) to convert the contents of in_json_filename
    to a Python dictionary.  Return the resulting dictionary.
    """
    # Use with to open in_json_filename and use that file object as an
    # argument to json.load.  This will return a Python dict with nested
    # lists and dictionaries
    with open(in_json_filename) as in_json_file:
        water_stns = json.load(in_json_file)
    return water_stns

def get_values_from_feature(feature):
    """Given a dictionary of feature attributes, return the following:
        Station_Number, Station_name, Longitude, Latitude  """
    stn = ''
    stn_name = ''
    longitude = 0
    latitude = 0
    stn = feature['attributes']['Station_Number']
    stn_name = feature['attributes']['Station_Name']
    longitude = float(feature['attributes']['Longitude'])
    latitude = float(feature['attributes']['Latitude'])
    return stn, stn_name, longitude, latitude

def get_wateroffice_link(station_number):
    """Given a station_number, return the English wateroffice link"""

    fmt = 'https://wateroffice.ec.gc.ca/report/real_time_e.html?stn={}'
    return fmt.format(station_number)


def get_kml_header():
    """Return the xml header including the Document start tag
    """
    kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>"""
    return kml


def get_kml_footer():
    """Return the document and kml end tags
    """
    kml = """  </Document>\
          </kml>"""
    return kml


# Create a placemark format string that can be used for creating KML Placemark
# elements in get_placemark.  Remember to make this a unicode string since
# some of the placemark content will contain unicode characters
#
pm_fmt = u"""\n  <Placemark>\n    <name>{}</name>
    <description>
        {}
    </description>
    <Point>
        <coordinates>{},{},0</coordinates>
    </Point>
  </Placemark>"""


def get_placemark(name, longitude, latitude, wateroffice_link):
    """Return the KML Placemark element including start and end tags
    NOTE:  .encode('utf-8') is used on the resulting string to ensure
           proper encoding of characters
    """
    global pm_fmt
    kml = pm_fmt.format(name, wateroffice_link, longitude, latitude)
    return kml.encode("utf-8")
