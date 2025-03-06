# Merge the ABR csv for each samples into a unique one 
rule merge_ABR:
    priority: 8
    input:
        expand("results/ABR_filtered_binned/{sample}_ABR_filtered_binned.csv", sample=SAMPLES),
    output:
        "results/merged_filtered_binned_ABR.csv",
    threads: resources["merge_ABR"]["cpu_tasks"]
    resources:
        slurm_partition=resources["merge_ABR"]["partition"],
        mem_mb=resources["merge_ABR"]["memory"],
        tasks=resources["merge_ABR"]["tasks"],
        cpus_per_task=resources["merge_ABR"]["cpu_tasks"],
        jobname=resources["merge_ABR"]["jobname"],
    log:
        stdout="logs/merge_ABR.stdout",stderr="logs/merge_ABR.stderr"
    shell:
        '''
        python workflow/scripts/merge_ABR.py {input} {output} > {log.stdout} 2> {log.stderr}
        ''' 