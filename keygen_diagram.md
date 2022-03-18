Explanation of Keygen Algo
```
' ', 50
'e', 49
's', 44
'a', 43

chunks = [
  [' ', 'e'],
  ['s', 'a']
]

chunk_perm = [ 
  [
    [' ', 'e'],
    ['e', ' ']
  ], 
  [
    ['s', 'a'],
    ['a', 's']
  ]
]

# We're "counting", least significant digits change first
chunk_ptrs = [
  0,
  0               # incremement this ptr first, then go down the stack. 
]                 


[
  ' ', 'e', 's', 'a',
  ' ', 'e', 'a', 's',
  'e', ' ', 's', 'a',
  'e', ' ', 'a', 's'
]

```


