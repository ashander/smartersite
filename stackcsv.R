#!/usr/bin/env Rscript
# given two csvs like grades.csv, stack them to a single csv
# Usage:
# Rscript stackcsv.R in1.csv in2.csv out.csv
args <- commandArgs(TRUE)
if (length(args) != 3)
    print("Usage: Rscript stackcsv.R in1.csv in2.csv out.csv")
for(a in args){
    if(a == 'd.csv')
        print("illegal filename! use something not called d.csv")
}

    
c1 <- read.csv(args[1],skip=2, fill=TRUE)
c2 <- read.csv(args[2],skip=2, fill=TRUE)

out <- rbind(c1, c2)

write.csv(out, 'd.csv', row.names=FALSE, quote=FALSE)
    
system(paste0('head -2 ', args[1], ' >', args[3]))
system(paste0('cat d.csv >>', args[3]))
                    

