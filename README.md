# mx-lidar

Scripts to simplify the process of downloading Mexico's LIDAR-based DEM data.

The INEGI data portal [lists "continental relief" files](http://en.www.inegi.org.mx/temas/mapas/relieve/continental/). Each image is rather tiny (similar to how the [UK data is distributed](https://github.com/iandees/uk-lidar)) so this repo is designed to make it easier to download, convert, and merge these data into larger, more manageable GeoTIFFs.

## Listing files

The data portal website uses an endpoint that looks like this to populate the search results:

```
http://www.beta.inegi.org.mx/app/api/productos/interna_v1/slcCartas/obtenCartas?entidad=&municipio=&localidad=&tema=MAP0701000000&titgen=&escala=1%3A10+000&edicion=&formato=&buscar=&adv=false&rango=&tipoB=2&orden=4&pagina=1&tamano=100&ordenDesc=true
```

The `list_urls.py` script uses this URL to download and list the URLs for the data, including only the URL for the terrain model in "BIL" format. The output is written to stdout, so run it like so:

```
python list_urls.py > mx-lidar.txt
```

## Downloading files

Once the URLs are listed with the script from above, pipe them through `xargs` to `curl` and download them quickly:

```
cat mx-lidar.txt | \
xargs \
  -I {} \
  -P 24 \
  -n 1 \
  sh -c 'export f="{}"; curl -s -o /mnt/mxlidar/$(basename $f) $f'
```

## Fixing broken zipfiles

An unknown number of the zipfiles you just downloaded have an invalid structure. Normal zipfiles specify directory structure with `/`, but these broken zipfiles use `\`. The `unzip` command and `gdal` expect there to be subdirectories using `/`, so we'll run the `fix_zip_slashes.py` script across all the zipfiles you just downloaded to fix that:

```
find /mnt/mxlidar -name "*.zip" -print | \
xargs -I {} -P 24 -n 1 \
      python fix_zip_slashes.py {}
```

## Converting to GeoTIFF

The files you just downloaded are in the `.bil` format. The data is more useful to us in GeoTIFF, so let's run `convert_bil_to_geotiff.sh` across all the fixed zipfiles you just made:

```
find /mnt/mxlidar -name "*_fixed.zip" -print | \
xargs -I {} -P 24 -n 1 \
      sh -c 'export f={}; ./convert_bil_to_geotiff.sh $f ${f/_fixed.zip/.tif}'
```

## Merging GeoTIFFs
