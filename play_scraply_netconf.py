# play with cisco nexus and scrapli_netconf

from netconf_data_class import evpn_data, vlan_svi_data
from scrapli_netconf.driver import NetconfScrape

def config_scrapi_netconf(conn, config, datastore='running'):    
    response = conn.edit_config(config=config, target=datastore)
    return response

def get_scrapli_netconf(conn, filter_):
    response = conn.get(filter_=filter_, filter_type="subtree")
    return response

# lab1 create/delete vlan and svi
# will be playing with public available cisco nexus sandbox
sandbox = {
    "host": "sbx-nxos-mgmt.cisco.com",
    "port": 10000,
    "auth_username": "admin",
    "auth_password": "Admin_1234!",
    "auth_strict_key": False,    
}

vlan2345 = vlan_svi_data(2345, ip_address='10.0.23.45/24', vlan_name='VLAN2345', description='SVI by  Netconf')

with NetconfScrape(**sandbox) as conn:
    print("************** creating the svi ******************")
    resp1 = config_scrapi_netconf(conn, vlan2345.get_rpc_create())
    print(resp1.result)

    print("*************** check the svi *********************")
    resp1 = get_scrapli_netconf(conn, vlan2345.get_rpc_get())
    print(resp1.result)

    print("************** deleting the svi *******************")
    resp1 = config_scrapi_netconf(conn, vlan2345.get_rpc_remove())
    print(resp1.result)

    print("*** check the svi are gone along with the vlan ****")
    resp1 = get_scrapli_netconf(conn, vlan2345.get_rpc_get())
    print(resp1.result)


# lab2 playing with evpns
# the sandbox doesn't support evpn so I will be playing with my own gears
my_device = {
    "host": "192.168.99.91",
    "auth_username": "apiuser",
    "auth_password": "apipassword",
    "auth_strict_key": False,        
}

evpn10 = evpn_data(333, 10333, '10.3.3.3/24', mtu=9000, mgroup='230.1.1.3')
evpn20 = evpn_data(444, 10444, '10.4.4.4/24', mgroup='230.1.1.4', description='anycast SVI (by netconf)', supARP=True)

with NetconfScrape(**my_device) as conn:
    print("************** creating evpns ******************")
    resp1 = config_scrapi_netconf(conn, evpn10.get_rpc_create())
    resp2 = config_scrapi_netconf(conn, evpn20.get_rpc_create())
    print(f"{resp1.result = }\n{resp2.result = }")

    print("*************** check evpns *********************")
    resp1 = get_scrapli_netconf(conn, evpn10.get_rpc_get())
    resp2 = get_scrapli_netconf(conn, evpn20.get_rpc_get())
    print(resp1.result, resp2.result)

    breakpoint() # have some time to check configs on the switch

    print("************** deleting evpns *******************")
    resp1 = config_scrapi_netconf(conn, evpn10.get_rpc_remove())
    resp2 = config_scrapi_netconf(conn, evpn20.get_rpc_remove())
    print(f"{resp1.result = }\n{resp2.result = }")

    print("*********** check evpns are gone *****************")
    resp1 = get_scrapli_netconf(conn, evpn10.get_rpc_get())
    resp2 = get_scrapli_netconf(conn, evpn20.get_rpc_get())
    print(resp1.result, resp2.result)
