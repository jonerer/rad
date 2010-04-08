# by teh jonerer and the elofferer.
# just grabs some images (like... linkoping) to populate the cache.

from tiledata import GetOsmTileData
from tilenames import tileXY

bbox = (58.258000000000003, 15.282, 58.539000000000001, 15.976000000000001)

z = 15
scalr = 1000.0
for lat in range(bbox[0]*scalr, bbox[2]*scalr):
  lat /= scalr
  for long in range(bbox[1]*scalr, bbox[3]*scalr):
    long /= scalr
    (x, y) = tileXY(lat, long, z)
    GetOsmTileData(z, x, y)
