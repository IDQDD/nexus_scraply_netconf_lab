from dataclasses import dataclass
from ipaddress import IPv4Address, IPv4Interface, IPv4Network
from tpl_evpn_xml import *

@dataclass
class vlan_svi_data:
    # mandatory data
    vlan_id: int    
    # optional data (with defaults)
    ip_address: str = '' # can be blank for a remove operation but mandatory for a creating one
    vlan_name: str = ''
    mtu: int = 1500
    description: str = 'SVI created by netconf'
    vrf_name: str = 'default'

    def __check_ip_int(self):
        try :
            IPv4Interface(self.ip_address)
        except ValueError:
            return False
            
        try: 
            IPv4Network(self.ip_address)
            return False
        except:
            return True    

    def __post_init__(self):
        pass        

    def get_rpc_create(self):
        if not self.vlan_name:
            self.vlan_name = 'VLAN' + str(self.vlan_id) 
        if not self.__check_ip_int():
            raise ValueError('Incorrect Interface IP address')        

        return (tpl_config_head + 
                tpl_bd_conf.format(vlan_id=self.vlan_id, vlan_name=self.vlan_name) +
                tpl_svi_conf.format(vlan_id=self.vlan_id, mtu=self.mtu, description=self.description, vrf_name=self.vrf_name, ip_address=self.ip_address) +                 
                tpl_config_tail)

    def get_rpc_get(self):
        return (tpl_system_head + 
                tpl_bd_get.format(vlan_id=self.vlan_id) +
                tpl_svi_get.format(vlan_id=self.vlan_id, vrf_name=self.vrf_name) +
                tpl_system_tail)

    def get_rpc_remove(self):
        return (tpl_config_head + 
                tpl_bd_remove.format(vlan_id=self.vlan_id) +
                tpl_svi_remove.format(vlan_id=self.vlan_id) +                
                tpl_config_tail)


@dataclass
class evpn_data:
    # mandatory data
    vlan_id: int
    vni: int
    # optional data (with defaults)
    ip_address: str = '' # can be blank for a remove operation but mandatory for a creating one
    vlan_name: str = ''
    mtu: int = 1500
    description: str = 'anycast SVI'
    vrf_name: str = 'Tenant-1'
    mgroup: str = ''
    supARP: bool = False

    def __check_ip_int(self):
        try :
            IPv4Interface(self.ip_address)
        except ValueError:
            return False
            
        try: 
            IPv4Network(self.ip_address)
            return False
        except:
            return True

    def __check_ip_mcast(self):
        try: 
            return IPv4Address(self.mgroup).is_multicast
        except:
            return False

    def __post_init__(self):
        pass        

    def get_rpc_create(self):
        if not self.vlan_name:
            self.vlan_name = 'l2VNI-' + str(self.vni) 
        if not self.__check_ip_int():
            raise ValueError('Incorrect Interface IP address')
        if self.mgroup:
            if not self.__check_ip_mcast():
                raise ValueError('Incorrect multicast group IP address')
        self.supARP = 'enabled' if self.supARP else 'off'

        return (tpl_config_head + 
                tpl_bd_vxlan_conf.format(vlan_id=self.vlan_id, vlan_name=self.vlan_name, vni=self.vni) +
                tpl_svi_anycast_conf.format(vlan_id=self.vlan_id, mtu=self.mtu, description=self.description, vrf_name=self.vrf_name, ip_address=self.ip_address) + 
                (tpl_nve_mcast_conf.format(vni=self.vni, mgroup=self.mgroup, supARP=self.supARP) if self.mgroup else tpl_nve_ingress_conf.format(vni=self.vni, supARP=self.supARP)) + 
                tpl_bgp_evpn_conf.format(vni=self.vni) + 
                tpl_config_tail)

    def get_rpc_get(self):
        return (tpl_system_head + 
                tpl_bd_get.format(vlan_id=self.vlan_id) +
                tpl_svi_get.format(vlan_id=self.vlan_id, vrf_name=self.vrf_name) +
                tpl_nve_get.format(vni=self.vni) +
                tpl_bgp_evpn_get.format(vni=self.vni) +
                tpl_system_tail)

    def get_rpc_remove(self):
        return (tpl_config_head + 
                tpl_bd_remove.format(vlan_id=self.vlan_id) +
                tpl_svi_remove.format(vlan_id=self.vlan_id) +
                tpl_nve_remove.format(vni=self.vni) +
                tpl_bgp_evpn_remove.format(vni=self.vni) +
                tpl_config_tail)

    def get_rpc_ypath(self):        
        pass
