## Correlation and Linear Regression Results

> glimpse(night_use)
Rows: 1,253
Columns: 13
$ type               <fct> mini-grid, mini-grid, mini-grid, mini-grid, mini-gr…
$ date_commissioned  <date> 2019-10-25, 2019-10-25, 2019-10-25, 2019-10-25, 20…
$ site_name          <chr> "Bandajuma Sowa", "Bandajuma Sowa", "Bandajuma Sowa…
$ id                 <fct> 181, 181, 181, 181, 181, 181, 181, 181, 181, 181, 1…
$ image_date         <date> 2019-10-01, 2019-11-01, 2019-12-01, 2020-01-01, 20…
$ image_value        <dbl> 0.50221395, 0.26047586, 0.21122119, 0.01436514, 0.3…
$ group              <dbl> 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70,…
$ time_period        <dbl> 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82,…
$ total_consumption  <dbl> 256.4149, 1203.2394, 1426.7584, 1376.2992, 1490.561…
$ num_customers      <dbl> 161, 161, 161, 161, 161, 161, 161, 161, 161, 161, 1…
$ total_revenue      <dbl> 121.7981, 883.9337, 904.6175, 1037.1945, 1138.5623,…
$ total_transactions <dbl> 113, 917, 980, 1019, 1098, 1316, 1021, 1073, 890, 8…
$ acpu               <dbl> 1.592639, 7.473537, 8.861853, 8.548443, 9.258146, 1…
> 

> # calculate correlation between nighttime brightness and total consumption
> cor(night_use$total_consumption, night_use$image_value)
[1] 0.2641349
> cor(night_use$acpu, night_use$image_value)
[1] 0.1259514
> cor(night_use$total_revenue, night_use$image_value)
[1] 0.2384718
> cor(night_use$total_transactions, night_use$image_value)
[1] 0.2316903
> cor(night_use$num_customers, night_use$image_value)
[1] 0.2662184
> 


## Linear Regression Results

> use.lm <- lm(night_use$image_value ~ night_use$total_consumption)
> summary(use.lm)

Call:
lm(formula = night_use$image_value ~ night_use$total_consumption)

Residuals:
    Min      1Q  Median      3Q     Max 
-0.3769 -0.0805 -0.0155  0.0573  4.1988 

Coefficients:
                             Estimate Std. Error t value Pr(>|t|)    
(Intercept)                 3.260e-01  6.992e-03  46.626   <2e-16 ***
night_use$total_consumption 2.111e-05  2.179e-06   9.686   <2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 0.1982 on 1251 degrees of freedom
Multiple R-squared:  0.06977,   Adjusted R-squared:  0.06902 
F-statistic: 93.82 on 1 and 1251 DF,  p-value: < 2.2e-16

> acpu.lm <- lm(night_use$image_value ~ night_use$acpu)
> summary(acpu.lm)

Call:
lm(formula = night_use$image_value ~ night_use$acpu)

Residuals:
    Min      1Q  Median      3Q     Max 
-0.3625 -0.0872 -0.0191  0.0594  4.1846 

Coefficients:
               Estimate Std. Error t value Pr(>|t|)    
(Intercept)    0.318853   0.012090  26.373  < 2e-16 ***
night_use$acpu 0.006362   0.001417   4.491 7.76e-06 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 0.2038 on 1251 degrees of freedom
Multiple R-squared:  0.01586,   Adjusted R-squared:  0.01508 
F-statistic: 20.17 on 1 and 1251 DF,  p-value: 7.758e-06

> rev.lm <- lm(night_use$image_value ~ night_use$total_revenue)
> summary(rev.lm)

Call:
lm(formula = night_use$image_value ~ night_use$total_revenue)

Residuals:
    Min      1Q  Median      3Q     Max 
-0.4058 -0.0839 -0.0159  0.0572  4.1911 

Coefficients:
                         Estimate Std. Error t value Pr(>|t|)    
(Intercept)             3.275e-01  7.211e-03  45.422   <2e-16 ***
night_use$total_revenue 3.945e-05  4.542e-06   8.685   <2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 0.1995 on 1251 degrees of freedom
Multiple R-squared:  0.05687,   Adjusted R-squared:  0.05611 
F-statistic: 75.43 on 1 and 1251 DF,  p-value: < 2.2e-16

> cust.lm <- lm(night_use$image_value ~ night_use$num_customers)
> summary(cust.lm)

Call:
lm(formula = night_use$image_value ~ night_use$num_customers)

Residuals:
    Min      1Q  Median      3Q     Max 
-0.4785 -0.0838 -0.0146  0.0598  4.2015 

Coefficients:
                         Estimate Std. Error t value Pr(>|t|)    
(Intercept)             3.133e-01  7.815e-03  40.086   <2e-16 ***
night_use$num_customers 2.200e-04  2.252e-05   9.769   <2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 0.1981 on 1251 degrees of freedom
Multiple R-squared:  0.07087,   Adjusted R-squared:  0.07013 
F-statistic: 95.42 on 1 and 1251 DF,  p-value: < 2.2e-16