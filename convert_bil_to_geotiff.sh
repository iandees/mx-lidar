set -e

zfile=$1
ofile=$2

if [[ -z "$zfile" || -z "$ofile" ]]; then
  >&2 echo "usage: $(basename $0) <input zipfile name> <output geotiff name>"
  exit 1
fi

vrt_tmp=$(mktemp -d)

unzip -qq -d $vrt_tmp/unzipped $zfile

bil_file=$(find $vrt_tmp/unzipped -name "*.bil" -print | head -n 1)

gdalwarp -q -dstnodata -32768 $bil_file ${bil_file/bil/tif}

mv ${bil_file/bil/tif} $ofile

rm -rf $vrt_tmp
