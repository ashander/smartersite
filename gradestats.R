#!/usr/bin/env Rscript
# given one csvs like grades.csv output stats
# Usage:
# Rscript gradestats.R grades.csv
args <- commandArgs(TRUE)
if (length(args) != 1)
    print("Usage: Rscript gradestats.R [grades.csv]")

    
c1 <- read.csv(args[1],skip=2, fill=TRUE)

print(summary(c1$grade))

    

                    

