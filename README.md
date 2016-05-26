# A10 Networks Openstack Horizon Dashboard
===========================================

A10 Networks Openstack Horizon Dashboard for Thunder, vThunder and AX Series Appliances

Supported releases:

* OpenStack: Icehouse, Juno, Kilo, Liberty, Mitaka
* LBaaS versions: v1, v2
* ACOS versions: ACOS 2/AxAPI 2.1 (ACOS 2.7.2+), ACOS 4/AxAPI 3.0 (ACOS 4.0.1-GA +)

Working but not available for support:

* OpenStack: git/master

## A10 github repos

- [a10-horizon](https://github.com/a10networks/a10-horizon) - A10 Horizon Dashboard repo.
- [a10-neutron-lbaas](https://github.com/a10networks/a10-neutron-lbaas) - Main A10 LBaaS driver repo. Middleware sitting between the
openstack driver and our API client, mapping openstack constructs to A10's AxAPI.
- [acos-client](https://github.com/a10networks/acos-client) - AxAPI client used by A10's OpenStack driver
- [a10-openstack-lbaas](https://github.com/a10networks/a10-openstack-lbaas) - OpenStack LBaaS driver,
identical to the files that are currently merged into neutron-lbaas.  Pypi package
'a10-openstack-lbaas'.
- [a10-openstack-lbaas, havana branch](https://github.com/a10networks/a10-openstack-lbaas/tree/havana) - OpenStack
LBaaS driver, for the Havana release.  Pypi package 'a10-openstack-lbaas-havana'.
- [a10networks-ci/project-config](https://github.com/a10networks-ci/project-config) - A10 Networks OpenStack third-party CI setup scripts


## Installation steps:

### Step 1:

Make sure you have horizon installed.  This dashboard will need to be installed on all of your Horizon nodes if you are running Horizon in an HA environment.


### Step 2:

The latest supported version of a10-horizon is available via standard pypi repositories and the current development version is available on github.

##### Installation from pypi
```sh
sudo pip install a10-horizon
```

##### Installation from cloned git repository.

Download the dashboard from: <https://github.com/a10networks/a10-horizon>



```sh
sudo pip install git+https://github.com/a10networks/a10-horizon.git
```

```sh
git clone https://github.com/a10networks/a10-horizon.git
cd a10-horizon
sudo pip install -e .
```

## Configuration

Horizon provides a plugin architecture for adding external panels.  To enable the A10 Networks Horizon UI dashboard, simply copy the files from `a10_horizon/_enabled_hooks` to the `local/enabled` directory in your Horizon Openstack dashboard directory.  These paths can be auto-discovered by typing the following commands:

### a10-horizon path
```sh
python -c "import a10_horizon; print(a10_horizon.__path__[0])"
```
### Horizon dashboard path
```sh
python -c "import openstack_dashboard; print (openstack_dashboard.__path__[0])"
```
## Restart necessary services

a10-horizon has static resources that must be "collected" by Horizon.  Following the installation of a10-horizon, execute the following command in the directory where you have installed Horizon:
```sh
./manage.py collectstatic
./manage.py compress
```

Restart horizon after configuration updates (exact command may vary depending
  on OpenStack packaging.)

```sh
service apache2 restart
```


## Examples

## A10 Community

Feel free to fork, submit pull requests, or join us on freenode IRC, channel #a10-openstack. Serious support escalations and formal feature requests must
still go through standard A10 processes.

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
