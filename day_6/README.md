# Generate image of daily commit streak on repo
---
```
Language: Python
Brief: Create a jpg that shows the max consecutive days main has been commited to 
Scope: silly
Tags: image, git
State: basic funcionality 
Result: success
```
---

I was thinking it would be nice to have a little encouragement to keep the streak going for 100_days_of_code by showing the max current streak.

Don't break the chain!

### Results

Works, but pretty basic

### Notes
Creating the image requires a third party program "wkhtmltopdf". This is a dependency of imgkit.

### If I was to do more
- Do some more fancy formatting to make the image look more interesting.
- Add a script for something like a pre-commit hook to update the image automatically