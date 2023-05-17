# Seed Queries

The python script included in this repo contains the code used to generate the seed queries used in our snowball searches. The seed queries for device detectors are straightforward, as there is a simple list of queries that is always used.
The seed queries for spy devices are slightly more complex. They contain templates such as "{ACTOR}" that can be filled in with multiple possible phrases. As such, the list is constructed by running the program.
One can observe the lists by running the script with python.
