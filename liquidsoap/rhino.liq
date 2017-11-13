#!/usr/bin/liquidsoap
# Log dir
set("log.file.path","/tmp/basic-radio.log")

# Setup stream environment:
hostname = "localhost"
input_mountpoint = "/master.ogg"
mountpoint = "/stream.ogg"
filename = "%Y-%m-%d-%H-%M.ogg"
stream_uri = "http://" ^ hostname ^ mountpoint
file_uri = "http://" ^ hostname ^ filename

# Setup "on-air" and "off-air" webhooks:
webhook_hostname = "radiorhino.eu"
webhook_route = "/on-air-status"
webhook_uri = "https://" ^ webhook_hostname ^ webhook_route

# Check if ON_AIR_TOKEN environment variable is set and store it or set it to default
on_air_token = getenv("ON_AIR_TOKEN")

################
#  Inputs      #
################

def on_air ()
    resp = http.post(
        data="Token=" ^ on_air_token ^
            "&Stream=" ^ stream_uri ^
            "&Filename=" ^ file_uri ^
            "&State=ON_AIR",
        webhook_uri)
    print(resp)
end

def off_air ()
    resp = http.post(
        data="Token=" ^ on_air_token ^
            "&State=OFF_AIR")
    print(resp)
end

base = synth.all.sine()
source =
    input.http("http://" ^ hostname ^ input_mountpoint,
        on_connect={on_air}, on_disconnect={off_air})
radio = fallback([base, source])

#################
#  Outputs      #
#################

# Possible options and values are bitrate=64, samplerate=11025, ...
output.icecast(%vorbis,
    host=hostname,
    port=8000,
    mount="live.ogg",
    password="yolo",
    source)

print(filename)
print(on_air_token)

output.file(
    %vorbis,
    filename,
    on_start=on_air,
    on_stop=off_air,
    source)
