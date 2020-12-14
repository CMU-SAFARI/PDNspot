# PDNspot

PDNspot is a framework that enables the modeling of power delivery networks (PDNs) of modern processors. There are three commonly-used PDNs in modern client processors in multiple metrics of interest. PDNspot provides a versatile framework that enables multi-dimensional architecture-space exploration of modern processor PDNs. PDNspot evaluates the effect of multiple PDN parameters, TDP, and workloads on the metrics of interest. 


## Modeled PDNs
Architecting an efficient PDN for client processors (e.g., tablets, laptops, desktops) is a well-known challenge that has been hotly debated in industry and academia in recent years. Due to multiple constraints, a modern client processor typically implements only one of three types of commonly-used PDNs:
 
* Motherboard voltage regulators (MBVR)
* Low dropout voltage regulators (LDO) 
* Integrated voltage regulators (IVR)

We model these three PDNs using PDNspot. Variants of these PDNs can be modeled using PDNspot.

## Using PDNspot
PDNspot tool is written in Python (PDNspot.py). To configure your PDN, update the configuration file (pdns.yaml). You can update existing PDNs and their parameters to realize your target PDN.

```bash
PDNspot.py 
```
Example from pdns.yaml:
```bash
Name: MBVR
  # Define each sub-PDN below under SubPDN1, SubPDN2, ...
  SubPDN1:
    Name: Compute IVR
    # Off chip Efficiency of the sub PDN's voltage regulator (%).
    OffChipEffi: SVR 
    # Off chip loadline of the sub PDN (in milliohm).
    OffChipRLL: 2 
    # Application Ratio of the subPDN (all domains in the subPDN)
    AR: 55
    domains:
    - !Domain
      Name: Core0
      # Nominal Voltage required by the domain (V).
      Vnom: 0.82
```


## Citation
* Jawad Haj-Yahya, Mohammed Alser, Jeremie S. Kim, Lois Orosa, Efraim Rotem, Avi Mendelson, Anupam Chattopadhyay, and Onur Mutlu,
[**"FlexWatts: A Power- and Workload-Aware Hybrid Power Delivery Network for Energy-Efficient Microprocessors"**](https://people.inf.ethz.ch/omutlu/pub/FlexWatts-HybridPowerDeliveryNetwork_micro20.pdf)
Proceedings of the 53rd International Symposium on Microarchitecture (MICRO), Virtual, October 2020.


## Contributors
* **Jawad Haj-Yahya** (ETH Zurich) 

##Talks
The presentations of the paper are available on YouTube:
* [**MICRO 2020 Full Talk Video (15 minutes)**](https://www.youtube.com/watch?v=P97EsW7dzQ4)
  * [**slides**](https://people.inf.ethz.ch/omutlu/pub/FlexWatts-HybridPowerDeliveryNetwork_micro20-talk.pdf)
* [**MICRO 2020Short Talk Video and Q&A (15 minutes)**](https://www.youtube.com/watch?v=wd7U2jrjHBM)
  * [**slides**](https://people.inf.ethz.ch/omutlu/pub/FlexWatts-HybridPowerDeliveryNetwork_micro20-short-talk.pdf)

## Contact
Jawad Haj-Yahya (jhajyahya@ethz.ch)




