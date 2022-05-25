# maxp

## Installation
View package on [PyPi](https://pypi.org/project/maxp/).

1. Open `Command Prompt`
2. Run `cd "C:\Program Files\Autodesk\3ds Max 2023\Python"`
3. Run `pip install maxp`

## Examples

### AutoWindow

```python
from maxp.widgets.autowindow import AutoWindow
class MyWindow(AutoWindow):
    def __init__(self):
        super().__init__('My Window Title', uiFileName='interface.ui')
```
