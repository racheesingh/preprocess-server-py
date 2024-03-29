#!/usr/bin/python2

import re, pygeoip

def getServerNameAddr():
    patternName = r'LocalSite .*'
    patternURL = r'HttpProxy .*'
    list_domain_URLs = []
    list_domain_names = []
    while True:
        try:
            string = raw_input()
        except EOFError:
            break
        regexName = re.compile( patternName, re.DOTALL|re.IGNORECASE )
        regexURL = re.compile( patternURL, re.DOTALL|re.IGNORECASE )
        matchName = regexName.findall( string )
        matchURL = regexURL.findall( string )
        if matchName:
            for x in matchName:
                x = x.split()[-1][1:-1]
                list_domain_names.append( x )
        if matchURL:
            for x in matchURL:
                x = x.split()[-1][1:-1]
                list_domain_URLs.append( x )

    N = len( list_domain_names )    
    serverDict = {}
    # Make a dictionary from this information
    for i in range( N ):
        name = list_domain_names[ i ]
        
        # Getting all URLs from the URL string
        URLs = list_domain_URLs[ i ]
        pattern = r'http://.*?:'
        regex = re.compile( pattern, re.DOTALL|re.IGNORECASE )
        match = regex.findall( URLs )
        URLsFinal = []
        for x in match:
            URLsFinal.append( x[:-1] )

        serverDict[ name ] = URLsFinal

    return serverDict

def getServerLocations( serverDict ):
    gi = pygeoip.GeoIP( "/usr/local/share/GeoIP/GeoIPCity.dat",
                        pygeoip.STANDARD )
    import socket
    serverDictLocation = {}
    for name, urls in serverDict.iteritems():
        url = urls[0][7:]

        try:
            gir = gi.record_by_name( url )
        except socket.gaierror:
            pass
        
        if gir != None:
            serverDictLocation[ name ] = \
            { 'url': urls, 'latitude': gir[ 'latitude' ], 
              'longitude': gir[ 'longitude' ] }
        else:
            # NF = Not Found
            serverDictLocation[ name ] = \
            { 'url': urls, 'latitude': "NF", 'longitude': "NF" }

    return serverDictLocation

def main():

    # Parsing geolist.txt to get the names and addresses of all servers
    serverDict = getServerNameAddr()

    # Get locations of all servers
    serverDictLocation = getServerLocations( serverDict )

    #for name, url in serverDictLocation.iteritems():
    #    print name, url

if  __name__ == "__main__":
    main()
