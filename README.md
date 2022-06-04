# maxp

## Requirements
This package is only intended and developed for use with _***3ds Max 2021 and above***_.

## Installation

### Development
View package on [PyPi](https://pypi.org/project/maxp/).

1. Open `Command Prompt`
2. Run `cd "C:\Program Files\Autodesk\3ds Max 2023\Python"`
3. Run `pip install maxp`

### In 3ds Max

1. Download and run `install.bat` found in the root of this repository.
2. This will install in any version of 3ds Max which is compatible.

## Examples

### AutoWindow

```python
from maxp.widgets.autowindow import AutoWindow
class MyWindow(AutoWindow):
    def __init__(self):
        super().__init__('My Window Title', uiFileName='interface.ui')
```
