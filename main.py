import folium
import overpy
#from shapely.geometry import Point
#import geopandas as gpd
from re import M

camping_icon = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Capa_1" x="0px" y="0px" viewBox="0 0 305.601 305.601" style="enable-background:new 0 0 305.601 305.601;" xml:space="preserve"> <g> <g> <g> <path style="fill:#010002;" d="M305.601,211.021l-9.213-1.534l-2.443,14.597C248.954,188.501,148.604,51.347,147.529,49.882     l-3.41-4.621l-2.951,4.895C114.692,94.228,40.292,209.536,11.138,219.306l-2.57-5.901L0,217.147l17.147,39.471l-0.596,0.85h0.977     l1.251,2.872l6.624-2.872h266.139l-0.967-1.212l7.259,1.212l4.445-26.487l0.459-0.85l-0.293-0.205L305.601,211.021z      M192.189,249.007h-85.401c-2.589-5.803-4.143-12.135-4.143-18.905c0-25.852,20.967-46.848,46.828-46.848     c25.891,0,46.848,20.977,46.848,46.848C196.322,236.853,194.778,243.214,192.189,249.007z M288.865,254.137L145.702,73.662     L23.448,247.649l-9.291-21.387C49.222,213.004,128.155,86.109,144.716,58.948c18.71,25.393,106.983,143.739,147.774,173.596     L288.865,254.137z"/> </g> </g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> <g> </g> </svg>'
api = overpy.Overpass()

query_result = api.query("""
        area[name="England"]->.boundaryarea;
        (
        nwr(area.boundaryarea)[tourism=camp_site];
        );
        out meta;
    """)
m = folium.Map(location=[53,0],
    zoom_start=8,
    tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
    #tiles='cartodbpositron',
    attr='Open Street Map Cyclosm'
    )

for site in query_result.nodes:
  html = (
        "<h3><center>" + str(site.tags.get('name')) + "</center></h3>" +
        "<p><Center>" + "<a href='https://www.openstreetmap.org/edit?editor=id&node=" +
        str(site.id) + "#map=16/" +
        str(float(site.lat)) + "/" +
        str(float(site.lon)) +"' target='_blank'>" +
        str(site.id) + "</a> - "+
        "<a href='https://www.google.com/maps/@" + str(site.lat) + "," +
        str(site.lon) + ",16z' target='_blank'> Google Maps </a></center></p>"
        )
  for key in site.tags.keys():
    if key == "website":
      html += ("<b><a href='"+ str(site.tags['website']) + "' target='_blank'>" +
      str(site.tags['website']) + "</a></b><br />")
    else:
      html += key + ": <b>" +str(site.tags[key]) + "</b><br />"

  iframe = folium.IFrame(html=html, width=300, height=300)
  m.add_child(
    folium.Marker(
    location= [float(site.lat), float(site.lon)],
    popup = folium.Popup(html=iframe),
    icon = folium.features.DivIcon(icon_size=(12,12), html=camping_icon)
      )
  )

m

