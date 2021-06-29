# Fetch Rewards Coding Assessment - Cloud Engineer

### What do I need to do?

Develop an automation program that takes a YAML configuration file as input and deploys a Linux AWS EC2 instance with two volumes and two users.

Here are some guidelines to follow:

*   Create a YAML file based on the configuration provided below for consumption by your application
*   You may modify the configuration, but do not do so to the extent that you fundamentally change the exercise
*   Include the YAML config file in your repo
*   Use Python and Boto3
*   Do not use configuration management, provisioning, or IaC tools such as Ansible, CloudFormation, Terraform, etc.



    ---
      # This YAML configuration specifies a server with two volumes and two users
      server:
        instance_type: t2.micro
        ami_type: amzn2
        architecture: x86_64
        root_device_type: ebs
        virtualization_type: hvm
        min_count: 1
        max_count: 1
        volumes:
          - device: /dev/xvda
            size_gb: 10
            type: ext4
            mount: /
          - device: /dev/xvdf
            size_gb: 100
            type: xfs
            mount: /data
        users:
          - login: user1
            ssh_key: --user1 ssh public key goes here-- user1@localhost
          - login: user2
            ssh_key: --user2 ssh public key goes here-- user2@localhost


### What are the requirements?

We must be able to:

1.  Run your program
2.  Deploy the virtual machine
3.  SSH into the instance as user1 and user2
4.  Read from and write to each of two volumes

Please assume the evaluator does not have prior experience executing programs in your chosen language or creating virtual machines via your chosen deployment method. Therefore, please include any documentation necessary to accomplish the above requirements.

### How do I submit it?

Provide a link to a public repository (i.e., GitHub, Bitbucket) to your recruiter. Please do not send files directly via email.

### FAQs

**How will this exercise be evaluated?**

An engineer will review the code you submit. At a minimum they must be able to run the program, and the program must produce the expected results. You should provide any necessary documentation within the repository. While your solution does not need to be fully production ready, you are being evaluated so put your best foot forward!

**I have questions about the problem statement.**

For any requirements not specified above, use your best judgement to determine expected result. You can elaborate on your decisions via the documentation you provide in your repo.

**Can I provide a private repository?**

If at all possible, we prefer a public repository because we do not know which engineer will be evaluating your submission. Providing a public repository ensures a speedy review of your submission. If you are still uncomfortable providing a public repository, you can work with your recruiter to provide access to the reviewing engineer.

**How long do I have to complete the exercise?**

There is no time limit for the exercise. Out of respect for your time, we designed this exercise with the intent that it should take you a few hours. But, please take as much time as you need to complete the work.
