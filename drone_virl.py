#! /usr/bin/env python
"""
Drone Plugin for managing network simulations with Cisco VIRL

Author: Hank Preston <hank.preston@gmail.com>
"""

__author__ = "Hank Preston"
__author_email__ = "hank.preston@gmail.com"
__copyright__ = "Copyright (c) 2016 Cisco Systems, Inc."
__license__ = "MIT"

from droneci import Plugin
from virlutils import *
from time import sleep

# Create new plugin object containing relevant details about the current build
drone_virl = Plugin(secrets = ["VIRL_USER", "VIRL_PASSWORD", "VIRL_HOST"])

# Print out Debug information if plugin parameter "debug" was set
if drone_virl.plugin["DEBUG"]:
    print("Debug Info:")
    print(drone_virl.ci)
    print(drone_virl.drone)
    print(drone_virl.plugin)
    print(drone_virl.secrets)
    print()
    print("Action: {}".format(drone_virl.plugin["ACTION"]))

# Create variables for VIRL server connection
simengine_host = drone_virl.secrets["VIRL_HOST"]
virl_user = drone_virl.secrets["VIRL_USER"]
virl_password = drone_virl.secrets["VIRL_PASSWORD"]


def create_sim():
    """
    Create a new simulation.
    """
    # If already running, destroy.
    destroy_sim()

    # VIRL file path - based on drone workspace and plugin filename
    virl_file = "{directory}/{filename}".format(directory = drone_virl.drone["WORKSPACE"], filename = drone_virl.plugin["VIRL_FILE"])
    virl_file = open(virl_file, "r")

    # Launch new simulation
    print("Launching New Simulation")
    print(launch_simulation(drone_virl.plugin["SIMULATION_NAME"], virl_file.read(), simengine_host, virl_user, virl_password))
    sleep(5)

    # Wait for nodes to be fully started (state = ACTIVE)
    while not test_node_state(drone_virl.plugin["SIMULATION_NAME"], "ACTIVE", simengine_host, virl_user, virl_password):
        print("  Nodes not started yet")
        sleep(10)
    print("")

    # Print Console Information for Nodes
    print("Retrieving Console Connection Details: ")
    nodes = get_nodes(drone_virl.plugin["SIMULATION_NAME"], simengine_host, virl_user, virl_password)
    for node in nodes.keys():
        console = get_node_console(drone_virl.plugin["SIMULATION_NAME"], node, simengine_host, virl_user, virl_password)
        try:
            print("    Console to {} -> `telnet {} {}`".format(node, console["host"], console["console_port"]))
        except TypeError:
            pass

def destroy_sim():
    """
    Destroy simulation.
    """
    # Get simulation list
    simulations = get_simulations(simengine_host, virl_user, virl_password)

    # See if a simulation is active
    if drone_virl.plugin["SIMULATION_NAME"] in simulations.keys():
        print("Simulation Currently Running")

        print("Killing VIRL Simulation: {}\n".format(drone_virl.plugin["SIMULATION_NAME"]))
        print(kill_simulation(drone_virl.plugin["SIMULATION_NAME"], simengine_host, virl_user, virl_password))
        print("Waiting 20 seconds to clear simulation")
        sleep(20)
        print("")

# Perform requested action
if drone_virl.plugin["ACTION"] == "create":
    create_sim()
elif drone_virl.plugin["ACTION"] == "destroy":
    destroy_sim()
else:
    print("Invalid action provided.")
    exit("Invalid action provided.")
