Author: Louis OLLIVIER (code, prediction), Cintia Gómez-Muñoz (concept and ABR analysis)
Mail: louis.xiv.bis@gmail.com

# Snakemake Workflow: Ploidy Prediction

This repository contains a Snakemake workflow for predicting ploidy levels from allele balance ratio (ABR) data. The workflow processes VCF files, computes ABR values, filters and bins the data, and uses a trained machine learning model to predict ploidy levels for various yeast strains.

Note: the model is trained on *Saccharmocyces cerevisiae* to predict the following classes : 1n-2n_homozygous, 2n_heterozygous, 3n, 4n, 5n. If you want to use it for another organism, you may need to train another model (using the pipeline to generate the ABR dataset for training features). 

## Workflow Overview

The workflow consists of the following main steps:

1. **Get DP and AD Values**: Extracts depth of coverage (DP) and allele depth (AD) values from the VCF file.
2. **Compute ABR**: Computes the allele balance ratio (ABR) for each site.
3. **Filter ABR**: Filters ABR values based on specific criteria.
4. **Bin ABR**: Bins the ABR values for machine learning.
5. **Merge ABR**: Merges the binned ABR values from multiple samples into a single file.
6. **Predict Ploidy**: Uses a trained machine learning model to predict ploidy levels from the binned ABR data.
7. **Plot Histograms**: Generates histograms of the ABR values for visualization.
8. **Predict Ploidy**: Predict the ploidy using the model in **/scripts/model**.


## Usage 
### System requirements

The only requirement is to be on a SLURM HPC cluster (recommended, but local running is possible, commands are also given for that case) and have a working install of [conda](https://www.anaconda.com/download/#linux) and [git](https://git-scm.com/downloads).
All tools necessary to run the pipeline are described in a conda environment file.  

### Initialization
These commands have to be run only once to setup the pipeline.

#### Create the minimal snakemake environment to run jobs
```
conda env create -f workflow/envs/snakemake.yaml -n your_env_name
```

or load Snakemake version 7.32.4 the way you want (**module load** for instance)

#### If SLURM : create your profile 

In order to run the pipeline on SLURM cluster, you need to create a "profile" file contains information about the resources and other snakemake commands. The profile should be in the folllowing folder: $HOME/.config/snakemake/name_of_profile. You can name the profile the way you want but will need to use that name to run the pipeline. More information [here](https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles).  

Now, if you need to run the pipeline on a SLURM based cluster (recommended) or on a local computer, follow the according section.

The file used already exist in the **/config/** directory. 

```
mkdir $HOME/.config/snakemake/name_of_profile
cp workflow/config/slurm.yaml $HOME/.config/snakemake/name_of_profile/config.yaml
```

You can change the profile file according to your preferences. 

### Running the pipeline
The workflow is configured using YAML files located in the **config/** directory. The main configuration file is **config.yaml**, which specifies the input VCF file and the list of samples to process.

Example config/config.yaml:
```
vcf: '/path/to/vcf/samples.vcf.gz'
samples: 
  - PD35A
  - DBVPG1029
  - HN2.2
  # Add more samples as needed
```
If you have a lot of smaples and want to be sure to give the exact same names in the vcf you can get the list this way (and paste it to the config file): 

```
bcftools query -l /path/to/vcf/samples.vcf.gz | sed 's/^/- /' > samples.txt
```

Follow the correct section if you want to run the pipeline on a SLURM HPC cluster (recommended) or on a local computer.   

##### SLURM HPC cluster 

```
nohup snakemake --profile name_of_profile &
```

##### Local computer

```
nohup snakemake --resources mem_mb=64000 --cores 8 &
```

Note: you can change the values for the RAM ad the number of core. You can also create a profile to specify more resources but you'd need to change the script for each rule.

