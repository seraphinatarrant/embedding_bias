# First we go to the scripts path
cd ./scripts

# Prepare the dataset for the CNN
python ./data_cleaning/hateval_cleaning.py

# Generate the unmodified embeddings
python ./embeddings/generate_embedding.py

# This makes the XWEAT tests and runs the CNN on the unmodified embeddings
bash ./msc_scripts/initial_tests.sh

# This runs attract-repel and then all of the tests. It takes *a lot* of time and you probably shouldn't run all of them at the exact same time
for test in 1 2 6 7 8 9; do
    bash ./msc_scripts/run_attract_repel.sh ${test}
done