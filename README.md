
## Apps

**Apps** is a framework for creating applications from template PBS scripts and simplifying job submission.
A template PBS script is provided with arguments to specify at submission time, such as input files and output directories.
The template PBS script works much like a normal PBS script with the added functionality of the arguments.
The input arguments may also be used to specify job resources such as number of nodes and wall time.

At the time an app is created, a developer may specify default rules for arguments.
These rules may either be default value or a command using other input arguments, such as number of nodes based on the number of lines in an input list file.
From these rules, a dependency graph is generated and solved, and a prompt order is created for the application.
When a job is submitted, users will be prompted to accept a default value or to supply their own for each argument to the PBS script.

### [Go to Wiki](https://github.com/dgravesa/PBS-Apps/wiki)
