# fetch_rewards_assessment

This will spin up a VM on ec2 that you can run according to `directions.html`

#### 1) Pre-requisites to run

First you will need docker, and docker-compose installed to run this exercise.

* [Mac docker install instructions](https://docs.docker.com/docker-for-mac/install/)
* [Docker-compose install instructions](https://docs.docker.com/compose/install/)

#### 2) AWS Environment Setup

Please make sure you have an `~/.aws/credentials` file with your aws_access_key_id and aws_secret_access_key, for example:

```
[default]
aws_access_key_id = xxxxxxxxxxxxxx
aws_secret_access_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 3) config.yaml Setup

Please provide a config.yaml in the root of this git checkout directory, if not sure you can reference `example.config.yaml` and/or rename it to `config.yaml` after editing for desired values.

#### 4) Setup your SSH key 

Be sure to generate an SSH keypair if you have not already done so. You can run `ssh-keygen -t rsa -b 4096` and copy the key into config.yaml as required.

#### 4) Execute docker-compose to build the instance

You should be able to run `make run` or `docker-compose up` to build your VM.
That's it! You can follow the on-screen directions to log into the ec2/vm host and begin using it.