from flask import Blueprint
from typing import List
import json
import aiohttp

# ========================================= HELPER CLASSES ==========================================================


async def fetch(session, url):
    async with session.get(url) as response:
        return await response


class Server:
    type: str
    ip_address: str

    def __init__(self, ip, type_of_server, capacity=0):
        self.ip_address = ip
        self.type = type_of_server
        self.capacity = capacity

    def get_ip(self):
        return self.ip_address

    def update_ip(self, ip: str):
        self.ip_address = ip


class LocationServer:
    location_servers = List[Server]
    available_data_servers = List[Server]

    def __init__(self, location_servers=None, data_servers=None):
        if data_servers is None:
            data_servers = []
        if location_servers is None:
            location_servers = []

        self.location_servers = location_servers
        self.available_data_servers = data_servers

    def get_display_data(self):
        return {
            "data_servers": json.dumps(self.available_data_servers),
            "location_server": json.dumps(self.location_servers)
        }

    def add_location_server(self, location_server_ip: str):
        """
        Adds a location server to the list of available location servers.
        Note: This location server will be a part of the distributed system.
        """
        self.location_servers.append(Server(location_server_ip, 'location_server'))
        return location_server_ip

    def remove_location_server(self, location_server_ip: str):
        return location_server_ip

    def add_data_server(self, data_server_ip: str):
        """
        Adds a data server to the list of available data servers.
        """
        self.available_data_servers.append(Server(data_server_ip, 'data_server'))
        return data_server_ip

    def remove_data_server(self, data_server_ip: str):
        return data_server_ip

    async def check_location_servers(self, key: str):
        """
        Asynchronously checks all location servers for whether the given key exists, if it does, it returns the IP data server.
        Else returns None.
        """

        # Send requests async to all location servers and obtain result set
        result = []
        urls = (server.get_ip() for server in self.location_servers)
        async with aiohttp.ClientSession() as session:
            for url in urls:
                result.append(await fetch(session, url))

        # Iterate over result set to get required value and send appropriate response
        for response in result:
            # Check response, return if key is found.
            print(response)

    def assign_data_server_for_key(self):
        """
        Traverses Trie in required order for data locality, and returns the data server.
        If above is not fulfilled, add a new data server to trie for this key and return it.
        If no data servers are available, return None.
        """

    async def get_data_server(self, key: str):
        """
        Obtain data server from trie, if it doesn't exist, check other location servers
        If not present anywhere, return None.
        """

        # Obtain from Trie

        # If not present, check other location servers whether it exists
        result = await self.check_location_servers(key)

        # If not there anywhere, return appropriate error message

        return self.available_data_servers[0].ip_address


# ======================================== ROUTES ==========================================================


main = Blueprint('main', __name__)
ls = LocationServer()


@main.route('/')
def index():
    return ls.get_display_data()


# Adds location server to list of location servers to be checked
@main.route('/add-location-server')
def add_location_server():
    location_server = " IP ADDRESS "
    ls.add_location_server(location_server)
    return f"Added: Location server {location_server}"


# Removes location server from list of location servers to be checked
@main.route('/remove-location-server')
def remove_location_server():
    location_server = " IP ADDRESS "
    ls.remove_location_server(location_server)
    return f"Removed: Location server {location_server}"


# Adds new data server to list of data servers
@main.route('/add-data-server')
def add_data_server():
    data_server = " IP ADDRESS "
    ls.get_data_server(data_server)
    return f"Added: Data server {data_server}"


# Removes data server from list -- how to handle?
@main.route('/remove-data-server')
def remove_data_server():
    data_server = " IP ADDRESS "
    ls.remove_data_server(data_server)
    return f"Removed: Data server {data_server}"


# Fetches the appropriate data server for given key
@main.route('/get-data-server')
def get_data_server():
    key = "keystring"
    data_server = ls.get_data_server(key)
    return f"Obtained data server: {data_server}"
