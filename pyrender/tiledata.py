#!/usr/bin/python
#----------------------------------------------------------------------------
# Download OSM data covering the area of a slippy-map tile 
#
# Features:
#  * Cached (all downloads stored in cache/z/x/y/data.osm)
#----------------------------------------------------------------------------
# Copyright 2008, Oliver White
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#---------------------------------------------------------------------------
from tilenames import *
from urllib import *
import os
from OsmMerge import OsmMerge

def DownloadLevel():
  """All primary downloads are done at a particular zoom level"""
  return(15)

def GetOsmTileData(z,x,y):
  """Download OSM data for the region covering a slippy-map tile"""
  if(x < 0 or y < 0 or z < 0 or z > 25):
    print "Disallowed %d,%d at %d" % (x,y,z)
    return
  
  directory = 'cache/%d/%d/%d' % (z,x,y)
  filename = '%s/data.osm' % (directory)
  #filename = 'linkoping.osm'
  if(not os.path.exists(directory)):
    os.makedirs(directory)

  (S,W,N,E) = tileEdges(x,y,z)

  if(z < 4):
    return
  # changed: fixed the merge-thing
  elif(z == DownloadLevel()):
  #elif (1):
    # Download the data
    #URL = 'http://dev.openstreetmap.org/~ojw/api/?/map/%d/%d/%d' % (z,x,y)
    URL = 'http://%s/api/0.6/map?bbox=%f,%f,%f,%f' % ('api.openstreetmap.org',W,S,E,N)
     
    if(not os.path.exists(filename)): # TODO: allow expiry of old data
      print "Downloading %d/%d/%d from network" % (z,x,y)
      urlretrieve(URL, filename)
    return(filename)
    
  elif(z > DownloadLevel()):
    # tbh, this shouldn't work.
    # TODO: chekkit?
    # use larger tile
    while(z > DownloadLevel()):
      z = z - 1
      x = int(x / 2)
      y = int(y / 2)
    return(GetOsmTileData(z,x,y))

  elif(z < DownloadLevel()):
    # merge smaller tiles
    if not os.path.exists(filename):
      filenames = []
      for i in (0,1):
        for j in (0,1):
          lx = x * 2 + i
          ly = y * 2 + j
          lz = z + 1
          #print "Downloading subtile %d,%d at %d" % (x,y,z)
          # download (or otherwise obtain) each subtile
          filenames.append(GetOsmTileData(lz,lx,ly))
      # merge them together
      OsmMerge(filename, z, filenames)
      print "Merge done (z=%s, filename=%s)" % (z, filename)
      return(filename)
    else:
      return filename
    
  #print "Below download level"
  #return(None)

if(__name__ == "__main__"):
  """test mode"""
  print GetOsmTileData(15, 16218, 10741)
