# InterSCity Experiment - Emulation Based On Anomaly Detection In Car Traffic

## Data Analysis

Our complete data analysis can be found in the `Analysis.ipynb` file. You can open
the file using Github itself to see our results and analysis or, to reproduce the
results, you open it with Jupyter Notebook and rerun the cells (we recommend
reading this whole file before running it). Also, if you have any questions, you
can contact us in IRC (freenode#ccsl-usp).

For the **Validation Experiment** you should check the
``validation`` folder, where in the ``validation/datasets`` folder you can find
the three datasets used in the analysis (one per scenario) and in the
``validation/inputs`` folder you can find the inputs used by the simulator and
the Spark scripts.

For the **City Scale Experiment** (based on a São Paulo environment) you should
check the ``city_scale`` folder, where in the ``city_scale/datasets`` folder
you can find the five datasets used. Since the City Scale datasets large (and
downloading them would make the reproductibility harder), we zipped them in
`tar.gz` files and removed the `output.csv` files (it is just a file containing
the data generated by every round). To generate the `output.csv` file enter in
a dataset folder (after unzipping it) and run:

```
cat round_{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20}.csv >> ../output
```

The `Analysis.ipynb` file will correctly use the `output.csv` files generated
and everything will be fine. In the ``city_scale/inputs`` folder you can find
the inputs used by the simulator and the Spark Scripts.

## The Datasets

The datasets are composed of 20 rounds (stored in `round_x.csv` files and after
merged in a single `output.csv` file). In each round, the `csv` has 8 fields,
that are, in the following order

- **hour**: The hour where the round started to run 

- **minute**: The minute where the round started to run

- **last_tick**: The last simulation tick of a given car trip (each tick meaning
a second).

- **type**: The type of the data in the output; every data will be of type
**arrival**

- **trip_id**: The identifier of a given trip

- **last_link**: The last graph edge of a given trip

- **duration**: The total duration of a given trip (so you can infer the first
tick of a trip combining the duration and the last tick)

- **distance**: The total distance (edges) of a given trip

So, for instance, a line in the csv containing
```
15;40;55;arrival;1_1;20;8;3
```
Means that such trip was simulated at `15:40`, ended in the second **55**,
can be find using the identifier **1_1**, ended in the edge identified by
**20** (check the map input of the experiment), has duration **8** (so it
started in tick **47**) and, in total, is composed of **3** edges.

