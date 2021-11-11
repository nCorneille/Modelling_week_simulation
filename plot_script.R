setwd("C:/Users/20161443/PycharmProjects/pythonProject1")
library(ggplot2)
library(MASS)

data = read.csv('output.csv', header = FALSE, col.names = c("Failure_rates", "Fines"))

ggplot(data, aes(x=Failure_rates, y=Fines)) + geom_point() 
