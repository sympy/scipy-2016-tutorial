Partial fraction decomposition
==============================

In [1]: f = 1/(x**2*(x**2 + 1))

In [2]: f
Out[2]:
     1
───────────
 2 ⎛ 2    ⎞
x ⋅⎝x  + 1⎠

In [3]: apart(f)
Out[3]:
    1      1
- ────── + ──
   2        2
  x  + 1   x

In [4]: var('a:d')
Out[4]: (a, b, c, d)

In [5]: p1 = a/x

In [6]: p2 = b/x**2

In [7]: p3 = (c*x + d)/(x**2 + 1)

In [8]: p1, p2, p3
Out[8]:
⎛a  b   c⋅x + d⎞
⎜─, ──, ───────⎟
⎜x   2    2    ⎟
⎝   x    x  + 1⎠

In [9]: sum(_)
Out[9]:
a   b    c⋅x + d
─ + ── + ───────
x    2     2
    x     x  + 1

In [10]: g = _

In [11]: together(g)
Out[11]:
    ⎛ 2    ⎞     ⎛ 2    ⎞    2
a⋅x⋅⎝x  + 1⎠ + b⋅⎝x  + 1⎠ + x ⋅(c⋅x + d)
────────────────────────────────────────
               2 ⎛ 2    ⎞
              x ⋅⎝x  + 1⎠

In [12]: factor(_, x)
Out[12]:
           3            2
a⋅x + b + x ⋅(a + c) + x ⋅(b + d)
─────────────────────────────────
            2 ⎛ 2    ⎞
           x ⋅⎝x  + 1⎠

In [13]: _, f
Out[13]:
⎛           3            2                     ⎞
⎜a⋅x + b + x ⋅(a + c) + x ⋅(b + d)       1     ⎟
⎜─────────────────────────────────, ───────────⎟
⎜            2 ⎛ 2    ⎞              2 ⎛ 2    ⎞⎟
⎝           x ⋅⎝x  + 1⎠             x ⋅⎝x  + 1⎠⎠

In [14]: map(numer, _)
Out[14]:
⎡           3            2           ⎤
⎣a⋅x + b + x ⋅(a + c) + x ⋅(b + d), 1⎦

In [15]: p, q = [ Poly(h, x) for h in _ ]

In [16]: p
Out[16]: Poly((a + c)*x**3 + (b + d)*x**2 + a*x + b, x, domain='ZZ[a,b,c,d]')

In [17]: q
Out[17]: Poly(1, x, domain='ZZ')

In [18]: [ Eq(p.nth(i), q.nth(i)) for i in xrange(0, 4) ]
Out[18]: [b = 1, a = 0, b + d = 0, a + c = 0]

In [19]: solve(_)
Out[19]: {a: 0, b: 1, c: 0, d: -1}

In [20]: g.subs(_)
Out[20]:
    1      1
- ────── + ──
   2        2
  x  + 1   x

In [21]: Eq(Symbol('apart')(f), _)
Out[21]:
     ⎛     1     ⎞       1      1
apart⎜───────────⎟ = - ────── + ──
     ⎜ 2 ⎛ 2    ⎞⎟      2        2
     ⎝x ⋅⎝x  + 1⎠⎠     x  + 1   x

In [22]: together(_20) == f
Out[22]: True

Deriving trigonometric identities
=================================

http://www.mathpages.com/home/kmath205.htm

In [1]: var('a,b')
Out[1]: (a, b)

In [2]: sin(a + b).series(b, 0, 10).collect([sin(a), cos(a)])
Out[2]:
⎛     2    4     6      8            ⎞          ⎛     3     5     7       9             ⎞
⎜    b    b     b      b             ⎟          ⎜    b     b     b       b              ⎟
⎜1 - ── + ── - ─── + ───── + O(b**10)⎟⋅sin(a) + ⎜b - ── + ─── - ──── + ────── + O(b**10)⎟⋅cos(a)
⎝    2    24   720   40320           ⎠          ⎝    6    120   5040   362880           ⎠

In [3]: sin(b).series(b, 0, 10)
Out[3]:
     3     5     7       9
    b     b     b       b
b - ── + ─── - ──── + ────── + O(b**10)
    6    120   5040   362880

In [4]: cos(b).series(b, 0, 10)
Out[4]:
     2    4     6      8
    b    b     b      b
1 - ── + ── - ─── + ───── + O(b**10)
    2    24   720   40320

In [5]: _2.subs({_3: sin(b), _4: cos(b)})
Out[5]: sin(a)⋅cos(b) + sin(b)⋅cos(a)

In [6]: Eq(sin(a + b), _)
Out[6]: sin(a + b) = sin(a)⋅cos(b) + sin(b)⋅cos(a)

In [7]: cos(a + b).series(b, 0, 10).collect([sin(a), cos(a)])
Out[7]:
⎛     2    4     6      8            ⎞          ⎛      3     5     7       9             ⎞
⎜    b    b     b      b             ⎟          ⎜     b     b     b       b              ⎟
⎜1 - ── + ── - ─── + ───── + O(b**10)⎟⋅cos(a) + ⎜-b + ── - ─── + ──── - ────── + O(b**10)⎟⋅sin(a)
⎝    2    24   720   40320           ⎠          ⎝     6    120   5040   362880           ⎠

In [8]: _7.subs({_3: sin(b), _4: cos(b)})
Out[8]: -sin(a)⋅sin(b) + cos(a)⋅cos(b)

In [9]: Eq(cos(a + b), _)
Out[9]: cos(a + b) = -sin(a)⋅sin(b) + cos(a)⋅cos(b)

In [10]: sin(a + b).expand(trig=True)
Out[10]: sin(a)⋅cos(b) + sin(b)⋅cos(a)

In [11]: cos(a + b).expand(trig=True)
Out[11]: -sin(a)⋅sin(b) + cos(a)⋅cos(b)

Numerical computing
===================

f = x**(1 - log(log(log(log(1/x)))))

limit(f, x, 0)

Issues with floating point numbers
----------------------------------

http://www.cybertester.com/data/gruntz.pdf

In [18]: 10**-10**1
Out[18]: 1e-10

In [19]: 10**-10**2
Out[19]: 1e-100

In [20]: 10**-10**3
Out[20]: 0.0

In [51]: f = x**(1 - log(log(log(log(1/x)))))

In [52]: f
Out[52]:
      ⎛   ⎛   ⎛   ⎛1⎞⎞⎞⎞
 - log⎜log⎜log⎜log⎜─⎟⎟⎟⎟ + 1
      ⎝   ⎝   ⎝   ⎝x⎠⎠⎠⎠
x

In [29]: f.subs(x, S(10)**-10**1)
Out[29]:
           -1 + log(log(log(10⋅log(10))))
10000000000

In [30]: f.subs(x, S(10)**-10**1).evalf()
Out[30]: 2.17686941815359e-9

In [31]: f.subs(x, S(10)**-10**2).evalf()
Out[31]: 4.87036575966820e-48

In [32]: f.subs(x, S(10)**-10**3).evalf()
Out[32]: 1.56972853078733e-284

In [33]: f.subs(x, S(10)**-10**4).evalf()
Out[33]: 3.42160969045651e-1641

In [34]: f.subs(x, S(10)**-10**5).evalf()
Out[34]: 1.06692865268558e-7836

In [35]: f.subs(x, S(10)**-10**6).evalf()
Out[35]: 4.40959214112950e-12540

In [35]: f.subs(x, S(10)**-10**7).evalf()
<timeout>

In [38]: f.subs(x, Float(10.0)**-10**6)
Out[38]: 4.40959214078817e-12540

In [39]: f.subs(x, Float(10.0)**-10**7)
Out[39]: 1.11148303902275e+404157

In [40]: F = lambdify(x, f, modules='mpmath')

In [41]: from sympy.mpmath import mpf

In [42]: F(mpf("1e-10"))
Out[43]: 2.17686941815358e-9

In [44]: F(mpf("1e-100"))
Out[44]: 4.87036575966825e-48

In [45]: F(mpf("1e-1000"))
Out[45]: 1.56972853078736e-284

In [46]: F(mpf("1e-10000"))
Out[46]: 3.42160969046405e-1641

In [47]: F(mpf("1e-100000"))
Out[47]: 1.0669286527192e-7836

In [48]: F(mpf("1e-1000000"))
Out[48]: 4.40959214078817e-12540

In [49]: F(mpf("1e-10000000"))
Out[49]: 1.11148303902275e+404157

In [54]: from sympy.mpmath import limit as mplimit

In [57]: mplimit(F, 0)
Out[57]: (2.23372778188847e-5 + 2.28936592344331e-8j)

In [58]: mplimit(F, 0, exp=True)
Out[58]: (3.43571317799366e-20 + 4.71360839667667e-23j)

In [62]: limit(f, x, 0)
Out[62]: ∞
