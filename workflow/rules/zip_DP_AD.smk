# Zip the DP_AD files to store them efficiently
rule zip_DP_AD:
    priority: 8
    input:
        "results/DP_AD_raw/{sample}_DP_AD.txt",
    output:
        "results/DP_AD_gz/{sample}_DP_AD.txt.gz",
    threads: resources["zip_DP_AD"]["cpu_tasks"]
    resources:
        slurm_partition=resources["zip_DP_AD"]["partition"],
        mem_mb=resources["zip_DP_AD"]["memory"],
        tasks=resources["zip_DP_AD"]["tasks"],
        cpus_per_task=resources["zip_DP_AD"]["cpu_tasks"],
        jobname=resources["zip_DP_AD"]["jobname"],
    log:
        stderr="logs/zip_DP_AD_{sample}.stderr"
    shell:
        '''
        gzip -c --best {input} > {output} 2> {log.stderr}
        ''' 
