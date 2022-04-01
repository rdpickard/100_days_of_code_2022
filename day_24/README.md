# RIPE Atlas DNS results by region

---
```
Language: Python
Brief: Pretty printing DNS measurement results of RIPE Atlas job
Scope: 
Tags: 
State: Completed
Result: Someone did it better
```
---

RIPE's Atlas projects is a great Internet research tool. However the web UI is mostly geared toward displaying timing and pass/fail information. I want the actual DNS records of a DNS measurement. The data is there in the result but it is encoded.

Write a decoder

### Results

---

Someone already did it better

[RIPE Atlas Sagan](https://ripe-atlas-sagan.readthedocs.io/en/latest/) python module

### If I was to do more

---

Don't try to redo the work already done by Sagan.

Use their module to do cluster-ing analysis to get interesting business intelligence. 

For example detecting dynamic or geography based DNS look up responses. Or seeing if it is possible to detect anycast.

### Notes

---

### Example 

---

Chase website uses geography based DNS


```
/Users/pickard/projects/100_days_of_code_2022/local/py3_venv/bin/python /Users/pickard/projects/100_days_of_code_2022/day_24/dnsresultreader.py
JP 202.51.9.120 -> 202.45.161.161
www.chase.com.          3600     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  20       IN     A      159.53.84.126
JP 202.51.9.120 -> 202.51.9.6
www.chase.com.          3600     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  20       IN     A      159.53.113.168
JP 202.51.9.120 -> 202.3.141.3
www.chase.com.          3600     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  20       IN     A      159.53.84.126
FR 37.58.245.110 -> 10.1.10.206
www.chase.com.          131      IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  20       IN     A      159.53.113.168
FR 37.58.245.110 -> 10.1.10.207
www.chase.com.          129      IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  18       IN     A      159.53.113.168
DE 91.96.167.50 -> 8.8.8.8
www.chase.com.          639      IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  6        IN     A      159.53.84.126
RU 213.183.234.53 -> 8.8.8.8
www.chase.com.          1524     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  20       IN     A      159.53.113.168
AT 178.189.219.44 -> None
AT 178.189.219.44 -> 10.0.0.138
www.chase.com.          2911     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  20       IN     A      159.53.116.62
AT 178.189.219.44 -> 10.0.0.138
www.chase.com.          2910     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  19       IN     A      159.53.116.62
FR 194.254.213.197 -> 10.0.160.254
www.chase.com.          1067     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  9        IN     A      159.53.116.62
NZ 60.234.104.69 -> 192.168.1.1
www.chase.com.          3600     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  20       IN     A      159.53.42.11
NZ 60.234.104.69 -> 192.168.1.1
www.chase.com.          3599     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  19       IN     A      159.53.42.11
US 170.39.169.26 -> 192.168.1.1
www.chase.com.          636      IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  2        IN     A      159.53.224.21
US 162.211.36.37 -> 1.1.1.3
www.chase.com.          1433     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  1        IN     A      159.53.44.60
US 162.211.36.37 -> 1.0.0.3
www.chase.com.          1954     IN     CNAME  wwwbcchase.gslb.bankone.com.
wwwbcchase.gslb.bankone.com.  20       IN     A      159.53.116.62

Process finished with exit code 0

```