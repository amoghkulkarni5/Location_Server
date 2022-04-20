from flask import Blueprint, render_template, request, url_for
from typing import List
import aiohttp

# ========================================= HELPER CLASSES ==========================================================
from werkzeug.utils import redirect


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

    def get_location_servers_for_ui(self):
        return self.location_servers

    def get_data_servers_for_ui(self):
        return self.available_data_servers

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
    data_servers = ls.get_data_servers_for_ui()
    location_servers = ls.get_location_servers_for_ui()
    return render_template("index.html", data_servers=data_servers, location_servers=location_servers)


@main.route('/add-remove-servers')
def add_remove_servers():
    return render_template('add_remove_servers.html')


# Adds location server to list of location servers to be checked
@main.route('/add-location-server', methods=['POST'])
def add_location_server():
    ip = request.form.get('ip')
    ls.add_location_server(ip)
    return redirect(url_for('main.index'))


# Removes location server from list of location servers to be checked
@main.route('/remove-location-server')
def remove_location_server():
    location_server = " IP ADDRESS "
    ls.remove_location_server(location_server)
    return f"Removed: Location server {location_server}"


# Displays the form for UI actions.
@main.route('/read-write-form')
def read_write_form():
    return render_template('read_write_form.html')


# Adds new data server to list of data servers
@main.route('/add-data-server', methods=['POST'])
def add_data_server():
    ip = request.form.get('ip')
    ls.add_data_server(ip)
    return redirect(url_for('main.index'))


# Removes data server from list -- how to handle?
@main.route('/remove-data-server')
def remove_data_server():
    data_server = " IP ADDRESS "
    ls.remove_data_server(data_server)
    return f"Removed: Data server {data_server}"


# Fetches the appropriate data server for given key
@main.route('/read-from-ui', methods=['POST'])
def read_from_ui():
    key = request.form.get('read-key')
    # data_server = ls.get_data_server(key)
    data_server = key
    value = key  # To be replaced with HTTP call to data server
    return render_template('read_write_result_ui.html', data_server=data_server, value=value, msg='Value Read Successfully')


# Adds new data server to list of data servers
@main.route('/write-from-ui', methods=['POST'])
def write_from_ui():
    key = request.form.get('write-key')
    value = request.form.get('write-value')
    # data_server = ls.get_data_server(key)
    data_server = key
    return render_template('read_write_result_ui.html', data_server=data_server, value=value, msg='Value Successfully Written')


# Adds new data server to list of data servers
@main.route('/get-data-server', methods=['POST'])
def get_data_server():
    key = request.form.get('get-data-server-key')
    # data_server = ls.get_data_server(key)
    data_server = key
    return render_template('read_write_result_ui.html', data_server=data_server, value=None, msg='Got Data Server')

