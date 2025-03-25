# Compute allele balance ratio (ABR) for each sites in the file
rule compute_ABR:
    priority: 6
    input:
        "results/DP_AD_raw/{sample}_DP_AD.txt",
    output:
        temp("results/ABR_raw/{sample}_ABR.tsv"),
    conda:
        "../envs/python.yaml"
    threads: resources["compute_ABR"]["cpu_tasks"]
    resources:
        slurm_partition=resources["compute_ABR"]["partition"],
        mem_mb=resources["compute_ABR"]["memory"],
        tasks=resources["compute_ABR"]["tasks"],
        cpus_per_task=resources["compute_ABR"]["cpu_tasks"],
        jobname=resources["compute_ABR"]["jobname"],
    log:
        stdout="logs/compute_ABR_{sample}.stdout", stderr="logs/compute_ABR_{sample}.stderr"
    shell:
        '''
        python workflow/scripts/compute_ABR.py "{input}" "{output}" > "{log.stdout}" 2> "{log.stderr}"
        ''' 
