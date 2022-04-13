# Bit length calculator

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
Was thinking about calculating how many bits it takes to represent an arbitrarily long number

### Results

---
Works.

### If I was to do more

---

Write up an equivalent of the code in Go and Rust to compare run time

### Notes

---

### Example 

---

number:bit width:time for Python3 on a moderately busy M1
```
7251103051815614857:63:0.582232333
5834348426395082392:63:0.582147583
8963214206934129312:63:0.5824291250000002
4306309840715227913:62:0.5851429170000002
7730645163702964161:63:0.5813006669999998
6840180127925227182:63:0.4958658340000004
1668064423694138980:61:0.5881544170000002
3266520495260367012:62:0.5916557090000003
9193775187411747202:63:0.6392096249999994
667670391161875084:60:0.5520292499999995
7131988338883722701:63:0.5053569169999994
1969258594125369288:61:0.589058208
3366109483748519269:62:0.5580494590000011
6557549738944826072:63:0.6684417499999995
3548318780848733044:62:0.5915307500000004
7077132411081855453:63:0.7231471660000004
1854436986735964093:61:0.5186632499999995
7324878640752335317:63:0.5925410840000005
6444669821942374901:63:0.7043145829999986
6506783597746741148:63:0.5980324170000006
2278544777665574979:61:0.5994887500000008
2859820277093088990:62:0.7208802080000005
7241593383069686699:63:0.6704869999999996
4376269849123444525:62:0.5975893330000002
9164943253202789278:63:0.5852693339999995
6908007144470676043:63:0.6587795829999994
7315053084345163803:63:0.6805170420000017
3854764934761266260:62:0.589384625000001
5561986206105940053:63:0.5788918750000001
4868264298172635474:63:0.5771507919999976
1724765901426262189:61:0.752086042000002
2467914739663110357:62:0.6757260840000008
1920182883543367132:61:0.5905259160000007
1583912974387338542:61:0.6015289159999995
3966593501258733359:62:0.7242057919999993
781318406958500205:60:0.48645212499999957
1231522947205775126:61:0.5976077079999982
4932466319765025187:63:0.6242566670000009
6465489089820805522:63:0.5812447079999998
7518555142201427333:63:0.6005054580000007
4053480804243699405:62:0.6091954999999984
6158247621681094308:63:0.6027607089999982
8945889932844524192:63:0.5882345829999984
5498216707841173295:63:0.5944732080000001
5052965500594456137:63:0.6453172500000015
4953937210483331564:63:0.5013514579999985
7412550995080010277:63:0.5064983749999996
1101902284719212441:60:0.6047441249999999
6508190941402152266:63:0.6077855409999984
2812717848085400613:62:0.6856321669999978
9037425302783198776:63:0.5839289170000015
8943586283499888090:63:0.6628147090000027
2249735581665207238:61:0.6072410830000052
1795724886166151194:61:0.676778082999995
8205152436673059353:63:0.5858337079999956
8663539819081228529:63:0.5833712080000026
1190290941917382795:61:0.5909155829999975
9210581234058525586:63:0.5546771670000012
5912971032370080030:63:0.7291407920000026
8505193573910934662:63:0.5900954170000006
5950575029914043750:63:0.6288188329999969
7261741329628165366:63:0.5815467089999942
5734956506516003688:63:0.5790442500000026
430930939928768635:59:0.5531273750000025
5176605695124581704:63:0.7333485410000051
4702752776169793038:63:0.623221375
8814776521614656777:63:0.5832221249999989
5843968866609002414:63:0.5059746670000038
83783186203161820:57:0.5532550420000035
3397087516671471412:62:0.5924945000000008
2921319031851881375:62:0.5924822919999997
6632291642301276069:63:0.5807100410000032
5408589343007573355:63:0.5959957079999967
8922836484227712079:63:0.5830833340000012
4844319295720335491:63:0.6296788339999964
1062634676561806745:60:0.5790230419999958
37291767319197743:56:0.6501786249999952
7573040013474001793:63:0.6445371670000029
1021961919572212819:60:0.5786147499999998
8640731505931299572:63:0.6091126660000015
7126517178160400891:63:0.6284174999999976
3967940445689908158:62:0.5946908330000014
6047664536885319156:63:0.4998499159999952
2698718563907668724:62:0.6700160830000002
8321159187240931733:63:0.5878547079999947
7383481483348791241:63:0.5020877919999975
7957432132102582297:63:0.6608827079999955
4758030700444838492:63:0.5776287910000022
8980653339984511848:63:0.5826372920000011
1035130392558547767:60:0.5525814579999988
2586917895839253692:62:0.583699916999997
7924067713865873922:63:0.6602832499999991
1011868007359103566:60:0.5529099170000009
1488629910427233594:61:0.5982806669999974
264472996765007176:58:0.6411297500000046
6839733593112115741:63:0.5847322920000053
6237740311834791034:63:0.6749160829999994
5556436250112302930:63:0.6327260420000016
8621803963462184071:63:0.5855540829999981
```


huh.
Doing v|= v>>pow(2,i) took two to three times longer
```
618970019642690137449562111:89:0.44211545799999996
5155375251291210138:63:1.153074084
1004021553796860112:60:1.2886049579999999
3664285700384583451:62:1.1181467499999997
8190527482028829339:63:1.1049061670000002
9002708835595956373:63:1.3554552919999994
6120573354346672745:63:1.1030303749999995
8403321847094337157:63:1.1056480000000004
4086823900933712944:62:1.1048822919999992
243693639251634447:58:1.085901959000001
8564825731181210611:63:0.8624227500000003
5856135973937453277:63:1.1292550830000003
2891564740760455766:62:1.1352829999999994
8658783956603659304:63:1.1201293329999995
2258421025011018431:61:1.1026791249999999
7465396373339522866:63:0.899423500000001
7464021501395507997:63:1.3388426250000016
2949725246044627153:62:1.0976630830000005
6027352587082776600:63:1.356872458999998
796254281595711657:60:1.072415834000001
3140986060982400040:62:1.1062710829999993
532518738997990250:59:1.295500624999999
3311750851058184025:62:0.8657460000000015
3845613225296471032:62:1.0210010830000016
6279975059495130545:63:1.1991465829999974
2821750442497408800:62:1.16018725
8517395249459153334:63:0.8571137909999997
4524347725648308442:62:0.8623615420000021
7133452380798318389:63:0.8667967500000024
2525538605934957622:62:1.104397875
4294649143550702411:62:0.8718765830000024
7241351021888570938:63:1.1087122499999964
1754582140265273965:61:1.1265898330000041
6017094412316054236:63:1.1247629580000051
2399874746855438327:62:1.1310086249999998
420577306379068668:59:1.0757634169999974
4337133298136066761:62:1.112236916999997
5783522459087660578:63:1.1179970829999988
8601605986573394265:63:1.1176822500000014
1930619805291373212:61:1.1131880830000043
3169009571107253546:62:0.8717421250000044
1199967919262352970:61:1.144508375000001
2923077357977085303:62:1.104416332999996
6006205242595933394:63:1.148331333999998
4538670512167026802:62:1.3573461670000029
6198789563296473250:63:1.1691222919999973
1720999549125303340:61:1.3881735000000006
2104764719274893338:61:1.4195127090000028
5590781515294414206:63:0.8620376670000027
2646736724310029269:62:1.1087000829999951
6767277241220289307:63:1.1232168750000042
4498505681765101674:62:1.1291793330000033
3845985837891257684:62:1.133923208000006
2897525329789181795:62:1.1217920420000027
5391641897176092787:63:1.1937918749999952
4349337846138308160:62:1.127189707999996
9024757461156358641:63:1.3841698330000014
6214649439237910178:63:1.143665458000001
195419948387891024:58:1.1916226249999937
1759493344639610171:61:1.3161117500000046
5712445081781516869:63:1.1251362089999901
6616724286030250389:63:1.1122562089999946
439240702065159723:59:1.0923445829999991
4060290377902805447:62:1.1188762499999996
5902896608046278175:63:1.189775124999997
6351320793774365211:63:1.1875366670000034
4836020703765474809:63:1.3828977080000016
6261765232104626332:63:1.1388719159999994
2926189623105010301:62:0.8827278750000005
7374324646499370888:63:1.3832236249999994
5089892495092678142:63:1.1791582499999862
7874379493910299903:63:0.8675125000000037
4708400885640697574:63:1.1390872500000029
6768914732926294858:63:1.3614386250000052
7719041116556775408:63:1.3580920419999956
3053712038386188823:62:1.2238813329999942
3358381452905919261:62:1.1345135419999934
2089679384682479870:61:1.3524226670000132
2235967945600531362:61:1.1124047919999924
5755377930209099905:63:1.1219634589999998
8849996364693659018:63:1.1330896249999967
2026963508520501750:61:1.1444387079999956
9169333427932301268:63:1.3601731660000098
8694965067502650608:63:1.1221620419999994
6947565805967739671:63:1.1458706250000006
217674838396959768:58:1.089402750000005
5502932367543115009:63:1.1125428330000062
6156771413898246452:63:1.1290227089999973
2799482697934877050:62:1.1179160829999972
8321967081327706031:63:1.373723916000003
7240223594032906081:63:1.1410653749999966
5768437871723711505:63:1.3515101670000007
2678244709936056267:62:1.116956708999993
5356785414977989734:63:1.1872875409999892
7144447755206009702:63:1.3564687499999906
7568753751837929793:63:1.1237555830000048
9106729720270583053:63:1.1336705840000008
9183247954551228046:63:1.119098957999995
4359132542526386243:62:1.1190688749999964
3396287219838626303:62:1.110348000000002
```