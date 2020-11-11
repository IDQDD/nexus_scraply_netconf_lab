# netconf xml rpc templates for configuring vlan, SVI, l2vni (evpn) with anycast SVI
# on a cisco nexus swicthes via netconf 
tpl_system_head = '<System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">'
tpl_system_tail = '</System>'

tpl_config_head = '<config>' + tpl_system_head
tpl_config_tail = tpl_system_tail + '</config>'  

# config vlans
tpl_bd_get = """
<bd-items>
    <bd-items>
        <BD-list>
            <fabEncap>vlan-{vlan_id}</fabEncap>                
        </BD-list>
    </bd-items>
</bd-items>"""

tpl_bd_remove = """
<bd-items>
    <bd-items>
        <BD-list operation="remove">
            <fabEncap>vlan-{vlan_id}</fabEncap>                
        </BD-list>
    </bd-items>
</bd-items>"""

tpl_bd_conf = """
<bd-items>
    <bd-items>
        <BD-list operation="replace">
            <fabEncap>vlan-{vlan_id}</fabEncap>
            <name>{vlan_name}</name>
            <BdState>active</BdState>
            <adminSt>active</adminSt>
            <bridgeMode>mac</bridgeMode>
            <fwdCtrl>mdst-flood</fwdCtrl>
            <fwdMode>bridge,route</fwdMode>
            <id>{vlan_id}</id>
            <mode>CE</mode>
        </BD-list>
    </bd-items>
</bd-items>"""

tpl_bd_vxlan_conf = """
<bd-items>
    <bd-items>
        <BD-list operation="replace">
            <fabEncap>vlan-{vlan_id}</fabEncap>
            <name>{vlan_name}</name>
            <BdState>active</BdState>
            <accEncap>vxlan-{vni}</accEncap>
            <adminSt>active</adminSt>
            <bridgeMode>mac</bridgeMode>
            <fwdCtrl>mdst-flood</fwdCtrl>
            <fwdMode>bridge,route</fwdMode>
            <id>{vlan_id}</id>
            <mode>CE</mode>
        </BD-list>
    </bd-items>
</bd-items>"""


# config svi
tpl_svi_get = """
<intf-items>
    <svi-items>
        <If-list>
            <id>vlan{vlan_id}</id>
        </If-list>
    </svi-items>
</intf-items>
<ipv4-items>
    <inst-items>
        <dom-items>
            <Dom-list>
                <name>{vrf_name}</name>
                <if-items>
                    <If-list>
                        <id>vlan{vlan_id}</id>                            
                    </If-list>
                </if-items>
            </Dom-list>
        </dom-items>
    </inst-items>
</ipv4-items>"""

tpl_svi_remove = """
<intf-items>
    <svi-items>
        <If-list operation="remove">
            <id>vlan{vlan_id}</id>
        </If-list>
    </svi-items>
</intf-items>"""

tpl_svi_conf = """
    <intf-items>
        <svi-items>
            <If-list operation="replace">
                <id>vlan{vlan_id}</id>
                <mtu>{mtu}</mtu>
                <descr>{description}</descr>
                <adminSt>up</adminSt>
                <rtvrfMbr-items>
                    <tDn>/System/inst-items/Inst-list[name='{vrf_name}']</tDn>
                </rtvrfMbr-items>
                <vlanId>{vlan_id}</vlanId>
            </If-list>
        </svi-items>
    </intf-items>
    <ipv4-items>
        <inst-items>
            <dom-items>
                <Dom-list>
                    <name>{vrf_name}</name>
                    <if-items>
                        <If-list operation="replace">
                            <id>vlan{vlan_id}</id>
                            <addr-items>
                                <Addr-list>
                                    <addr>{ip_address}</addr>
                                </Addr-list>
                            </addr-items>
                        </If-list>
                    </if-items>
                </Dom-list>
            </dom-items>
        </inst-items>
    </ipv4-items>"""
    
tpl_svi_anycast_conf = tpl_svi_conf + """    
<hmm-items>
    <fwdinst-items>
        <if-items>
            <FwdIf-list operation="replace">
                <id>vlan{vlan_id}</id>
                <adminSt>enabled</adminSt>
                <mode>anycastGW</mode>
            </FwdIf-list>
        </if-items>
    </fwdinst-items>
</hmm-items>"""


# nve1 (vtep) interface
tpl_nve_get = """
<eps-items>
    <epId-items>
        <Ep-list>
            <epId>1</epId>
            <nws-items>
                <vni-items>
                    <Nw-list>
                        <vni>{vni}</vni>           
                    </Nw-list>
                </vni-items>
            </nws-items>
        </Ep-list>
    </epId-items>
</eps-items>"""

tpl_nve_remove = """
<eps-items>
    <epId-items>
        <Ep-list>
            <epId>1</epId>
            <nws-items>
                <vni-items>
                    <Nw-list operation="remove">
                        <vni>{vni}</vni>           
                    </Nw-list>
                </vni-items>
            </nws-items>
        </Ep-list>
    </epId-items>
</eps-items>"""

tpl_nve_mcast_conf = """
<eps-items>
    <epId-items>
        <Ep-list>
            <epId>1</epId>
            <nws-items>
                <vni-items>
                    <Nw-list operation="replace">
                        <vni>{vni}</vni>
                        <mcastGroup>{mgroup}</mcastGroup>                                                        
                    </Nw-list>
                </vni-items>
            </nws-items>
        </Ep-list>
    </epId-items>
</eps-items>"""

tpl_nve_ingress_conf = """
<eps-items>
    <epId-items>
        <Ep-list>
            <epId>1</epId>
            <nws-items>
                <vni-items>
                    <Nw-list operation="replace">
                        <vni>{vni}</vni>
                        <IngRepl-items>
                            <proto>bgp</proto>
                        </IngRepl-items>                            
                    </Nw-list>
                </vni-items>
            </nws-items>
        </Ep-list>
    </epId-items>
</eps-items>"""


# bgp evpn configs
tpl_bgp_evpn_get = """
<evpn-items>    
    <bdevi-items>
        <BDEvi-list>
            <encap>vxlan-{vni}</encap>                
        </BDEvi-list>
    </bdevi-items>
</evpn-items>"""

tpl_bgp_evpn_remove = """
<evpn-items>    
    <bdevi-items>
        <BDEvi-list operation="remove">
            <encap>vxlan-{vni}</encap>                
        </BDEvi-list>
    </bdevi-items>
</evpn-items>"""

tpl_bgp_evpn_conf = """
<evpn-items>
    <adminSt>enabled</adminSt>
    <bdevi-items>
        <BDEvi-list operation="replace">
            <encap>vxlan-{vni}</encap>
            <rd>rd:unknown:0:0</rd>
            <rttp-items>
                <RttP-list>
                    <type>export</type>
                    <ent-items>
                        <RttEntry-list>
                            <rtt>route-target:unknown:0:0</rtt>
                        </RttEntry-list>
                    </ent-items>
                </RttP-list>
                <RttP-list>
                    <type>import</type>
                    <ent-items>
                        <RttEntry-list>
                            <rtt>route-target:unknown:0:0</rtt>
                        </RttEntry-list>
                    </ent-items>
                </RttP-list>
            </rttp-items>
        </BDEvi-list>
    </bdevi-items>
</evpn-items>"""
