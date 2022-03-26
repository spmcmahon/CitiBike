library(datasets)
library(forecast)
library(astsa)
library(tsdl)
library(feather)
library(arrow)
library(tidyverse)


df <- arrow::read_feather("C:\\Users\\Francesco\\Desktop\\NYCDSA\\CitiBike\\Francesco\\agno.feather")

str(df)

df %>%
  ggplot(aes(x = month)) +
  geom_bar(color = "darkorchid4") +
  labs(title = "Precipitation - Boulder, Colorado",
       subtitle = "The data frame is sent to the plot using pipes",
       y = "Daily precipitation (inches)",
       x = "Date")

# plot the most used start_station
freq_start <- df %>%
  group_by(start_name, end_name) %>%
  summarise(count = n()) %>%
  top_n(n = 15, wt = count) %>%
  arrange(desc(count))

ggplot(freq_start, aes(x = reorder(start_name, count), y = count)) +
  geom_col() +
  coord_flip() +
  facet(~year, scales = "free")
