# add_pd

This repository adds a point defect as a pseudo-particle into a molecular dynamics run. This is useful when performing dynamics simulations of solids.

To install the library, run:

```sh
pip install git+https://github.com/MUEXLY/add_pd
```

At which point, you can run the command-line interface `add-pd`:

```sh
add-pd input_file output_file defect_type
```

`input_file` specifies the MD run you wish to analyze, `output_file` specifies where you would like the new run to be stored, and `defect_type` specifies the PD type, which is either `V` for vacancies or `I` for self-interstitials. An example run `test.dump.gz` is included, which is an MD run of Fe-7%Cr at 1000 K with a self-interstitial. This can be analyzed with:

```sh
add-pd test.dump.gz new.dump.gz I
```

which will take in the MD run, replace the self-interstitial dumbbell with a pseudo-particle, and output the run data to `new.dump.gz`.
