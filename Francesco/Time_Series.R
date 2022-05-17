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
library(ggforce)

df <- arrow::read_feather("C:\\Users\\Francesco\\Desktop\\NYCDSA\\CitiBike\\Francesco\\agno.feather")
df2 <- arrow::read_feather("C:\\Users\\Francesco\\Desktop\\NYCDSA\\CitiBike\\Francesco\\test_df.feather")


# subsetting df  e df2 to have start stations and timing
df_start <- df[,c(1,13,7)]
df2_start <- df2[,c(1,4,12)]
colnames(df2_start)[2] <- "start_name"

# merging the two dataframes
df_start <- rbind(df_start, df2_start)

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
options(scipen=999)
plot(myts,
     main = "Time Series of bike rides per month", 
     xlab = "Year", 
     ylab = "Rides")

# Decompose monthly TS
myds_month <- decompose(myts)
options(scipen=999)
plot(myds_month,
     main = "Decomposed monthly Time Series")

# group_by Yearday
Temps_day <- df_start %>% group_by(Yearday) %>% summarise(count = n())

# Ts day
myts <- ts(Temps_day$count, frequency=365, start = c(2018))
options(scipen=999)
plot(myts,
     main = "Time Series of daily bike rides", 
     xlab = "Year", 
     ylab = "Rides")

#Decompose daily TS
myts_day <- decompose(myts)
options(scipen=999)
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

# Magic function for Sarima
my_model <- auto.arima(myts)
my_model

#ARIMA(4,1,1)(0,1,0)[365]
options(scipen=999)
plot.ts(my_model$residuals)

myforecast <- forecast(my_model, level=c(95), h=10*12)

plot(myforecast)

Box.test(my_model$resid, lag=5, type="Ljung-Box")
Box.test(my_model$resid, lag=10, type="Ljung-Box")
Box.test(my_model$resid, lag=15, type="Ljung-Box")
Box.test(my_model$resid, lag=500, type="Ljung-Box")


checkresiduals(myforecast)

accuracy(myforecast)

# Splittin the data in train and test
train <- ts(Temps_day[1:1460,]$count, frequency=365)
test <- ts(Temps_day[1461:1519,]$count, frequency=365, start = end(train))

# Create new model
model_s <- auto.arima(train)
model_s

# Plot new model
fc_s <- forecast(model_s, level=c(40), h=10*12)
options(scipen=999)
autoplot(fc_s)+
  autolayer(test, series="Test Data")  +
  facet_zoom(xlim = c(4.9,5.2))

checkresiduals(fc_s)
accuracy(fc_s)

Box.test(fc_s$resid, lag=5, type="Ljung-Box")
Box.test(fc_s$resid, lag=10, type="Ljung-Box")
Box.test(fc_s$resid, lag=15, type="Ljung-Box")
Box.test(fc_s$resid, lag=500, type="Ljung-Box")

Box.test(fc_s$resid, lag=7, type="Ljung-Box")

# Trying weekly 
Temps_week <- df_start %>% 
    group_by(year = year(start_time), week = week(start_time)) %>% 
    summarise(count = n())

myts <- ts(Temps_week$count, frequency = 52, start = c(2018))
options(scipen=999)
plot(myts,
     main = "Time Series of weekly bike rides", 
     xlab = "Year", 
     ylab = "Rides")

# decompose weekly
myts_week <- decompose(myts)
options(scipen=999)
plot(myts_week)

#Splittin the data in train and test
train <- ts(Temps_week[1:200,]$count, frequency=52)
test <- ts(Temps_week[200:221,]$count, frequency=52, start = end(train))

# Create new model
model_w <- auto.arima(train)
model_w

# Plot new model
fc_w <- forecast(model_w, level=c(40), h=10*2)
options(scipen=999)
autoplot(fc_w)+
  autolayer(test, series="Test Data")  +
  facet_zoom(xlim = c(4.8,5.3))

checkresiduals(fc_w)
accuracy(fc_w)

Box.test(fc_w$resid, lag=5, type="Ljung-Box")
Box.test(fc_w$resid, lag=10, type="Ljung-Box")
Box.test(fc_w$resid, lag=15, type="Ljung-Box")
Box.test(fc_w$resid, lag=40, type="Ljung-Box")

#Decompose daily TS
myts_day <- decompose(myts)
options(scipen=999)
plot(myts_day)



# new approach
df_new <- df[,1]
df2_new <- df2[,1]

df_new <- rbind(df_new, df2_new)

df_start <- mutate(df_new, 
                   Yearweek = paste(year(start_time), 
                                   formatC(month(start_time), 
                                           width = 2, 
                                           flag = "0"),
                                   formatC(week(start_time), 
                                           width = 2, 
                                           flag = "0")))


Temps_week <- df_start %>% group_by(Yearweek) %>% summarise(count = n())

Temps_week <- Temps_week[-1,]

ts_week <- ts(Temps_week$count, frequency=52)

plot(ts_week, 
     main = "Time Series of weekly rides per week", 
     xlab = "Year", 
     ylab = "Rides")

train <- ts(Temps_week[1:200,]$count, frequency=52)
test <- ts(Temps_week[201:261,]$count, frequency=52, start = end(train))


# Create new model
model_s <- auto.arima(train)
model_s

# Plot new model
fc_s <- forecast(model_s, level=c(40), h=10*12)
autoplot(fc_s) +
  autolayer(test, series="Test Data") +
    facet_zoom(xlim = c(4.8,5))

checkresiduals(fc_s)
accuracy(fc_s)

ndiffs(myts)

str(df2)

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
