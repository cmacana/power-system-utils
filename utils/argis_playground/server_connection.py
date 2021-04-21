import json

from arcgis import GIS

a = 10

url_spatial_nsw = "https://portal.spatial.nsw.gov.au/portal"
url_six_nsw = "https://maps.six.nsw.gov.au/"
nsw_spatial_token = "DgPN3jOwsJ-nmEqM8U32YdQBeYQ771WZwt2kBJ6ppA67PHzhIj2a47zJF1Y1w1X-VhImpxQM_uV5fMtiEfifmzHQRbowod8jlRiN8S2Lrn5LPZTLycgwm1zNaGFt9ycv"  # Expires "expires": 1620036856042,

with open('../../results/address-location/argis_credentials.json') as f:
    credentials = json.load(f)

# nsw_gis: GIS = GIS(url=url_spatial_nsw, username=credentials["username"], password=credentials["password"])
# print(f'GIS Server connection was successful. {nsw_gis}')

argis_gis = GIS()
print(f'GIS Server connection was successful. {argis_gis}')

# search_result = gis.content.search(query="", item_type="Feature Layer")
# for result in search_result:
#    print(result)
multi_field_address = {
    "Postal": 2444,
    "source_country": "Australia"
}
# geocoder = get_geocoders(argis_gis)
# result = geocode(address=multi_field_address, geocoder=geocoder)
# extent = result
# print(extent)
# url_act_address = "https://data.actmapi.act.gov.au/arcgis/rest/services/data_extract/Land_Administration/MapServer/7/query?outFields=*&where=1%3D1"
# url_address_points = "https://services6.arcgis.com/i35qCl90qPAzjBmb/arcgis/rest/services/AddressPoint/FeatureServer/0"
# url_nsw_addresses = "https://portal.spatial.nsw.gov.au/server/rest/services/NSW_Geocoded_Addressing_Theme/FeatureServer/1"
# url_postcodes = "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/AUS_Boundaries_2018/FeatureServer"
# url_nsw_address_table = "https://portal.spatial.nsw.gov.au/server/rest/services/NSW_Geocoded_Addressing_Theme/FeatureServer/3"
# layer = FeatureLayer(url_nsw_address_table)
# df: DataFrame = GeoAccessor.from_layer(layer)
# print(df.head())
# df.head().to_csv("addresses.csv")