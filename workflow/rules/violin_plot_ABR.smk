# Filter sites with allele ABR not matching some assumptions
rule violin_plot_ABR:
    priority: 6
    input:
        "results/ABR_filtered/{sample}_ABR_filtered.tsv",
    output:
        "results/violin_plot_ABR/{sample}_ABR_filtered_violinPlot.png",
    threads: resources["violin_plot_ABR"]["cpu_tasks"]
    resources:
        slurm_partition=resources["violin_plot_ABR"]["partition"],
        mem_mb=resources["violin_plot_ABR"]["memory"],
        tasks=resources["violin_plot_ABR"]["tasks"],
        cpus_per_task=resources["violin_plot_ABR"]["cpu_tasks"],
        jobname=resources["violin_plot_ABR"]["jobname"],
    log:
        stdout="logs/violin_plot_ABR_{sample}.stdout", stderr="logs/violin_plot_ABR_{sample}.stderr"
    shell:
        '''
        python workflow/scripts/violin_plot_ABR.py {input} {output} > {log.stdout} 2> {log.stderr}
        ''' 