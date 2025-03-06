# Filter sites with allele ABR not matching some assumptions
rule hist_plot_ABR:
    priority: 6
    input:
        "results/ABR_filtered/{sample}_ABR_filtered.tsv",
    output:
        "results/hist_ABR/{sample}_ABR_filtered_hist.png",
    threads: resources["hist_plot_ABR"]["cpu_tasks"]
    resources:
        slurm_partition=resources["hist_plot_ABR"]["partition"],
        mem_mb=resources["hist_plot_ABR"]["memory"],
        tasks=resources["hist_plot_ABR"]["tasks"],
        cpus_per_task=resources["hist_plot_ABR"]["cpu_tasks"],
        jobname=resources["hist_plot_ABR"]["jobname"],
    log:
        stdout="logs/hist_plot_ABR_{sample}.stdout", stderr="logs/hist_plot_ABR_{sample}.stderr"
    shell:
        '''
        python workflow/scripts/hist_plot_ABR.py {input} {output} > {log.stdout} 2> {log.stderr}
        ''' 