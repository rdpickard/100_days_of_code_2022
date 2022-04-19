# ROA lookup tool

---
```
Language: Python
Brief: 
Scope: 
Tags: 
State: 
Result: 
```
---

Look up RPKI status based on a FQDN


### Results

---


### If I was to do more

---

### Notes

---

### Example 

---

```
google.com
	216.58.208.110 => AS15169 216.58.208.0/24 -> ROA valid
	2a00:1450:400e:802::200e => AS15169 2a00:1450:400e::/48 -> ROA valid
sof01s11-in-f110.1e100.net
	216.58.208.110 => AS15169 216.58.208.0/24 -> ROA valid
ams17s08-in-f14.1e100.net
	216.58.208.110 => AS15169 216.58.208.0/24 -> ROA valid
	2a00:1450:400e:80e::e => AS15169 2a00:1450:400e::/48 -> ROA valid
ams16s21-in-x0e.1e100.net
	2a00:1450:400e:802::200e => AS15169 2a00:1450:400e::/48 -> ROA valid
ams15s41-in-x0e.1e100.net
	2a00:1450:400e:802::200e => AS15169 2a00:1450:400e::/48 -> ROA valid
```

```
chase.com
	159.53.44.60 => AS7743 159.53.32.0/19 -> ROA unknown
	159.53.84.126 => AS7743 159.53.64.0/19 -> ROA unknown
	159.53.42.11 => AS7743 159.53.32.0/19 -> ROA unknown
	159.53.224.21 => AS10934 159.53.224.0/21 -> ROA unknown
	159.53.113.168 => AS7743 159.53.96.0/19 -> ROA unknown
	159.53.116.62 => AS7743 159.53.96.0/19 -> ROA unknown
	159.53.85.137 => AS7743 159.53.64.0/19 -> ROA unknown
```

```
twitter.com
	104.244.42.1 => AS13414 104.244.42.0/24 -> ROA valid
	104.244.42.65 => AS13414 104.244.42.0/24 -> ROA valid
```