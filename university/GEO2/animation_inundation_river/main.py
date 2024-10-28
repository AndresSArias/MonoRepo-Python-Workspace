# Importing necessary libraries
import geopandas as gpd
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import imageio
from rasterio import features

# Function to generate hillshade
def hillshade(array, azimuth, angle_altitude):
    x, y = np.gradient(array)  # Gradient in x and y directions
    slope = np.pi / 2. - np.arctan(np.sqrt(x*x + y*y))  # Slope calculation
    aspect = np.arctan2(-x, y)  # Aspect calculation
    azimuthrad = azimuth * np.pi / 180.  # Convert azimuth to radians
    altituderad = angle_altitude * np.pi / 180.  # Convert altitude to radians
    
    # Calculate hillshade
    shaded = np.sin(altituderad) * np.sin(slope) + np.cos(altituderad) * np.cos(slope) * np.cos(azimuthrad - aspect)
    return 255 * (shaded + 1) / 2  # Normalize and scale the output

 # Light source from azimuth 315° and altitude 45°



def main(): 
    # Paths to the DEM and river shapefile
    dem_path = r"static\DEM.tif"
    river_path = r"static\rio.shp"


    # Reading DEM data (raster)
    with rasterio.open(dem_path) as src:
        dem_array = src.read(1)  # Reading the elevation values
        dem_meta = src.meta      # Metadata, including the affine transform

    # Reading the river shapefile (vector)
    river_gdf = gpd.read_file(river_path)

    # Verificar y re-proyectar si es necesario
    if river_gdf.crs != dem_meta['crs']:
        river_gdf = river_gdf.to_crs(dem_meta['crs'])  # Cambiar CRS del shapefile si no coincide


    # Generate the hillshade array
    hillshade_array = hillshade(dem_array, 315, 45) 


    # Calculate the average elevation of the river from the DEM
    river_elevations = []
    for geom in river_gdf.geometry:
        mask = features.geometry_mask([geom], transform=dem_meta['transform'], invert=True, out_shape=dem_array.shape)
        river_elevations.extend(dem_array[mask])  # Extract elevations under the river

    mean_river_elevation = np.mean(river_elevations)  # Mean river elevation

    # Generate frames for the flood animation
    intervals = np.arange(0, 2.2, 0.2)  # Flood increments
    frames = []

    for interval in intervals:
        flood_elevation = mean_river_elevation + interval  # Elevation threshold for flooding
        flood_mask = dem_array <= flood_elevation  # Mask for flooded areas
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Plot the hillshade
        ax.imshow(hillshade_array, cmap='gray', extent=[dem_meta['transform'][2], 
                                                    dem_meta['transform'][2] + dem_array.shape[1] * dem_meta['transform'][0],
                                                    dem_meta['transform'][5] + dem_array.shape[0] * dem_meta['transform'][4],
                                                    dem_meta['transform'][5]])
        
        # Overlay the flood mask
        ax.imshow(flood_mask, cmap='Blues', alpha=0.5, extent=[dem_meta['transform'][2], 
                                                            dem_meta['transform'][2] + dem_array.shape[1] * dem_meta['transform'][0],
                                                            dem_meta['transform'][5] + dem_array.shape[0] * dem_meta['transform'][4],
                                                            dem_meta['transform'][5]])
        
        # Plot the river shapefile
        river_gdf.plot(ax=ax, color='blue', edgecolor='blue')
        
        # Set title and remove axis labels
        ax.set_title(f"Inundación a {interval} m")
        plt.axis('off')
        
        # Convert the figure to an image
        fig.canvas.draw()
        image = np.array(fig.canvas.renderer._renderer)
        plt.close(fig)
        
        # Add the image to the frames
        frames.append(image)

    # Save the frames as an animated GIF

    gif_path = r"static\flood_animation.gif"
    imageio.mimsave(gif_path, frames, duration=0.5, loop=0)  # Save with a 0.5-second delay between frames

    print(f"Animación guardada en: {gif_path}")    
    
if __name__ == "__main__":
    print("Bienvenido al creador de inundación de un río")
    main()
    print("Creación exitosa")