import requests
import re
import zipfile
import os
import shutil

USER = "minecraft"

minecraft_server_request = {
    "url": "https://minecraft.net/en-us/download/server/bedrock/",
    "headers": {
        "Accept-Encoding": "identity",
        "Accept-Language": "en",
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; BEDROCK-UPDATER)"
    },
    "allow_redirects": True
}

if os.path.isdir( "./MinecraftServer" ):
    print( "Cleaning Previous MinecraftServer Instance" )
    shutil.rmtree( "./MinecraftServer", ignore_errors=True )

try:
    r = requests.get( **minecraft_server_request )
except Exception:
    Exception( "Unable to connect to Minecraft.net" )

mc_re = re.search( "https://minecraft.azureedge.net/bin-linux/[\w]*-[\w]*-[\d\.]*zip", str(r.content) )
if not isinstance( mc_re, type( None ) ):
    url_mc = mc_re.group(0)
else:
    Exception( "Unable to retreive Minecraft Server Url" )

try:
    print( f"Downloading Minecraft Server from: {url_mc}" )
    r = requests.get( url_mc )
    with open( "MinecraftServer.zip", "wb" ) as pFile:
        print( f"Saving Minecraft Server" )
        pFile.write( r.content )
except Exception:
    Exception( "Unable to Download Minecraft Server" )

try:
    print( "Extracting MinecraftServer.zip" )
    with zipfile.PyZipFile( "MinecraftServer.zip", "r" ) as zFile:
        zFile.extractall( "./MinecraftServer" )
except Exception:
    Exception( "Unable to Extract MinecraftServer.zip" )

if os.path.exists( "./MinecraftServer.zip" ):
    print( "Deleting MinecraftServer.zip" )
    os.remove( "./MinecraftServer.zip" )


MC_PATH = os.path.abspath( "./MinecraftServer" ).replace( "\\", "/" )
try:
    print( "Writing Server Properties" )
    with open( "./MinecraftServer/server.properties", "w" ) as oFile:
        with open( "./config/base.server.properties", "r" ) as pFile:
            oFile.write( pFile.read() )

    print( "Writing Start Script" )
    with open( "./MinecraftServer/start_server.sh", "w" ) as oFile:
        with open( "./config/start_server.sh", "r" ) as pFile:
            oFile.write( pFile.read().replace( "{0}", MC_PATH ) )

    print( "Writing Stop Script" )
    with open( "./MinecraftServer/stop_server.sh", "w" ) as oFile:
        with open( "./config/stop_server.sh", "r" ) as pFile:
            oFile.write( pFile.read() )

    print( "Writing Service Script" )
    with open( "./MinecraftServer/MCServer.service", "w" ) as oFile:
        with open( "./config/MCServer.service", "r" ) as pFile:
            oFile.write( pFile.read().format( MC_PATH, USER ) )

except Exception:
    Exception( "Unable to write basic server config" )
