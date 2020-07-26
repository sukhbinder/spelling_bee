# spelling_bee
Spelling Bee for kids


## Quick Demo.

```bash

spelling -h
usage: spelling [-h] [-num NUM] [-s] [-w WORD_FILE]

Spelling BEE

optional arguments:
  -h, --help            show this help message and exit
  -num NUM              number of words
  -s, --skip-intro      Say intro
  -w WORD_FILE, --word-file WORD_FILE

```

### Example Content of word file 

```bash
cat words.txt 

Victorious
Mandatory
Obligatory
Territorial	
Auditorium
Romance
Performance 
Chance 
Guidance 
Glance 
Finance 

```

### To check spelling log

```bash

spelling_log

```
This produces

![](img/spelling_log.png)


### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/sukhbinder/spelling_bee
  $ cd spelling_bee
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

4. Install system dependencies, on Fedora linux:
  ```
  sudo dnf -y install espeak espeak-ng espeak-ng-devel libtimidity-devel
  ```

5. Run the app
  ```
  $ python spelling_bee.py -w words.txt
  ```

