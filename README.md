stale_ports_cleanup
===================

This script deletes the left over ports after a router has been deleted. Fix is already commited to raise an exception if the user tries to delete a router which has ports attached to it. 

Instructions to run the script
-----------------------------
1. Source the openrc script with admin credentials
2. Run the script --> python router_port_cleanup.py

