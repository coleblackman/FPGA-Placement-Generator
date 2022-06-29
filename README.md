# FPGA-Placement-Generator

**This tool is a work in project**

This tool generates a macro_placement.cfg file for use with OpenLANE and OpenFPGA. It takes as input a config.tcl file, an fpga_top.v and your parameters.

Motivation: 

The advantage of using this tool over allowing OpenLANE to determine P&R automatically is this script enables an "island-style" *even* distribution of configurable logic blocks (CLBs) and other elements. Another goal is to conform to design rules requirements regarding edge spacing. 

Existing scripts, such as that used by SOFA, are not open source. 
