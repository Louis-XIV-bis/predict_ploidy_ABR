# Predict the ploidy from the ABR for all samples
rule predict_ploidy:
    priority: 8
    input:
        "results/merged_filtered_binned_ABR.csv",
    output:
        "results/ploidy_strain.csv",
    threads: resources["predict_ploidy"]["cpu_tasks"]
    resources:
        slurm_partition=resources["predict_ploidy"]["partition"],
        mem_mb=resources["predict_ploidy"]["memory"],
        tasks=resources["predict_ploidy"]["tasks"],
        cpus_per_task=resources["predict_ploidy"]["cpu_tasks"],
        jobname=resources["predict_ploidy"]["jobname"],
    log:
        stdout="logs/predict_ploidy.stdout",stderr="logs/predict_ploidy.stderr"
    shell:
        '''
        python workflow/scripts/predict_ploidy.py "{input}" "{output}" > "{log.stdout}" 2> "{log.stderr}"
        ''' 