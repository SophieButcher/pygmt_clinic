# -*- coding: utf-8 -*-
"""
Probing data for PyGMT Python Clinic
"""
#%% Imports
import pygmt
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime
#%% Regional figure 
latmin = 2
latmax = 18
lonmin = 32
lonmax = 48

proj = "M12c"

fig = pygmt.Figure()
# First draw the solid colors
fig.coast(region=[lonmin,lonmax,latmin,latmax], projection=proj, land="lightgreen", water="lightblue", shorelines=True)  # Pass region to the first plot element
fig.show()

#%% Add national boundaries, map frame and scale

frame = "a2.0f1.0"

fig = pygmt.Figure()
# Set some plot configuration things
pygmt.config(FONT_ANNOT_PRIMARY="12p", FONT_TITLE='12p')
pygmt.config(FORMAT_GEO_MAP="ddd.x")#, MAP_FRAME_TYPE="plain")
# First draw the solid colors
fig.coast(region=[lonmin,lonmax,latmin,latmax], projection=proj, frame=frame, land="lightgreen", water="lightblue", shorelines=True, borders=1)  # Pass region to the first plot element


fig.show()    


#%% Add some interesting geological details


frame = "a2.0f1.0"

fig = pygmt.Figure()
# Set some plot configuration things
pygmt.config(FONT_ANNOT_PRIMARY="12p", FONT_TITLE='12p')
pygmt.config(FORMAT_GEO_MAP="ddd.x")#, MAP_FRAME_TYPE="plain")
# First draw the solid colors
fig.coast(region=[lonmin,lonmax,latmin,latmax], projection=proj, frame=frame, land="lightgreen", water="lightblue", shorelines=True, borders=1)  # Pass region to the first plot element

# Add Bird (2003) plate boundaries
bird_data = "./Data/bird_symbols.txt"
fig.plot(data=bird_data, pen='2p, black, -', projection=proj, region=[lonmin,lonmax,latmin,latmax])

#Add usgs earthquake data
eq_data = pd.read_csv('./Data/usgs_cat.csv')
fig.plot(x=eq_data.longitude, y=eq_data.latitude, style='c0.1c', pen='0.5p,black', fill='gray', projection=proj)

# Add GVP Holocene volcanoes
volc_data = pd.read_csv('./Data/GVP_Holocene.csv')
fig.plot(x=volc_data.lon, y=volc_data.lat, style='t0.3c', pen='0.5p,black', fill='red', projection=proj)


    
fig.show()
    

#%% Make earthquakes look nicer

frame = "a2.0f1.0"

#Augment the EQ data. If you want to plot by datetime feature, must convert dt
eq_data = pd.read_csv('./Data/usgs_cat.csv')
eq_data['datetime_numeric'] = mdates.date2num(eq_data['time'])

#Initiate figure
fig = pygmt.Figure()

# Set some plot configuration things
pygmt.config(FONT_ANNOT_PRIMARY="12p", FONT_TITLE='12p')
pygmt.config(FORMAT_GEO_MAP="ddd.x")#, MAP_FRAME_TYPE="plain")

# First draw the solid colors
fig.coast(region=[lonmin,lonmax,latmin,latmax], projection=proj, frame=frame, land="lightgreen", water="lightblue", shorelines=True, borders=1)  # Pass region to the first plot element

# Add Bird (2003) plate boundaries
bird_data = "./Data/bird_symbols.txt"
fig.plot(data=bird_data, pen='2p, black, -', projection=proj, region=[lonmin,lonmax,latmin,latmax])


pygmt.makecpt(cmap="viridis", series=[eq_data['datetime_numeric'].min(), eq_data['datetime_numeric'].max(), "1d"])
#fig.plot(x=eq_data.longitude, y=eq_data.latitude, style='cc', size=0.01*(2**eq_data.mag), pen='0.5p,black', cmap=True, color=eq_data.time, projection=proj)
fig.plot(x=eq_data.longitude, y=eq_data.latitude, style='cc', size=0.01*(2**eq_data.mag), pen='0.5p,black', cmap=True, fill=eq_data['datetime_numeric'], projection=proj)
     
fig.show()



#%% Add legend, scale, colorbar, title
titlestr = "USGS Earthquake Catalogue, 1990-2024"
title = "+t\""+titlestr+"\""

frame = "a2.0f1.0"

#Initiate figure
fig = pygmt.Figure()

# Set some plot configuration things
pygmt.config(FONT_ANNOT_PRIMARY="12p", FONT_TITLE='12p')
pygmt.config(FORMAT_GEO_MAP="ddd.x")#, MAP_FRAME_TYPE="plain")


# First draw the solid colors
fig.coast(region=[lonmin,lonmax,latmin,latmax], projection=proj, frame=frame, land="lightgreen", water="lightblue", shorelines=True, borders=1)  # Pass region to the first plot element

# Add Bird (2003) plate boundaries
bird_data = "./Data/bird_symbols.txt"
fig.plot(data=bird_data, pen='2p, black, -', projection=proj, region=[lonmin,lonmax,latmin,latmax])


pygmt.makecpt(cmap="viridis", series=[eq_data['datetime_numeric'].min(), eq_data['datetime_numeric'].max(), "1d"])
#fig.plot(x=eq_data.longitude, y=eq_data.latitude, style='cc', size=0.01*(2**eq_data.mag), pen='0.5p,black', cmap=True, color=eq_data.time, projection=proj)
fig.plot(x=eq_data.longitude, y=eq_data.latitude, style='cc', size=0.01*(2**eq_data.mag), pen='0.5p,black', cmap=True, fill=eq_data['datetime_numeric'], projection=proj)


# Set basemap
fig.basemap(region=[lonmin,lonmax,latmin,latmax], projection=proj, frame=[frame, title], map_scale='6.0/-3.0c+w500k+f+u')

#Add colorbar for dates
tick_locations = [eq_data['datetime_numeric'].min(), 
                 (eq_data['datetime_numeric'].max() + eq_data['datetime_numeric'].min()) / 2, 
                 eq_data['datetime_numeric'].max()]

# Convert ticks to datetime strings
tick_labels = [mdates.num2date(tick).strftime('%b %Y') for tick in tick_locations]

# Add a colorbar below the plot, format it as datetime
# fig.colorbar(
#     frame=["a365000000"+"f3650"+"x+l1990               2000               2010               2020"],
#     position="JBC+w10c/0.5c+h",  # Position: centered below map, horizontal colorbar, 10 cm wide
#     scale=1,
# )


fig.colorbar(frame="af",position="JBC+w10c/0.5c+h", scale=1)     

fig.show()


#%% Add topog

titlestr = "1 arc second topography"
title = "+t\""+titlestr+"\""

frame = "a2.0f1.0"

#Initiate figure
fig = pygmt.Figure()

# Set some plot configuration things
pygmt.config(FONT_ANNOT_PRIMARY="12p", FONT_TITLE='12p')
pygmt.config(FORMAT_GEO_MAP="ddd.x")#, MAP_FRAME_TYPE="plain")


grid = pygmt.datasets.load_earth_relief(resolution ="03m", region=[lonmin,lonmax,latmin,latmax])
#test = fig.grdcontour(grid=grid, annotation=10, levels=5)
dgrid = pygmt.grdgradient(grid=grid, radiance=[270, 30])
cmap3 = pygmt.makecpt(cmap="grayC", series=[-1.5,1.5,0.1])
fig.grdimage(grid=dgrid, projection=proj, cmap=cmap3)


grid = pygmt.datasets.load_earth_relief(resolution ="03m", region=[lonmin,lonmax,latmin,latmax])
cmap2 = pygmt.makecpt(cmap="earth", series=[float(grid.min()), float(grid.max()), 10])
fig.grdimage(grid=grid, projection=proj, cmap=cmap2, transparency=60)

#grid = pygmt.datasets.load_earth_relief(resolution ="01s", region=[lonmin,lonmax,latmin,latmax])
#test = fig.grdcontour(grid=grid, levels=50, annotation=200, region=[lonmin,lonmax,latmin,latmax], projection='M20c')

# First draw the coast lines
fig.coast(region=[lonmin,lonmax,latmin,latmax], projection=proj, frame=frame, shorelines=True, borders=1)  # Pass region to the first plot element


fig.colorbar( frame=["x+lElev[m]"],position="JBC+w10c/0.5c+h",scale=1)

# Set basemap
fig.basemap(region=[lonmin,lonmax,latmin,latmax], projection=proj, frame=[frame, title], map_scale='6.0/-3.0c+w500k+f+u')

fig.show()
#%% writing the spec file as you go 





titlestr = "USGS Earthquake Catalogue, 1990-2024"
title = "+t\""+titlestr+"\""

frame = "a2.0f1.0"
scale = 0.01
mag_scale = [3, 4, 5, 6, 7]
ncols = len(mag_scale)

legend_fname = './legend_v2.txt'
lfile = open(legend_fname, 'w')
lfile.write('N '+str(ncols)+'\n')
for mag in mag_scale:
    label = 'M'+str(float(mag))
    size = str(scale*(2**mag))+'c'
    lfile.write('S 0.0c c '+size+' black 0.5p 0.5c '+label+'\n')
lfile.close()
    

#Initiate figure
fig = pygmt.Figure()

# Set some plot configuration things
pygmt.config(FONT_ANNOT_PRIMARY="12p", FONT_TITLE='12p')
pygmt.config(FORMAT_GEO_MAP="ddd.x")#, MAP_FRAME_TYPE="plain")


# First draw the solid colors
fig.coast(region=[lonmin,lonmax,latmin,latmax], projection=proj, frame=frame, land="gray", water="white", shorelines=True, borders=1)  # Pass region to the first plot element

# Add Bird (2003) plate boundaries
bird_data = "./Data/bird_symbols.txt"
fig.plot(data=bird_data, pen='2p, black, -', projection=proj, region=[lonmin,lonmax,latmin,latmax])


pygmt.makecpt(cmap="viridis", series=[eq_data['datetime_numeric'].min(), eq_data['datetime_numeric'].max(), "1d"])
#fig.plot(x=eq_data.longitude, y=eq_data.latitude, style='cc', size=0.01*(2**eq_data.mag), pen='0.5p,black', cmap=True, color=eq_data.time, projection=proj)
fig.plot(x=eq_data.longitude, y=eq_data.latitude, style='cc', size=scale*(2**eq_data.mag), pen='0.5p,black', cmap=True, fill=eq_data['datetime_numeric'], projection=proj)


# Set basemap
fig.basemap(region=[lonmin,lonmax,latmin,latmax], projection=proj, frame=[frame, title], map_scale='6.0/-3.5c+w500k+f+u')

#Add colorbar for dates
tick_locations = [eq_data['datetime_numeric'].min(), 
                 (eq_data['datetime_numeric'].max() + eq_data['datetime_numeric'].min()) / 2, 
                 eq_data['datetime_numeric'].max()]

# Convert ticks to datetime strings
tick_labels = [mdates.num2date(tick).strftime('%b %Y') for tick in tick_locations]

# Add a colorbar below the plot, format it as datetime
# fig.colorbar(
#     frame=["a365000000"+"f3650"+"x+l1990               2000               2010               2020"],
#     position="JBC+w10c/0.5c+h",  # Position: centered below map, horizontal colorbar, 10 cm wide
#     scale=1,
# )


fig.colorbar(frame="af",position="JBC+w10c/0.5c+h", scale=1)     



fig.legend(spec='legend.txt', position='0.0c/-3.0c+w12c')
# Show the figure
fig.show()


#%% build 3d plot/space

# play around with angle, vis
# Add seismic location points
# color them in clusters
# add topog

# Corbetti only now, zoom in
latmin = 6.9
latmax = 7.55
lonmin = 38.2
lonmax = 38.7
proj = "M12c"
elevmin = -5000
elevmax = 5000
perspective=[260,30]
fig = pygmt.Figure()

pygmt.config(FONT_ANNOT_PRIMARY="12p", FONT_TITLE='12p')
pygmt.config(FORMAT_GEO_MAP="ddd.x", MAP_FRAME_TYPE="plain")

grid = pygmt.datasets.load_earth_relief(resolution ="03s", region=[lonmin,lonmax,latmin,latmax])
cmap2 = pygmt.makecpt(cmap="earth", series=[float(grid.min()), float(grid.max()), 10])
cutgrd = pygmt.grdcut(grid=grid, region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax])

fig.grdview(
    grid=cutgrd,
    perspective=perspective,
    frame=["xa", "yaf", "za1000f500", "WSne"],
    projection=proj,
    zscale="0.001c",
    # Set the surftype to "surface"
    surftype="s",
    shading="+a45",
    # Set the CPT to "geo"
    cmap="earth",
    region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax],
    transparency=50
)

fig.show()

#%% chunk to check max extent of data
eq_data = pd.read_csv('./Data/Corbetti/Corbetti_catalog.txt', sep='\t')
print((eq_data.Depth*-1000).min())
print(cutgrd.max())



#%% go back and work out what view angle is best once data is in

elevmin = -23000
elevmax = 3000



fig = pygmt.Figure()

pygmt.config(FONT_ANNOT_PRIMARY="12p", FONT_TITLE='12p')
pygmt.config(FORMAT_GEO_MAP="ddd.x", MAP_FRAME_TYPE="plain")

#grid = pygmt.datasets.load_earth_relief(resolution ="03s", region=[lonmin,lonmax,latmin,latmax])
#cmap2 = pygmt.makecpt(cmap="earth", series=[float(grid.min()), float(grid.max()), 10])
#cutgrd = pygmt.grdcut(grid=grid, region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax])

# fig.grdview(
#     grid=cutgrd,
#     perspective=perspective,
#     frame=["xa", "yaf", "za1000f500", "WSne"],
#     projection=proj,
#     zscale="0.001c",
#     # Set the surftype to "surface"
#     surftype="s",
#     shading="+a45",
#     # Set the CPT to "geo"
#     cmap="earth",
#     region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax],
#     transparency=50
# )

# Plot hypocenters
fig.plot3d(x=eq_data.Longitude,
           y=eq_data.Latitude,
           z=eq_data.Depth*-1000,
           style="uc",
           size=0.02*(2**eq_data.Magnitude),
           fill="red",
           zscale="0.0005c",
           perspective=perspective,
           projection=proj,
           frame=["xa", "yaf", "za5000f1000", "WSneZ"],
           region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax]
           )

fig.show()


#%%
# Merge 'YearMonthDay' and 'HrMinSec' columns into a single string column, add space between
eq_data['datetime_str'] = eq_data['YearMonthDay'].astype(str) + ' ' + eq_data['HrMinSec'].astype(str)

# Convert the merged 'datetime_str' column to a pandas datetime object
eq_data['datetime'] = pd.to_datetime(eq_data['datetime_str'], format='%Y%m%d %H:%M:%S')

# Convert the datetime column to a float using mdates
eq_data['datetime_numeric'] =  mdates.date2num(eq_data['datetime'])

perspective=[260,15]

fig = pygmt.Figure()

pygmt.config(FONT_ANNOT_PRIMARY="12p", FONT_TITLE='12p')
pygmt.config(FORMAT_GEO_MAP="ddd.x", MAP_FRAME_TYPE="plain")

grid = pygmt.datasets.load_earth_relief(resolution ="03s", region=[lonmin,lonmax,latmin,latmax])
cmap2 = pygmt.makecpt(cmap="gray", series=[float(grid.min()), float(grid.max()), 10])
cutgrd = pygmt.grdcut(grid=grid, region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax])

fig.grdview(
    grid=cutgrd,
    perspective=perspective,
    frame=["xa", "yaf", "za1000f500", "WSne"],
    projection=proj,
    zscale="0.0005c",
    # Set the surftype to "surface"
    surftype="s",
    shading="+a45",
    # Set the CPT to "geo"
    cmap="gray",
    region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax],
    transparency=80
)

cmap1 = pygmt.makecpt(cmap="viridis", series=[eq_data['datetime_numeric'].min(), eq_data['datetime_numeric'].max(), "1d"])


# Plot hypocenters
fig.plot3d(x=eq_data.Longitude,
           y=eq_data.Latitude,
           z=eq_data.Depth*-1000,
           style="uc",
           size=0.02*(2**eq_data.Magnitude),
           fill=eq_data['datetime_numeric'],
           cmap=True,
           zscale="0.0005c",
           perspective=perspective,
           projection=proj,
           frame=["xa", "yaf", "za5000f1000", "WsNeZ"],
           region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax]
           )

fig.show()

#%% add station data


fig = pygmt.Figure()

pygmt.config(FONT_ANNOT_PRIMARY="12p", FONT_TITLE='12p')
pygmt.config(FORMAT_GEO_MAP="ddd.x", MAP_FRAME_TYPE="plain")

station_data = pd.read_csv('./Data/Corbetti/station_locs.csv')
station_data_latlon = station_data[['Longitude', 'Latitude']]
track = pygmt.grdtrack(points=station_data_latlon, grid=cutgrd, newcolname="elevation")
track['Name'] = station_data['Station Code']

grid = pygmt.datasets.load_earth_relief(resolution ="03s", region=[lonmin,lonmax,latmin,latmax])
cmap2 = pygmt.makecpt(cmap="gray", series=[float(grid.min()), float(grid.max()), 10])
cutgrd = pygmt.grdcut(grid=grid, region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax])

fig.grdview(
    grid=cutgrd,
    perspective=perspective,
    frame=["xa", "yaf", "za5000f1000", "WsNeZ"],
    projection=proj,
    zscale="0.0005c",
    # Set the surftype to "surface"
    surftype="s",
    shading="+a45",
    # Set the CPT to "geo"
    cmap="gray",
    region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax],
    transparency=80
)

cmap1 = pygmt.makecpt(cmap="viridis", series=[eq_data['datetime_numeric'].min(), eq_data['datetime_numeric'].max(), "1d"])


# Plot hypocenters
fig.plot3d(x=eq_data.Longitude,
           y=eq_data.Latitude,
           z=eq_data.Depth*-1000,
           style="uc",
           size=0.02*(2**eq_data.Magnitude),
           fill=eq_data['datetime_numeric'],
           cmap=True,
           zscale="0.0005c",
           perspective=perspective,
           projection=proj,
           frame=["xa", "yaf", "za5000f1000", "WsNeZ"],
           region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax]
           )

fig.colorbar(frame="a100000f90",position="JBC+w10c/0.5c+h", scale=1)   

# Plot seismic stations
fig.plot3d(x=track.Longitude,
           y=track.Latitude,
           z=track.elevation,
           style="c0.2c",
           fill='black',
           zscale="0.0005c",
           perspective=perspective,
           projection=proj,
           frame=["xa", "yaf", "za5000f1000", "WsNeZ"],
           region=[lonmin,lonmax,latmin,latmax,elevmin,elevmax]
           )


fig.show()



#%% zoomed in section using subplots and cross sections
import numpy as np#


elevmin = -10000
elevmax = 3000
lonmin = 38.3
lonmax = 38.5
latmin = 7.1
latmax = 7.3
proj="M20c"


fig = pygmt.Figure()

pygmt.config(FONT_ANNOT_PRIMARY="16p", FONT_TITLE='16p')
pygmt.config(FORMAT_GEO_MAP="ddd.x", MAP_FRAME_TYPE="plain")

grid = pygmt.datasets.load_earth_relief(resolution ="01s", region=[lonmin,lonmax,latmin,latmax])
dgrid = pygmt.grdgradient(grid=grid, radiance=[270, 30])
cmap3 = pygmt.makecpt(cmap="grayC", series=[-1.5,1.5,0.1])


# Define the xprofile
a_lat = 7.205
a_lon = 38.3
A_lat = 7.19
A_lon = 38.5

a = (a_lat, a_lon)
A = (A_lat, A_lon)

num_points = 100

# Linearly interpolate latitudes and longitudes
lats = np.linspace(a[0], A[0], num_points)
lons = np.linspace(a[1], A[1], num_points)

# Combine into a DataFrame
df_coords = pd.DataFrame({
    "lon": lons,
    "lat": lats
})

# Show the DataFrame with 100 points
#print(df_coords)

xprofile = pygmt.grdtrack(points=df_coords, grid=grid, newcolname='xelev')


# repeat for y

b_lat = 7.1
b_lon = 38.405
B_lat = 7.3
B_lon = 38.42

b = (b_lat, b_lon)
B = (B_lat, B_lon)

num_points = 100

# Linearly interpolate latitudes and longitudes
lats = np.linspace(b[0], B[0], num_points)
lons = np.linspace(b[1], B[1], num_points)

# Combine into a DataFrame
df_coords = pd.DataFrame({
    "lon": lons,
    "lat": lats
})

# Show the DataFrame with 100 points
#print(df_coords)

yprofile = pygmt.grdtrack(points=df_coords, grid=grid, newcolname='yelev')

############## pick up here mon


xframe = ["ya5000f1000+lDepth(m)", "xa0.05f0.01", "WSne"]
mainframe = "a0.05f0.01"
yframe = ["xa5000f1000+lDepth(m)", "ya0.05f0.01", "wSnE"]



fig.shift_origin(xshift="4c") 
with fig.subplot(nrows=1, ncols=1, figsize=("20c", "3c")):
    fig.basemap(region=[lonmin,lonmax,elevmin,elevmax], projection="X?", frame=xframe)
    fig.plot(x=[(B_lon+b_lon)/2., (B_lon+b_lon)/2.], y=[elevmin,elevmax], pen='1p,gray,dash', projection="X?")
    fig.plot(x=xprofile.lon, y=xprofile.xelev)
    pygmt.makecpt(cmap="viridis", series=[eq_data['datetime'].min(), eq_data['datetime'].max()])
    fig.plot(x=eq_data.Longitude, y=(eq_data.Depth)*-1000., style='cc', size=0.1*(2**eq_data.Magnitude), pen='0.5p,black', cmap=True, fill=eq_data['datetime'])
    fig.colorbar(frame="af",position="x0c/-1.8c+w11c/0.5c+h", scale=1, region=[lonmin,lonmax,elevmin,elevmax], projection='X?')   
    fig.legend(spec='legend.txt', position='12.0c/-2.2c+w12c')

fig.shift_origin(yshift="4c")    
with fig.subplot(nrows=1, ncols=1, figsize=("25c", "15c")):
    titlestr ="test"
    title = "+t\""+titlestr+"\""
    fig.basemap(region=[lonmin,lonmax,latmin,latmax], projection=proj, frame=[mainframe, title])
    pygmt.makecpt(cmap="grayC", series=[-1.5,1.5,0.1])
    fig.grdimage(grid=dgrid, projection=proj, frame =mainframe, cmap=True, transparency=40)
    fig.plot(x=[a_lon, A_lon], y=[a_lat, A_lat], pen='1p,black,dash', projection=proj)  
    fig.plot(x=[b_lon, B_lon], y=[b_lat, B_lat], pen='1p,black,dash', projection=proj)    
    pygmt.makecpt(cmap="viridis", series=[eq_data['datetime'].min(), eq_data['datetime'].max()])
    fig.plot(x=eq_data.Longitude, y=eq_data.Latitude, style='cc', size=0.1*(2**eq_data.Magnitude), pen='0.5p,black', cmap=True, fill=eq_data['datetime'], projection=proj)
    

fig.shift_origin(xshift="21c")
with fig.subplot(nrows=1, ncols=1, figsize=("3c", "20c")):
    fig.basemap(region=[-elevmax, -elevmin, latmin, latmax], projection="X?", frame=yframe)
    fig.plot(x=[-elevmax, -elevmin], y=[(A_lat+a_lat)/2., (A_lat+a_lat)/2.], pen='1p,gray,dash', projection="X?")
    fig.plot(x=-yprofile.yelev, y=yprofile.lat)
    pygmt.makecpt(cmap="viridis", series=[eq_data['datetime'].min(), eq_data['datetime'].max()])
    fig.plot(x=(eq_data.Depth)*1000, y=eq_data.Latitude, style='cc', size=0.1*(2**eq_data.Magnitude), pen='0.5p,black', cmap=True, fill=eq_data['datetime'])

#fig.savefig('/Volumes/sbutcher/OneDriveCopy/PostDublin/qualitycontrol/sample_plots/maps/nll_'+str(i)+'.png')
fig.show()

