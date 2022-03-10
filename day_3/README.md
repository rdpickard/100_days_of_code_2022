# File joiner

---
```
Language: Go
Brief: Join files together where they overlap 
Scope: experiment
Tags: first time language
State: finished
Result: ugly but works
```
---

I've occasionally accumulated text files with contents of the output of some process. Before the terminal buffer wraps I'll copy everything on screen into the clipboard and then copy it into a file. Hoping not to lose any output. If I haven't missed any output the files with the pasted data will have a lot of overlapping content.

I wanted to have a script that will join these files together but not include overlapping content.

Seemed like a reasonable task for my first Go program.

### Results 
 
Code is god awful and ugly. Fine with chalking that up to first time using the code. 

For basic test it works

```
(base) [pickard@eris.local:] projects/100_days_of_code_2022/day_3 [main] MM?? % go run file_joiner.go output.txt test_files/small_*

(***snipped output of my ugly baby***)

(base) [pickard@eris.local:] projects/100_days_of_code_2022/day_3 [main] MM?? % diff output.txt test_files/big_sample_from_top.txt


```
This is the expected output. The test files `small_*` are chopped up pieces of `test_files/big_sample_from_top.txt`. Diff'ing the `output .txt`
shows the file_joiner program rememberable the pieces and stipped out overlaps.

### If I was to do more

Nuke and start again. The idea is sound and I think has some value. But the code is gnarly because I was basically building the tracks in front of the train. I don't have a good sense of how to structure go programs yet.

More go in the future though.