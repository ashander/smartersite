#!/usr/bin/env Rscript
# convert xls files as provided by smartsite for class rosters or section memberships
# Usage:
# Rscript xlstocsv.R fromfile.xls tofile.csv
args <- commandArgs(TRUE)

library(xlsx)
tmp <- read.xlsx(args[1], sheetName='Sheet0')
write.csv(tmp, file=args[2], quote=FALSE)
