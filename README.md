# DtS-IoT Resource Allocation Analysis Framework (DRAAF)

DRAAF is a framework designed to enable rapid testing of satellite based simulation tooling. It is composed of three parts: i) a set of performance metrics that make up the evaluation scheme; ii) a set of benchmark scenarios, which are the control variables that define the use cases; and iii) a software-based toolchain contained in this repository. A paper on DRAAF was presented as part of the WFIoT24 conference titled "DtS-IoT Resource Allocation Analysis Framework: Assessing DQ and RESS-IoT". While DRAAF was initially created to support resource analysis for DtS-IoT use cases it has been extended to support inter-satellite communication use cases as well. These include inter and intra-constellation links.

## Project Structure

- The workspaces encapsulate each experiment.
- The data sources store the simulation data in the raw format and the transformed and filtered format. These data sources are decoupled from the specific workspace experiments, allowing users to mix and match wht data is used without duplicating data sources.
- The `etl.py` file defines the over all structure of the DRAAF ETL pipeline.
- The `metric_engine.py` file defines the equations to produce the metrics.
- The `protocol_definitions.py` file defines the protocol specific energy models used to generate the metrics.
- The `graph_manager.py` file stores the generic class to save and generate different types of graphs including standard plots, error bars, and spider graphs.

## Usage

The user-centric sections of DRAAF are focused around the workspaces. A workspace can map to a research paper or experiment. Each workspace is composed of a client file which can be a jupyter notebook or a python script that creates a DRAAF ETL pipeline by selecting the data sources and executing it. This will produce a json file that can be ingested by the GraphManager which can produce various graphs based on the selected metrics to be used for comparison. Examples of workspaces can be seen in the folder including the `draaf_conference_workspace` which was used for the initial DRAAF paper.