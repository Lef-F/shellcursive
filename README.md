# shellcursive: Apply CLI commands to ALL the folders you like 🌈

Has this ever happened to you?

You are going to not have access to the internet for a while and you need to make sure you have all your codebases up-to-date and offline?

You're at the right place my friend! 🥳

## Run

```shell
./run /path/to/walk/under command --to execute
```

By default `shellcursive` looks for paths with a `.git` folder in them so to `git pull` all repos under a path you can simply run:

```shell
./run /path/to/walk/under git pull
```

To list all files in all folders named `kazaa` simply run:

```shell
./run --pattern **/kazaa/ /path/to/walk/under ls -alh
```
