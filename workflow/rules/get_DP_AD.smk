# Query for both AD (Allele Depth) and DP (Depth of Coverage) for the specified sample in the vcf
rule get_DP_AD:
    priority: 4
    input:
        VCF,
    output:
        temp("results/DP_AD_raw/{sample}_DP_AD.txt"),
    conda:
        "../envs/bcftools_gzip.yaml"
    threads: resources["get_DP_AD"]["cpu_tasks"]
    resources:
        slurm_partition=resources["get_DP_AD"]["partition"],
        mem_mb=resources["get_DP_AD"]["memory"],
        tasks=resources["get_DP_AD"]["tasks"],
        cpus_per_task=resources["get_DP_AD"]["cpu_tasks"],
        jobname=resources["get_DP_AD"]["jobname"],
    log:
        stderr="logs/get_DP_AD_{sample}.stderr"
    shell:
        '''
        echo -e "CHROM\tPOS\tREF\tALT\tDP\tAD" > "{output}"
        bcftools query -f "%CHROM\t%POS\t%REF\t%ALT[\t%DP\t%AD]\n" -s "{wildcards.sample}" "{input}" >> "{output}" 2> "{log.stderr}"
        ''' 
