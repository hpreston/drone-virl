Use the VIRL plugin to manage network simulations that can be used for network configuration deployment verification and/or network testing.  

Actions supported include:

* **create** - Given a VIRL file and Simulation Name, create a new simulation.  An existing simulation with the same name will be destroyed first.  
* **destroy** - Destroy a running simulation with a given Simulation Name.

The following is a sample drone-virl configuration for your .drone.yml file.  A simulation is first started, then destroyed.  

```yaml
pipeline:
  StartTestNetwork:
    image: hpreston/drone-virl:latest
    virl_file: topology.virl
    simulation_name: TestNetwork
    action: create
    secrets: [ VIRL_USER, VIRL_PASSWORD, VIRL_HOST ]

  DestroyTestNetwork:
    image: hpreston/drone-virl:latest
    simulation_name: TestNetwork
    action: destroy
    secrets: [ VIRL_USER, VIRL_PASSWORD, VIRL_HOST ]
```

# Secrets

The drone-virl plugin requires reading the VIRL Server information from the secrets store within Drone.  Add the secrets with:

```bash
drone7 secret add --name VIRL_USER --value ${VIRL_USER} --repository myorg/myproject --image hpreston/drone-virl:latest

drone7 secret add --name VIRL_PASSWORD --value ${VIRL_PASSWORD} --repository myorg/myproject --image hpreston/drone-virl:latest

drone7 secret add --name VIRL_HOST --value ${VIRL_HOST} --repository myorg/myproject --image hpreston/drone-virl:latest
```

# Parameter Reference

* **virl_file** - The source VIRL file for a simulation.  File should be stored within the code repository.  Provide path relative to base of the repo.  
* **simulation_name** - The name of the VIRL simulation to manage.  
* **action** - The desired action to take.  Options are `create`, `destroy`
