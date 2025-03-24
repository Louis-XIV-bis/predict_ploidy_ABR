# Zip the ABR files to store them efficiently
rule zip_ABR:
    priority: 8
    input:
        "results/ABR_raw/{sample}_ABR.tsv",
    output:
        "results/ABR_gz/{sample}_ABR.tsv.gz",
    threads: resources["zip_ABR"]["cpu_tasks"]
    resources:
        slurm_partition=resources["zip_ABR"]["partition"],
        mem_mb=resources["zip_ABR"]["memory"],
        tasks=resources["zip_ABR"]["tasks"],
        cpus_per_task=resources["zip_ABR"]["cpu_tasks"],
        jobname=resources["zip_ABR"]["jobname"],
    log:
        stderr="logs/zip_ABR_{sample}.stderr"
    shell:
        '''
        gzip -c --best "{input}" > "{output}" 2> "{log.stderr}"
        ''' 
