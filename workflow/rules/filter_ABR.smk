# Filter sites with allele ABR not matching some assumptions
rule filter_ABR:
    priority: 6
    input:
        "results/ABR_raw/{sample}_ABR.tsv",
    output:
        temp("results/ABR_filtered/{sample}_ABR_filtered.tsv"), 
    threads: resources["filter_ABR"]["cpu_tasks"]
    resources:
        slurm_partition=resources["filter_ABR"]["partition"],
        mem_mb=resources["filter_ABR"]["memory"],
        tasks=resources["filter_ABR"]["tasks"],
        cpus_per_task=resources["filter_ABR"]["cpu_tasks"],
        jobname=resources["filter_ABR"]["jobname"],
    log:
        stdout="logs/filter_ABR_{sample}.stdout", stderr="logs/filter_ABR_{sample}.stderr"
    shell:
        '''
        python workflow/scripts/filter_ABR.py {input} {output} > {log.stdout} 2> {log.stderr}
        ''' 