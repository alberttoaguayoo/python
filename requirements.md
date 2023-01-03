# Barman instalation

* Once Postgres is installed and configured we can use this script to install barman service.

## First you have to create Barman and streaming barman users before run it.

###### Ambos passwords son generados por nosotros, usualmente usamos http://passwordsgenerator.net/ con un password de al menos 50 caracteres.
 ###### psql -c "create user barman with superuser password '{barman_password}';"
 ###### psql -c "create user streaming_barman with REPLICATION password '{streaming_password}';"

## Requirements 
```
 -c Client name.
 -r Absolute postgres path.
 -e External IP.
 -a Barman Address.
 -p Postgres port.
```