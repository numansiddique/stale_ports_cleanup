import os
from neutronclient.v2_0.client import Client as NeutronClient


class RouterPortCleanup():
    def __init__(self):
        kwargs = {}
        kwargs['username'] = os.environ.get('OS_USERNAME')
        kwargs['tenant_name'] = os.environ.get('OS_TENANT_NAME')
        kwargs['auth_url'] = os.environ.get('OS_AUTH_URL')
        #kwargs['endpoint_url'] = os.environ.get('OS_AUTH_URL')
        kwargs['auth_strategy'] = 'keystone'
        kwargs['password']= os.environ.get('OS_PASSWORD')
        self.client = NeutronClient(**kwargs)
        self.subnets = []
        self.ports = []
    
    def _check_and_delete(self, port):
        for subnet in self.subnets:
            if port['fixed_ips'][0]['subnet_id'] == subnet['id']:
                if port['fixed_ips'][0]['ip_address'] == subnet['gateway_ip']:
                    # delete this port
                    print "Found a stale port : "+ port['id']                    
                    self.client.delete_port(port['id'])
                    print "Deleted the port : " + port['id']
                    print "\n\n"
                    return

    def clean_up_ports(self):
        """ Delete the stale ports.
        These ports have
        1. Empty device_id
        2. Empty device_owner
        3. The IP address of the port will be the gateway ip of the subnet 
        """
        
        # get the subnets
        self.subnets = self.client.list_subnets()['subnets']
        print "subnets = \n"
        print self.subnets
        print "\n"
        
        self.ports = self.client.list_ports()['ports']
              
        for port in self.ports:
            print "\n**************************"
            print 'port =' + str(port)
            print "\n"
            if len(port['device_owner']) == 0 and len(port['device_id']) == 0:
                self._check_and_delete(port)

router_cleanup = RouterPortCleanup()
router_cleanup.clean_up_ports()



    

