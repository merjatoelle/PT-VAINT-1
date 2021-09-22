# -*- coding: utf-8 -*-
"""
Autors of project: Evgenii Churiulin, Merja Tölle, Center for Enviromental 
                                                   System Research (CESR) 

The Etopo background was downloaded from https://www.ngdc.noaa.gov/mgg/global/global.html
Cite ETOPO1: doi:10.7289/V5C8276M


Current Code Owner: CESR, Evgenii Churiulin
phone:  +49  561 804-6142
fax:    +49  561 804-6116
email:  evgenychur@uni-kassel.de
History:
Version    Date       Name
---------- ---------- ----                                                   
    1.1    2021-06-18 Evgenii Churiulin, Center for Enviromental System Research (CESR)
           Initial release
           
           
           
"""

import harmonica as hm

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt

import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy


def main():
    # Create a Stamen terrain background instance.
    stamen_terrain = cimgt.Stamen('terrain-background')

    fig = plt.figure(figsize = (14,10))

    # Create a GeoAxes in the tile's projection.
    ax = fig.add_subplot(1, 1, 1, projection=stamen_terrain.crs)

    # Limit the extent of the map to a small longitude/latitude range.
    ax.set_extent([5, 16, 47, 56], crs=ccrs.Geodetic())
  

    img = plt.imread('C:/Users/Churiulin/Desktop/My presentation/Articles/Orog/etopo.png')
    img_extent = (-180, 180, -90, 90)
    ax.imshow(img, origin='upper', extent=img_extent, transform=ccrs.PlateCarree())

    # Add boaders
    ax.add_feature(cfeature.COASTLINE, linestyle = ':', color = 'k', linewidth = 0.8 )
    ax.add_feature(cfeature.BORDERS  , linestyle = ':', color = 'k', linewidth = 1.0 )
    
    # Add hydrology
    ax.add_feature(cfeature.LAKES , alpha = 0.5)
    ax.add_feature(cfeature.RIVERS, alpha = 0.5, linestyle = '-', color = 'b', linewidth = 0.3)
    ax.add_feature(cfeature.OCEAN , alpha = 0.5)
    
    # Add the Stamen data at zoom level 10. Level of detalization
    ax.add_image(stamen_terrain, 10)


    # Add a marker for the Park station.
    ax.plot(6.45, 50.82, marker = 'o', color = 'red', markersize = 12,
            alpha = 1.0, transform = ccrs.Geodetic())

    ax.plot(6.44, 50.87, marker = 'o', color = 'darkred', markersize = 8,
            alpha = 0.7, transform = ccrs.Geodetic())
    
    ax.plot(6.30, 50.62, marker = 'o', color = 'darkred', markersize = 8,
            alpha = 0.7, transform = ccrs.Geodetic())
        
    # Add a marker for the Linden station.    
    ax.plot(8.41, 50.32, marker = 'o', color = 'green', markersize = 12,
            alpha = 1.0, transform = ccrs.Geodetic())

    # Add a marker for the Lindenberg station.
    ax.plot(14.11, 52.50, marker = 'o', color = 'blue', markersize = 12,
            alpha = 0.7, transform = ccrs.Geodetic())    
    

    # Add COSMO domains

    ax.plot(6.35, 50.7, marker = 's', color='lightcoral', markersize = 46,
            alpha = 0.3, transform = ccrs.Geodetic())
    
    ax.plot(8.41, 50.32, marker = 's', color = 'limegreen', markersize = 36,
            alpha = 0.3, transform = ccrs.Geodetic())    

    ax.plot(14.11, 52.50, marker = 's', color = 'cyan', markersize = 36,
            alpha = 0.3, transform = ccrs.Geodetic())  
    
    
    
    # Use the cartopy interface to create a matplotlib transform object
    # for the Geodetic coordinate system. We will use this along with
    # matplotlib's offset_copy function to define a coordinate system which
    # translates the text by 25 pixels to the left.
    geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)
    text_transform = offset_copy(geodetic_transform, units = 'dots', x = -25)

    # Add text 25 pixels to the left of the volcano.
    ax.text(7.1, 51.05, 'I',
            verticalalignment = 'center', horizontalalignment = 'right',
            transform = text_transform,
            bbox = dict(facecolor = 'sandybrown', alpha=0.5, boxstyle = 'round'))
    
    # Add text 25 pixels to the left of the volcano.
    ax.text(9.0, 50.55, 'II',
            verticalalignment = 'center', horizontalalignment = 'right',
            transform = text_transform,
            bbox = dict(facecolor = 'sandybrown', alpha=0.5, boxstyle = 'round'))
    
    # Add text 25 pixels to the left of the volcano.
    ax.text(14.8, 52.75, 'III',
            verticalalignment = 'center', horizontalalignment = 'right',
            transform = text_transform,
            bbox = dict(facecolor = 'sandybrown', alpha=0.5, boxstyle = 'round'))
 
    
    #ax.text(10.0, 53.0, 'Germany', fontsize = 14,
    #        verticalalignment = 'center', horizontalalignment = 'right',
    #        transform = text_transform,
    #        bbox = dict(facecolor = 'White', alpha = 0.01, boxstyle = 'round'))
     
    
    
    # Add legend
   
    colors = ['darkred', 'green', 'blue', 'lightcoral', 'limegreen', 'cyan']
    texts  = ["EURONET sites", "Linden site"  , "Lindenberg site"  , 
              "Park domain"  , "Linden domain", "Lindenberg domain"]

    # a list of marker shapes
    markers = ["o", "o", "o", "s", "s", "s"]

    patches = [plt.plot([],[], marker=markers[i], ms = 10, ls = "", mec = None, color = colors[i], 
                        label="{:s}".format(texts[i]) )[0]  for i in range(len(texts)) ]
    
    plt.legend(handles = patches, bbox_to_anchor=(1.01, -0.009), 
                   loc = 'lower right', ncol = 2, facecolor="white", numpoints=1 )   
    
 
    
    
    plt.savefig('C:/Users/Churiulin/Desktop/My presentation/Articles/Orog/' + '1' + '.png', format = 'png', dpi = 300) 
    plt.show()

if __name__ == '__main__':
    main()
    

 



