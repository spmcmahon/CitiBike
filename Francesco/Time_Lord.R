library(forecast)
library(astsa)
library(tsdl)
library(feather)
library(arrow)
library(tidyverse)
library(ggpubr)
library(TSstudio)
library(timetk)
library(lubridate)
library(fUnitRoots)

df <- arrow::read_feather("C:\\Users\\Francesco\\Desktop\\NYCDSA\\CitiBike\\Francesco\\agno.feather")

str(df)

# frequence of start_station pre_covid
freq_start_pre_covid <- df %>%
  filter(year < 2020) %>%
  group_by(start_name) %>%
  summarise(count = n()) %>%
  top_n(n = 15, wt = count) %>%
  arrange(desc(count))

# frequence of start_station post_covid
freq_start_post_covid <- df %>%
  filter(year > 2019) %>%
  group_by(start_name) %>%
  summarise(count = n()) %>%
  top_n(n = 15, wt = count) %>%
  arrange(desc(count))

# frequence of end_station pre_covid
freq_end_pre_covid <- df %>%
  filter(year < 2020) %>%
  group_by(end_name) %>%
  summarise(count = n()) %>%
  top_n(n = 15, wt = count) %>%
  arrange(desc(count))

# frequence of end_station post_covid
freq_end_post_covid <- df %>%
  filter(year > 2019) %>%
  group_by(end_name) %>%
  summarise(count = n()) %>%
  top_n(n = 15, wt = count) %>%
  arrange(desc(count))

# plot 4 graphs


a <- ggplot(freq_start_pre_covid, 
            aes(x = reorder(start_name, count), 
                y = count,
                fill = start_name)) +
  geom_col() +
  coord_flip() +
  theme(legend.position="none",
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        plot.title = element_text(size=10, face = "bold", hjust = 0.5)) +
  ggtitle("Start Station pre-Covid")

b <- ggplot(freq_start_post_covid, 
            aes(x = reorder(start_name, count), 
                y = count,
                fill = start_name)) +
  geom_col() +
  coord_flip() +
  theme(legend.position="none",
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        plot.title = element_text(size=10, face = "bold", hjust = 0.5)) +
  ggtitle("Start Station post-Covid")

c <- ggplot(freq_end_pre_covid, 
            aes(x = reorder(end_name, count), 
                y = count,
                fill = end_name)) +
  geom_col() +
  coord_flip() +
  theme(legend.position="none",
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        plot.title = element_text(size=10, face = "bold", hjust = 0.5)) +
  ggtitle("End Station pre-Covid")

d <- ggplot(freq_end_post_covid, 
            aes(x = reorder(end_name, count), 
                y = count,
                fill = end_name)) +
  geom_col() +
  coord_flip() +
  theme(legend.position="none",
        axis.title.x = element_blank(),
        axis.title.y = element_blank(),
        plot.title = element_text(size=10, face = "bold", hjust = 0.5)) +
  ggtitle("End Station post-Covid")

# merge the plots
ggarrange(a, c, b, d,
          ncol = 2, nrow = 2)


# grouping the most frequent routes
routes_freq <- df %>%
  group_by(start_name, end_name) %>%
  summarise(count = n()) %>%
  arrange(desc(count))

str(routes_freq)



# subsetting df to have start stations and timing
df_start <- df[,c(1,13,7,15,12)]

# add a column for rides
df_start$rides <- 1

# Create different columns for different time configurations
# Month
df_start <- mutate(df_start, 
                   MonthYear = paste(year(start_time),
                                               formatC(month(start_time), 
                                                       width = 2, 
                                                       flag = "0")))

# Day of the week
df_start <- mutate(df_start, 
                   Yearday = paste(year(start_time), 
                                   formatC(month(start_time), 
                                           width = 2, 
                                           flag = "0"),
                                                     formatC(day(start_time), 
                                                             width = 2, 
                                                             flag = "0")))
# Hour of the day
df_start <- mutate(df_start, 
                   Dayhour = paste(year(start_time), 
                                   formatC(month(start_time), 
                                           width = 2, 
                                           flag = "0"),
                                                     formatC(day(start_time), 
                                                             width = 2, 
                                                             flag = "0"),
                                                                        formatC(hour(start_time),
                                                                                width = 2,
                                                                                flag = "0")))

# Week of the year
df_start <- mutate(df_start, Week = week(start_time))

# Year
df_start <- mutate(df_start, Year = year(start_time))
df_start$Year <- as.factor(df_start$Year)


# eliminate year 2017
df_start <- subset(df_start, Year != 2017)

# Grou_by year
Temps_year <- df_start %>% group_by(Year) %>% summarise(count = n())

# TS year
myts <- ts(Temps_year$count, frequency=1, start = c(2018))
plot(myts, 
     main = "Time Series of bike rides per year", 
     xlab = "Year", 
     ylab = "Rides")

# group_by Montyear
Temps_month <- df_start %>% group_by(MonthYear) %>% summarise(count = n())

# Ts month
myts <- ts(Temps_month$count, frequency=12, start = c(2018))
plot(myts, 
     main = "Time Series of bike rides per month", 
     xlab = "Year", 
     ylab = "Rides")

# Decompose monthly TS
myds_month <- decompose(myts)
plot(myds_month)

# group_by Yearday
Temps_day <- df_start %>% group_by(Yearday) %>% summarise(count = n())

# Ts day
myts <- ts(Temps_day$count, frequency=365, start = c(2018))
plot(myts, 
     main = "Time Series of daily bike rides", 
     xlab = "Year", 
     ylab = "Rides")

#Decompose daily TS
myts_day <- decompose(myts)
plot(myts_day)

# Unit root test
urkpssTest(myts, type = c("tau"), lags = c("short"),use.lag = NULL, doplot = TRUE)
ndiffs(myts) #1

# Make the TS more stationary
myts2 <- diff(myts)
plot(myts2)
Box.test(myts2, type="Ljung-Box", lag = log(length(myts2)))

# Plot ACF (autocorrelation function) for daily TS
acf(myts2, type = "correlation", main = "ACF for daily rides") #2 significative lags
pacf(myts2, main = "Partial ACF for daily rides") #6

#arima with p=6, d=1, q=2

d=1
for(p in 1:7){
  for(q in 1:3){
    if (p+d+q<=11){
      model <- arima(x=myts, order=c((p-1),d,(q-1)))
      pval<-Box.test(model$residuals, lag=log(length(model$residuals)))
      sse<-sum(model$residuals^2)
      cat(p-1,d,q-1, 'AIC=', model$aic, ' SSE=',sse,' p-VALUE=', pval$p.value,'\n')
    }
  }
}

Bike.arima = arima(x=myts, order = c(6,1,2))

Bike.predict = forecast(Bike.arima, level=c(95), h=10*12)

autoplot(Bike.predict)

# working on SARIMA
myts3 <- diff(myts, 4)
plot(myts3)
acf(myts3, type = "correlation", main = "ACF for daily rides without seasonality") #Q1
pacf(myts3, main = "Partial ACF for daily rides without seasonality") #P5

d = 1
DD = 1
per = 4
for(p in 1:7){
  for(q in 1:3){
    for(p_seasonal in 1:6){
      for(q_seasonal in 1:2){
        if(p+d+q+p_seasonal+DD+q_seasonal<=21){
          model<-arima(x=myts, order = c((p-1),d,(q-1)), seasonal = list(order=c((p_seasonal-1),DD,(q_seasonal-1)), period=per))
          pval<-Box.test(model$residuals, lag=log(length(model$residuals)))
          sse<-sum(model$residuals^2)
          cat(p-1,d,q-1,p_seasonal-1,DD,q_seasonal-1,per, 'AIC=', model$aic, ' SSE=',sse,' p-VALUE=', pval$p.value,'\n')
        }
      }
    }
  }
}

# It will never work
my_model <- auto.arima(myts)
my_model

#ARIMA(4,1,1)(0,1,0)[365]
plot.ts(my_model$residuals)

myforecast <- forecast(my_model, level=c(95), h=10*12)

plot(myforecast)

Box.test(my_model$resid, lag=5, type="Ljung-Box")
Box.test(my_model$resid, lag=10, type="Ljung-Box")
Box.test(my_model$resid, lag=15, type="Ljung-Box")

# Hourly TS
Temps_hour <- df_start %>% group_by(Dayhour) %>% summarise(count = n())

# Ts day
myts <- ts(log(Temps_hour$count), frequency = 8760, start = c(2018))
plot(myts, 
     main = "Time Series of daily bike rides", 
     xlab = "Year", 
     ylab = "Rides")

#Decompose daily TS
myts_day <- decompose(myts)
plot(myts_day)

# Unit root test
urkpssTest(myts, type = c("tau"), lags = c("short"),use.lag = NULL, doplot = TRUE)
ndiffs(myts) #1

# Do the magic again
my_model <- auto.arima(myts)
my_model

#ARIMA(4,1,1)(0,1,0)[365]
plot.ts(my_model$residuals)

myforecast <- forecast(my_model, level=c(95), h=10*12)

plot(myforecast)

Box.test(my_model$resid, lag=5, type="Ljung-Box")
Box.test(my_model$resid, lag=10, type="Ljung-Box")
Box.test(my_model$resid, lag=15, type="Ljung-Box")


# Make the TS more stationary
myts2 <- diff(myts)
plot(myts2)
Box.test(myts2, type="Ljung-Box", lag = log(length(myts2)))

# Plot ACF (autocorrelation function) for daily TS
acf(myts2, type = "correlation", main = "ACF for daily rides") #3 significative lags
pacf(myts2, main = "Partial ACF for daily rides") #5

#arima with p=6, d=1, q=2

d=1
for(p in 1:6){
  for(q in 1:4){
    if (p+d+q<=11){
      model <- arima(x=myts, order=c((p-1),d,(q-1)))
      pval<-Box.test(model$residuals, lag=log(length(model$residuals)))
      sse<-sum(model$residuals^2)
      cat(p-1,d,q-1, 'AIC=', model$aic, ' SSE=',sse,' p-VALUE=', pval$p.value,'\n')
    }
  }
}

Bike.arima = arima(x=myts, order = c(6,1,2))

Bike.predict = forecast(Bike.arima, h=12, level=80)

autoplot(Bike.predict)
