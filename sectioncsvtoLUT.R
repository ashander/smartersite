#!/usr/bin/env Rscript
# convert section membership files to two columns
# email id, section
# Usage:
# Rscript sectioncsvtoLUT.R fromfile.xls tofile.csv
args <- commandArgs(TRUE)

tmp <- read.csv(args[1])
t2 <-  tmp$Combined.Scheduled
no.section <- t2 == ""
t3 <- paste(as.character(t2), collapse=" ")
matches <- gregexpr('A[0-9][0-9]' , t3)

tmp2 <- with(tmp, data.frame(id=Student.ID[!no.section], section=unname(regmatches(t3, matches))))
names(tmp2) <- c('id', 'section')
write.csv(tmp2, file=args[2], quote=FALSE, row.names=FALSE)

