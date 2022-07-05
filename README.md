# FPGA-Placement-Generator

**This tool is a work in progress**

This tool generates a macro_placement.cfg file for use with OpenLANE and OpenFPGA. It takes as input a config.tcl file, an fpga_top.v and your parameters. It requires pre-hardened macros for each block as well. 

Motivation: 

The advantage of using this tool over allowing OpenLANE to determine P&R automatically is this script enables an "island-style" *even* distribution of configurable logic blocks (CLBs) and other elements, which currently OpenLANE does not. Another goal is to conform to design rules requirements regarding edge spacing, and to enable user-friendly configurability specific to FPGA design.

Existing scripts, such as that used by SOFA, are not open source. 

FPGA design typically requires specialized teams of experienced engineers. With tools such as OpenLANE, OpenFPGA, and others, it is becoming possible to produce a tape-out ready FPGA with only a small team of hardware engineers.

This script will not allow overlap between macros.

Use:

- Make sure OpenLANE and OpenFPGA are installed. 
- Clone the repo. 
- Optionally, copy the repo scripts into a directory containing the requisite files: config.tcl for each module, gds and lef for each pre-hardened module, either an fpga_top.v or fpga_core.v (fpga_core.v if using certain OpenFPGA configurations), and your FPGA config.tcl file. If you don't copy/move these scripts into this directory and you don't provide a command line argument, the script will prompt you to input a starting directory containing all of these requisites. 
- Run ```python3.8 placement_cfg_gen.py``` or ```python3.8 placement_cfg_gen.py absolute/path/to/starting/directory```
