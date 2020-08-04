# Basically what this does is run the attract repel script. You must give the name of a file in the attract-repel/config folder to be able to run this.

config="test1_more.cfg"

config_path="./attract_repel/config/${config}"

python ./attract_repel/code/attract-repel.py $config_path
