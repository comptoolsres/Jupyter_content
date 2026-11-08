# install.packages("BiocManager"); BiocManager::install("airway")
library(airway)
library(SummarizedExperiment)
data(airway)

dir.create("data", showWarnings = FALSE)

# Counts: genes x samples
counts <- as.data.frame(assay(airway))
counts <- cbind(gene_id = rownames(counts), counts)
write.csv(counts, "data/airway_counts.csv", row.names = FALSE)

# Sample metadata
samples <- as.data.frame(colData(airway))
samples <- cbind(run_id = rownames(samples), samples)
write.csv(samples[, c("run_id", "SampleName", "cell", "dex")],
          "data/airway_samples.csv", row.names = FALSE)

# Gene annotation (columns available depend on package version)
genes <- as.data.frame(rowData(airway))
genes$gene_id <- rownames(airway)
keep <- intersect(c("gene_id", "gene_name", "gene_biotype",
                    "seq_name", "gene_seq_start", "gene_seq_end"), colnames(genes))
write.csv(genes[, keep], "data/genes.csv", row.names = FALSE)
