# Coding Style EPITA
A Clang-Format config to respect EPITA coding style

## How to use it
1. Install Clang Format 
2. Drop it to your home dir
3. Install a plugin to link it in you favourite Ide (vim-clang-format | Sublime Clang Format)

### Or just apply clang format to your whole project
```
find . -iname *.h -o -iname *.c | xargs clang-format -i
```

## How to collab
If you find new useful commands don't hesitate to notify me or make a pull request. \
When adding a new line of config, please add a comment to breifly explain what the line does. \
Also add the coding style corresponding number to keep track of implemented features.

## Documentation
Documentation on Clang-Format can be found [here](https://clang.llvm.org/docs/ClangFormatStyleOptions.html)
