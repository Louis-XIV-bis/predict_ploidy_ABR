# Merge the ABR csv for each samples into a unique one 
rule merge_ABR_csv:
    priority: 8
    input:
        "results/ABR_filtered_binned/{sample}_ABR_filtered_binned.csv", 
    output:
        "results/merged_filtered_binned_ABR.csv",
    threads: resources["merge_ABR_csv"]["cpu_tasks"]
    resources:
        slurm_partition=resources["merge_ABR_csv"]["partition"],
        mem_mb=resources["merge_ABR_csv"]["memory"],
        tasks=resources["merge_ABR_csv"]["tasks"],
        cpus_per_task=resources["merge_ABR_csv"]["cpu_tasks"],
        jobname=resources["merge_ABR_csv"]["jobname"],
    log:
        stderr="logs/merge_ABR_csv.stderr"
    shell:
        '''
        (head -n 1 {input.tsv_files[0]} && tail -n +2 -q {input.tsv_files[1:]}) > {output} 2> {log.stderr}
        ''' 