setwd("C:/Users/20161443/PycharmProjects/pythonProject1")
library(ggplot2)
library(MASS)

data = read.csv('output.csv', header = FALSE, col.names = c("Failure_rates", "Fines"))

demand = read.csv('demand_data.csv', head = FALSE, col.names = c("demand_data"))
demand$ID <- seq.int(nrow(demand))


ggplot(data, aes(x=Failure_rates, y=Fines)) + geom_point() +
  geom_smooth(method = 'lm', formula = y~poly(x,2))+ 
  xlab("Failure rate [1/h]") + ylab("Expected fine (€)") + labs(title = "Expected fine vs. failure rate of gas boilers") +
  theme(plot.title = element_text(hjust = 0.5))
#ggplot(demand, aes(x=ID, y=demand_data)) + geom_point() + xlim(0, 500)

