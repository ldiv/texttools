
## Texttools

A convenience program to run operations on text.  Run with help option (-h or --help) to list available operations.

Run by calling the module with the '-m' flag.
```
$> echo "hello" | python -m texttools "title_case"
$> Hello
```

Input and output are stdin and sdtout by default, otherwise pass file arguments
```
$> echo "hello" > myfilein
$> python -m texttools myfilein myfileout "title_case"
$> cat myfileout
$> Hello
```

Operations, internally referred to as transforms, are passed to the program as a command.

A command is a series of one or more chained operations.  The '->' characters are used as the chain operator.

`operation1->operation2->operationN...`

Arguments can be passed to the operations enclosed in parenthesis.  If no arguments are passed the parenthesis are optional.

```
$> echo " Ok " | python -m texttools "reverse"
$>  kO
$ echo " Ok " | python -m texttools "reverse()"
$>  kO
```

Most operations operate on characters by default and can operate on words by passing the `operate_on_word` argument or `w` as shortcut
```
$ echo " now what " | python -m texttools "reverse(operate_on_word=True)->trim()"
$> what now 
```
Shortcuts can be assigned to paramaters to simplify commands:
``` python
$ echo " now what " | python -m texttools "reverse(w)->trim()"
$> what now
```


