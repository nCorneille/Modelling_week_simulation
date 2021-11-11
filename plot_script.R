setwd("C:/Users/20161443/PycharmProjects/pythonProject1")
library(ggplot2)

data = read.csv('output.csv', header = FALSE, col.names = c("Failure_rates", "Fines"))

plot(data$Failure_rates, data$Fines)