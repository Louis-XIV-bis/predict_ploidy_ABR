# Store the ABR values into bins and reformat the data to be used for machine learning
rule bin_ABR:
    priority: 6
    input:
        "results/ABR_filtered/{sample}_ABR_filtered.tsv",
    output:
        "results/ABR_filtered_binned/{sample}_ABR_filtered_binned.csv",
    conda:
        "../envs/environment.yaml"
    threads: resources["bin_ABR"]["cpu_tasks"]
    resources:
        slurm_partition=resources["bin_ABR"]["partition"],
        mem_mb=resources["bin_ABR"]["memory"],
        tasks=resources["bin_ABR"]["tasks"],
        cpus_per_task=resources["bin_ABR"]["cpu_tasks"],
        jobname=resources["bin_ABR"]["jobname"],
    log:
        stdout="logs/binned_ABR_{sample}.stdout", stderr="logs/binned_ABR_{sample}.stderr"
    shell:
        '''
        python workflow/scripts/binned_ABR.py "{input}" "{output}" > "{log.stdout}" 2> "{log.stderr}"
        ''' 