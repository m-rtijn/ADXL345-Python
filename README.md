# ADXL345-Python

You can use this program to interact with the ADXL345 Accelerometer using your
Raspberry Pi.

What you need is the python-smbus library, if you don't have this library installed
yet you can install it using:
```
	sudo apt-get install python-smbus
```
	
Once you've installed smbus you can import ADXL345.py in your own python programs.
you have to make sure that ADXL345.py is in the same directory as your python program.

If you don't know how to import it, it's really simple: just place this in your python
program:

```python
	from ADXL345 import ADXL345
```

Please note that for this program to work you need to have i2c enabled on your Raspberry Pi.