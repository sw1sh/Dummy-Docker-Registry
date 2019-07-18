#!/usr/bin/env python

import argparse
import docker
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import time


parser = argparse.ArgumentParser()
parser.add_argument('--host', help='listening host', default='0.0.0.0')
parser.add_argument('--rhost', help='registry host', default='127.0.0.1')
parser.add_argument('--port', default=5000, type=int)
args = parser.parse_args()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        request_path = self.path
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        return_json = b'{}'
        print(request_path)
        if re.match('^/v2/$', request_path):
            self.send_header('Content-Length', '2')
            self.send_header('Content-Type', 'application/json; charset=utf-8')
        else:
            image_request = re.match('^/v2/(.+)/manifests/(.+)$', request_path)
            if image_request:
                name, tag = image_request.groups()
                print(f"Spoofing image {name}:{tag}")
                image_names = [f"{name}:{tag}",
                               f"{args.rhost}/{name}:{tag}",
                               f"{args.rhost}:{args.port}/{name}:{tag}"]
                images = docker.from_env().images
                digest = ''
                for image_name in image_names:
                    print(f"Trying image {image_name}")
                    try:
                        digest = images.get(image_name).id
                        print(f"Found image {image_name} with digest: {digest}")
                        break
                    except:
                        pass
                return_json = bytes(json.dumps({'config': {'digest': digest}}), 'utf-8')
                self.send_header('Content-Length', f"{len(return_json)}")
                self.send_header('Content-Type', 'application/vnd.docker.distribution.manifest.v2+json')

        self.send_header('Docker-Distribution-Api-Version', 'registry/2.0')
        self.end_headers()
        self.wfile.write(return_json)

myServer = HTTPServer((args.host, args.port), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (args.host, args.port))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (args.host, args.port))
