# Tired to get 200+ errors of coding style on your project ?
Here is a Clang-Format config to respect EPITA coding style (most of it).

## How to use it
1. Install Clang Format
2. Drop it to your home dir
3. Install a plugin to link it in you favourite Ide (vim-clang-format | Sublime Clang Format)

### Or just apply clang format to your whole project
```
find . -iname *.h -o -iname *.c | xargs clang-format -i
```

## Other tools
Clang-Format is not perfect and some errors might remain. To solve this started working on a moulinette to display remaining coding style errors. \

### How to run the moulinette

First install the moulinette
```
mkdir ~/.scripts
cp <path-to-repo>/moulinette.py ~/.scripts
```
And then add the following line to your bash config (.bashrc of .bash_profile)
```
alias moulinette='python3 ~/.scripts/moulinette.py'
```

### How to solve remaining errors

If the error is caused by a bad formatting of clang format such as:
```
int arr[10] = {0};
```
Instead of:
```
int arr[10] =
{
    0
};
```
Then, you have to disable clang-format on that specific portion of code as follow:
```
// clang-format off
int arr[10] =
{
    0
};
// clang-format on
```
For other errors such as "More than 10 functions in file. (8.9)", you'll have to fix them on your own.

## How to collab
If you find new useful commands don't hesitate to notify me or make a pull request. \
When adding a new line of config, please add a comment to breifly explain what the line does. \
Also add the coding style corresponding number to keep track of implemented features.

## Documentation
Documentation on Clang-Format can be found [here](https://clang.llvm.org/docs/ClangFormatStyleOptions.html)
