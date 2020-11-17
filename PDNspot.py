#!/usr/bin/env python3

import yaml
import sys
import ruamel.yaml

def Pgb (Pnom, FL, Vnom, Vgb, delta):
    #  return Pnom * ( ((FL/100)*(pow( (Vnom+(Vgb/1000))/Vnom)),delta) + (1- FL/100)*(pow(((Vnom+(Vgb/1000))/Vnom)),2))
    Vratio= (Vnom+(Vgb/1000))/Vnom
    return Pnom * ((FL/100)*pow(Vratio, delta) + (1- FL/100)*pow(Vratio,2))

def Pd_ll (Vd,AR,Rd_ll,Pd):
    Vd_ll = Vd + (Pd/(AR*Vd))*Rd_ll 
    return Vd_ll*Pd/Vd
def SVR_effi(Vin,   Vout,  Iout):
    return 0.88

def CalcPpdn (PDN):
    Ppdn = 0
    Vbat = 0
    for spdn in PDN.subPDNs:
        P_D = 0
        V_D = 0
        for domain in spdn['domains']:
            # calculate P_GB, V_GB and update the nominal voltage and power 
            domain.Pnom = Pgb(domain.Pnom,domain.FL,domain.Vnom,domain.Vtob,domain.delta)
            domain.Vnom = domain.Vnom + domain.Vtob
            # calculate new voltage guardband (e.g., due to the power-gate)
            domain.Vtob =  (domain.Pnom/(domain.AR*domain.Vnom))*domain.EPG/1000 
            #update nominal voltage and power 
            domain.Pnom = Pgb(domain.Pnom,domain.FL,domain.Vnom,domain.Vtob,domain.delta)
            domain.Vnom = domain.Vnom + domain.Vtob
            domain.Vtob = 0
            V_D = max(V_D,domain.Vnom)    
        for domain in spdn['domains']:
            domain.Vtob = V_D - domain.Vnom
            domain.Pnom = Pgb(domain.Pnom,domain.FL,domain.Vnom,domain.Vtob,domain.delta)
            domain.Vnom = domain.Vnom + domain.Vtob
            P_D += domain.Pnom
        spdn_AR =  float(str(spdn['AR']))
        spdn_RLL = float(spdn['OffChipRLL'])
        Vd_ll = V_D + P_D/(spdn_AR*V_D)*spdn_RLL/1000
        Pd_ll = Vd_ll*P_D/V_D
        Id_ll = Pd_ll/Vd_ll
        Ppdn += Pd_ll/SVR_effi(Vbat,Vd_ll,Id_ll)
        print ("Compeleted " +str(spdn['Name'])+str(spdn['AR']))

    return Ppdn



class Domain:
    def __init__(self, name=None, Vnom=None, Vtob=None, Pnom=None, AR=None, EPG=None, FL=None, delta=None, OnChipEffi=None):
        self.name = name
        self.Vnom = Vnom
        self.Vtob = Vtob
        self.Pnom = Pnom
        self.AR = AR
        self.EPG = EPG
        self.FL = FL
        self.delta = delta
        self.OnChipEffi = OnChipEffi

    @classmethod
    def from_yaml(cls, constructor, node):
        for m in constructor.construct_yaml_map(node):
            pass
        return cls(m['Name'], m['Vnom'], m['Vtob'], m['Pnom'], m['AR'], m['EPG'], m['FL'], m['delta'], m['OnChipEffi'])

    def __repr__(self):
        return 'Domain(name={.name}, Vnom={.Vnom}, Vtob={.Vtob}, Pnom={.Pnom}, AR={.AR}, EPG={.EPG}, FL={.FL}, delta={.delta}, OnChipEffi={.OnChipEffi})'.format(self, self)

class PDN:
    def __init__(self, name=None, object=None, subPDNs=None):
        self.name = name
        self.object = object
        self.subPDNs = [] if subPDNs is None else subPDNs

    @classmethod
    def from_yaml(cls, constructor, node):
        for m in constructor.construct_yaml_map(node):
            pass
        if 'Name' in m:
            name = m['Name']
        elif 'name' in m:
            name = m['name']
        else:
            name = None
        object = m['object'] if 'object' in m else None
        if 'subPDNs' in m:
            subPDNs = m['subPDNs']
        elif 'SubPDN1' in m:
            x = 1
            subPDNs = []
            while True:
                sub_name = "SubPDN{}".format(x)
                try:
                    subPDNs.append(m[sub_name])
                except KeyError:
                    break
                x += 1
        else:
            subPDNs = None
        return cls(name, object, subPDNs)

    def __repr__(self):
        return 'PDN(name={}, object={}, subPDNs{})'.format(
            self.name, self.object, '[...]' if self.subPDNs else '[]',
        )

yaml = ruamel.yaml.YAML(typ='safe')
yaml.register_class(Domain)
yaml.register_class(PDN)
with open('pdns.yaml') as fp:
    pdns = yaml.load(fp)

for pdn in pdns:
    print("Total Power of PDN: " +str(pdn.name)+ " is " + str(CalcPpdn(pdn)))