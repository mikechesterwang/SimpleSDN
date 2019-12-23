# Computer network project test

### Before test

```bash
vagrant@vagrant:~$ cd sdn-code
vagrant@vagrant:~/sdn-code$ ryu-manager --observe-links shortest_paths.py
```

### Test case 1: single 5

```bash
vagrant@vagrant:~/sdn-code$ sudo python run_mininet.py single 5
```

```
mininet> net
mininet> pingall
mininet> link s1 h1 down //测试switch和host
mininet> pingall
mininet> link s1 h1 up
mininet> pingall
```

![image-20191223153332012](C:\Users\22805\AppData\Roaming\Typora\typora-user-images\image-20191223153332012.png)

### Test case 2: linear 5

```shell
vagrant@vagrant:~/sdn-code$ sudo python run_mininet.py linear 3
```

```
mininet> net
mininet> pingall
mininet> link s2 s3 down //测试switch和swtich
mininet> pingall
mininet> link s2 s3 up
```

![image-20191223153324424](C:\Users\22805\AppData\Roaming\Typora\typora-user-images\image-20191223153324424.png)

### Test case 3: tree 2

```
vagrant@vagrant:~/sdn-code$ sudo python run_mininet.py tree 2
```

```
mininet> net
mininet> pingall
mininet> link s1 s3 down
mininet> h1 ping h2 -c 1
```

![image-20191223153239702](C:\Users\22805\AppData\Roaming\Typora\typora-user-images\image-20191223153239702.png)

### Test case 4: assign1

```
vagrant@vagrant:~/sdn-code$ sudo python run_mininet.py assign1
```

```
mininet> net
mininet> pingall
mininet> link s2 s3 down
mininet> link s5 s3 up //src and dst not connected: s5 s3
mininet> pingall
```

![image-20191223153215845](C:\Users\22805\AppData\Roaming\Typora\typora-user-images\image-20191223153215845.png)

### Test case 5: triangle

```
vagrant@vagrant:~/sdn-code$ sudo python run_mininet.py triangle
```

```
mininet> net
mininet> pingall
mininet> link s1 s3 down
mininet> h1 ping h3 -c 1
mininet> link s2 s3 down
mininet> h1 ping h3 -c 1
mininet> link s1 s3 up
mininet> h1 ping h3 -c 1
```

![image-20191223153205382](C:\Users\22805\AppData\Roaming\Typora\typora-user-images\image-20191223153205382.png)

### Test case 6: mesh 5

```
vagrant@vagrant:~/sdn-code$ sudo python run_mininet.py mesh 5
```

```
mininet> net
mininet> pingall
mininet> link s1 s2 down
mininet> link s1 s4 down
mininet> link s1 s5 down
mininet> link s2 s4 down
mininet> link s2 s5 down
mininet> link s3 s4 down
mininet> pingall
```

![image-20191223153050430](C:\Users\22805\AppData\Roaming\Typora\typora-user-images\image-20191223153050430.png)

### Test case 7: someloops

```
vagrant@vagrant:~/sdn-code$ sudo python run_mininet.py someloops
```

```
mininet> net
mininet> pingall
mininet> link s3 s4 down
mininet> link s4 s6 down
mininet> link s3 s6 down
mininet> pingall
mininet> s4 ping s3 -c 1
```

![image-20191223152744714](C:\Users\22805\AppData\Roaming\Typora\typora-user-images\image-20191223152744714.png)