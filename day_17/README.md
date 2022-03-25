# Blank README for day

---
```
Language: 
Brief: 
Scope: 
Tags: 
State: 
Result: 
```
---

### Results

---

### If I was to do more

---

### Notes

curl -v -F 'file=@media/dog.jpg' localhost:5000/api/labeled_image/

curl -v -F 'file=@imagenet_classes.json' localhost:5000/api/indexed_label_set/

curl -v localhost:5000/api/indexed_label_sets/

curl -X POST localhost:5000/api/labeled_image/1/labels/imagenet%20classes -H 'Content-Type: application/json' -d '["0", "1", "2"]'


---

### Example 

---