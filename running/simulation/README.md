# InterSCSimulator

The InterSCSimulator version used in this experiment was containerized using
Docker and it is available in [docker hub](https://hub.docker.com/r/kanashiro/interscsimulator/).
So to reproduce the experiment you do not even need to have the simulator
installed and running in your machine, just ensure that you have docker and
docker-compose both installed and functional.

In order to make your life easier we create two docker-compose config files for
our scenarios (one for validation and another one representing São Paulo city).
In this folder you can find `docker-compose-validation-scenario.yml` and
`docker-compose-sao-paulo-scenario.yml`. They have almost everything that you
need, except the IP address of the host that is running your rabbitmq-server
instance (the rabbitmq is used to exchange messages with the anomaly detection
system). In short, do not forget to replace `<IP_ADRESS>` in docker-compose
config file with the right info before run the experiment.

# Running validation scenario

The input files for the validation scenario are in `validation_scenario` folder.
There you can find the files describing the map, the trips and the traffic
events. You must not change any of this file, the only one that you can modify
is the `config.xml`. There you have two lines, one to configure the simulation
without traffic events and another one with traffic events, so leave
uncommented the line that you are interested.

Now everything is set up and you just need to run:

```
$ docker-compose -f docker-compose-validation-scenario.yml up
```

When the simulation is over the output file will be placed in
`./interscsimulator_output`, copy it to another directory of your choice (if
you rerun the simulation it will be overwritten). Now you executed one round of
this scenario, to reproduce our work you need to repeat this more 19 times.
We recommend remove the container between the rounds execution, so execute this
command between rounds:

```
$ docker-compose -f docker-compose-validation-scenario.yml down
```

# Running São Paulo scenario

The input files for the São Paulo scenario are in `sao_paulo_scenario` folder.
There you can find the files describing the map, the trips and the traffic
events. You must not change any of this file, the only one that you can modify
is the `config.xml`. There you have two lines, one to configure the simulation
without traffic events and another one with traffic events, so leave
uncommented the line that you are interested.

Now everything is set up and you just need to run:

```
$ docker-compose -f docker-compose-sao-paulo-scenario.yml up
```

When the simulation is over the output file will be placed in
`./interscsimulator_output`, copy it to another directory of your choice (if
you rerun the simulation it will be overwritten). Now you executed one round of
this scenario, to reproduce our work you need to repeat this more 19 times.
We recommend remove the container between the rounds execution, so execute this
command between rounds:

```
$ docker-compose -f docker-compose-sao-paulo-scenario.yml down
```
