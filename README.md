# InterSCity Experiment - Emulation Based On Anomaly Detection In Car Traffic

This repository contains our analysis and everything needed to run the
experiment **Emulation Based on Anomaly Detection In Car Traffic**. In this
experiment we evaluate actuation in a city traffic simulation via traffic boards,
that alerts drivers about closed streets and are triggered via anomaly detection.
In our context, we refer to **events** as **close street events**, that are
configurable and predefined by us.

So, in this experiment, we:

- Simulate a city traffic

- During the simulation, a few events will affect the roads, closing them

- Since the roads behaviour are going to change, we will detect them as
anomalies and trigger traffic boards

- Drivers that arrive at nodes containing triggered traffic boards will
have a chance to recalculate their route, letting them plan a better route

We separated the experiment in two scenarios: in the first, that we called
**validation scenario**, we used a fairly simple graph to validate our models and
algorithms. In the second scenario, that we called **sao paulo scenario**, we
used a reduced São Paulo map, with events in two clusters, and with traffic boards
in high traffic edges. For each scenario we used a three phases separation, and in
each phase we runned 20 simulations. The first phase is a simulation **without
events** and **without traffic boards**, and was used as our baseline to find
the thresholds to classify roads as anomalies. The second phase is a simulation
**with events and without traffic boards**, and was expected to have the slowest
travels in comparison to the others two phases. Finally, the third phase is a
simulation **with events and with traffic boards**, were we used a small anomaly
detection system (written in Apache Spark) to trigger the traffic boards.

Next, we describe the structure of this repository, which will help
you to understand and reproduce the results.

#### `img` folder

This folder holds the images used in our Jupyter Notebooks. You can skip it! :)

#### `running` folder

This folder holds everything needed to reproduce the simulation and the scenarios.
There you will find a `README.md` file that better describes the steps needed
to rerun the scenarios.

#### scenario_1_validation

This folder holds the results of the first scenario simulated. In the
`scenario_1_validation/datasets` folder you will find three folders, one for each
phase of the scenario, and in each of these folders, an `output.csv` file, which
aggregates the results of the 20 rounds simulated, and a `rounds` folder, which
stores the results of each of these rounds. In `scenario_1_validation/inputs` you
will find the inputs used by the simulator for this scenario, where the `hex_map.xml`
is the map used.

#### scenario_2_sao_paulo

This folder holds the results of the second scenario simulated. In the
`scenario_2_sao_paulo/datasets` folder you will find three folders, one for each
phase of the scenario, and in each of these folders, an `output.csv` file, which
aggregates the results of the 20 rounds simulated, and a `rounds` folder, which
stores the results of each of these rounds. In `scenario_2_sao_paulo/inputs` you
will find the inputs used by the simulator for this scenario, where the `map.xml`
is the map used.

#### `utils` folder

This folder holds useful scripts that you might find useful if you want to reproduce
everything that we used. For instance, here you can find a Jupyter Notebook that
generates the `map.xml` file used by the simulator in the second scenario of the
experiment.

#### Data Analysis

Our complete data analysis can be found in the `Analysis.ipynb` file. You can open
the file using Github itself to see our results and analysis or, to reproduce the
results, you can open it with Jupyter Notebook and rerun the cells (we recommend
reading this whole file before trying to run it). Also, if you have any questions,
you can contact us in IRC (freenode#ccsl-usp).

For the **Validation scenario** you should check the
``scenario_1_validation`` folder, where in the ``validation/datasets`` folder you can
find the three datasets used in the analysis (one per scenario) and in the
``validation/inputs`` folder you can find the inputs used by our scrips.

For the **São Paulo scenario** you should
check the ``scenario_2_sao_paulo`` folder, where in the ``scenario_2_sao_paulo/datasets``
folder you can find the three datasets generated.

In the datasets folders you will find a folder for each phase of the experiment

```
cat round_{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20}.csv >> ../output
```

The `Analysis.ipynb` file will correctly use the `output.csv` files generated
and everything will be fine. In the ``city_scale/inputs`` folder you can find
the inputs used by the simulator and the Spark Scripts.
