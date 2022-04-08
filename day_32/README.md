# Messing with TikTok's text to speach

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

---

curl -X POST 'https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/?text_speaker=en_us_001&req_text=beep+boop+i+am+a+robot' | jq -r .data.v_str | base64 -di - > result.mp3 && ffplay -loop 0 result.mp3

### Example 

---

[beep boop](media/result.mp3)
