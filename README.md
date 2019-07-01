# ConsenSGX

ConsenSGX: Scaling Anonymous Communications Networks with Trusted Execution Environments
https://petsymposium.org/2019/files/papers/issue3/popets-2019-0050.pdf

This repository provides the scripts and instructions for recreating the experiments and graphs produced in our paper.

<hr>
<h2>Parsing Tor Consensuses</h2>

This section deals with analysing previous Tor consensus, and the scripts for it are in the subfolder Tor_consensus, specifically it reproduces
Figure 2, 3 and 4 of the paper. 

Past Tor consensuses are available to download at the Tor Metrics page:
https://metrics.torproject.org/collector/archive/relay-descriptors/consensuses/

The corresponding relay descriptors for the relays in a consensus are available at:
https://metrics.torproject.org/collector/archive/relay-descriptors/server-descriptors/

Gather the consensuses and relay descriptors for the months of interest with which you want to plot the histograms of relay descriptor sizes from the Tor Metrics site into the Tor_conesnsus folder.
For each month, extract the consensus and server descriptors into folders labelled YEAR_MM, which should give you a folder YEAR_MM, with the subfolders
consensuses-YEAR-MM and server-descriptors-YEAR-MM.

The hist_plot.py script produces Fig 3 and 4. As is the script generates this for the first consensus of 2018-09.
Some of the relay descriptors in the consensus for a month aren't available in the server descriptors of that month (these are older descriptors that haven't changed since when they were published).
Hence gather upto 6 months of older server descriptors from the Metrics site, and store them in the same format as mentioned before.

In hist_plot.py set TARGET_HIST_CONSENSUS to point at the consensus for which you want to plot the histogram for, and run
```
python plot_hist.py
```
 This will generate the two graphs hist_relays.png and hist_relays_pruned.png, where the latter has the histogram after pruning the policy and family fields of the relay descriptors as we describe in the paper.
 
To plot the bandwidth curve (Figure 2), use thie script bandwidth_curve.py.  Set the TARGET_CONSENSUS variable in the script to point at the consensus file that you want to plot the bandwidth curve for, and run
```
python bandwidth_curve.py
```
This will produce the bandwidth curve graph as relays_bws.png



<hr>

<h2> PIR Experiments </h2>
The experiments for ConsenSGX leverages 3 different PIR systems: 
XPIR, Percy and ZeroTrace

Create a working directory say CONSENSGX_WD, which will contain these 3 libraries.

1) XPIR: 
    Clone the fork of XPIR available at: 
    https://github.com/sshsshy/XPIR
  
    Follow the build instructions for it which is on the same page

2) Percy:
    Download the source files for Percy which is available at:
    http://percy.sourceforge.net/download.php

    To build the library, in the Percy folder: 
      First edit the Makefile, so that the NTL directory is /usr/include/NTL instead of /usr/local/include/NTL
      ```
      make depend
      make
      ```
 
3) ZeroTrace: 
    Clone the ZeroTrace library available at:
    https://github.com/sshsshy/ZeroTrace

    To build the library, in the ZeroTrace folder:
    ```
    make clean
    make
    ```

Once CONSENSGX_WD has been setup with the above three libraries, clone this repository into a directory for the experiment scripts, say CONSENSGX_ES.
The three main scripts are titled run_experiments_xpir, run_experiments_percy.sh, and run_experiments_zt.sh

To run these scripts in the CONSENSGX_ES folder invoke,:
```
./run_experiments_XYZ.sh <relays_start> <relays_stop> <increment_additive> <block_size> 
                         <no_of_requests> <bulk_batch_size> <Full_path_to_CONSENSGX_WD>
```
Here:

  <relays_start> <relays_stop> : sets the range of relays in a consensus to run experiments with.
  
  <increment_additive> : sets the increment to iterate from <relays_start> to <relays_stop>.
  
  <block_size> : sets the block size used by the PIR scheme. It should be set to the max relay descriptor size.
  
  <bulk_batch_size> : as described in the paper, this sets the parameter for number of relay descriptors to fetch in a request.

Running any experiment will create a folder called Results in the CONSENSGX_ES Folder, and store the results for the corresponding experiment in Results/XYZ.

Once the experiments have been run for the same set of parameters for all 3 PIR schemes, the generate_graphs.py script in CONSENGSX_ES can generate the graphs corresponding to these experiments by invoking:
```
./generate_graphs.py <relays_start> <relays_stop> <increment> <block_size> <no_of_req>
```
The script uses a statically defined list of bulk_batch_sizes ([10,50]), which we used for the paper. To try other values simply redefine it to your required values, and run the experiments for those bulk_batch_sizes before running the grapher script.



