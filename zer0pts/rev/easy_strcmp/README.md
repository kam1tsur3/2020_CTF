# easy strcmp
265pt ?solves

## Challenge
The target of this challenge is to set return value of strcmp to 0 and print "Correct!"
In this binary, strcmp compares argv[1] and some string.
So let's see with ltrace.

```
vagrant@ubuntu-bionic:~/workspace/2020/zer0pts/rev/easy_strcmp$ ltrace ./chall hogehoge
strcmp("hogehoge", "zer0pts{********CENSORED********"...)                                                     = -18
puts("Wrong!"Wrong!
)                                                                                                = 7
+++ exited (status 0) +++
```
Ok, argv[1] is compared to "zer0pts{\*\*\*\*\*\*\*\*CENSORED\*\*\*\*\*\*\*\*}"

```
vagrant@ubuntu-bionic:~/workspace/2020/zer0pts/rev/easy_strcmp$ ltrace ./chall "zer0pts{********CENSORED********}"
strcmp("zer0pts{********CENSORED********"..., "zer0pts{********CENSORED********"...)                          = 190
puts("Wrong!"Wrong!
)                                                                                                = 7
+++ exited (status 0) +++
```
Why dose strcmp return 190?
I can't understand what's happen in the contest term.
So my solution is not smart:-(

But, I have understood that after reading official writeup.

### Solution
I tried setting argv[1] to "zer0pts{a" and saw return value.
```
vagrant@ubuntu-bionic:~/workspace/2020/zer0pts/rev/easy_strcmp$ ltrace ./chall "zer0pts{a"
strcmp("zer0pts{a", "zer0pts{********CENSORED********"...)                                                    = -11
puts("Wrong!"Wrong!
)                                                                                                = 7
+++ exited (status 0) +++
```
Hmm.. Return value is -11.
Next is "zer0pts{b"
```
vagrant@ubuntu-bionic:~/workspace/2020/zer0pts/rev/easy_strcmp$ ltrace ./chall "zer0pts{b"
strcmp("zer0pts{b", "zer0pts{********CENSORED********"...)                                                    = -10
puts("Wrong!"Wrong!
)                                                                                                = 7
+++ exited (status 0) +++
```
Return value is -10.
So first word of flag is "l" ("b"+10).

Like that, I checked all word of flag one by one.

flag: zer0pts{l3ts\_m4k3\_4\_DETOUR\_t0d4y}

## Reference
official writeup: https://hackmd.io/@theoldmoon0602/HJlUflfHI
