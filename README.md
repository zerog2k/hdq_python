# hdq_python
python example for reading Texas Instruments battery gas gauge ICs via HDQ protocol via UART

useful for reading data from things like iphone batteries

### hardware
* some kind of cheap usb to uart adapter, e.g. CP2102, CH340G. [Banggood: CP2102 USB-UART adapter](http://www.banggood.com/CJMCU-CP2102-USB-To-TTLSerial-Module-UART-STC-Downloader-p-970993.html?p=WX0407753399201409DA)
#### connection
* RXD pin of uart is connected to HDQ pin
* TXD pin of uart is tied to RXD/HDQ via small signal diode, e.g. 1N4148, with cathode pointing back to TXD, anode to RXD/HDQ
* if that doesn't work, e.g. not using open-drain uart, refer to the TI app note (slua408a referenced below, fig. 5)

### software
python (duh!)
requires pyserial:
```
pip install -U pyserial
```

### example usage
from an old iphone 5S battery:
```
$ ./hdq.py /dev/ttyUSB0 -f bq27545.csv 
                    name    short    hex    dec unit
               Control()     CNTL 0x0310    784 N/A
                AtRate()       AR 0x0000      0 mA
         UnfilteredSOC()    UFSOC 0x7FFF  32767 %
           Temperature()     TEMP 0x0BB9   3001 0.1K
               Voltage()     VOLT 0x104F   4175 mV
                 Flags()    FLAGS 0x0180    384 N/A
  NomAvailableCapacity()      NAC 0x04CA   1226 mAh
 FullAvailableCapacity()      FAC 0x0544   1348 mAh
     RemainingCapacity()       RM 0x046A   1130 mAh
    FullChargeCapacity()      FCC 0x04E4   1252 mAh
        AverageCurrent()       AI 0x0000      0 mA
           TimeToEmpty()      TTE 0xFFFF  65535 Minutes
           FilteredFCC()     FFCC 0x0000      0 mAh
        StandbyCurrent()       SI 0xFFFC  65532 mA
         UnfilteredFCC()    UFFCC 0x05A0   1440 mAh
        MaxLoadCurrent()      MLI 0xFF38  65336 mA
          UnfilteredRM()     UFRM 0x0B9A   2970 mAh
            FilteredRM()      FRM 0x0568   1384 mAh
          AveragePower()       AP 0x0000      0 mW/cW
   InternalTemperature()  INTTEMP 0x104F   4175 0.1°K
            CycleCount()       CC 0x01F4    500 Counts
         StateOfCharge()      SOC 0x005B     91 %
         StateOfHealth()      SOH 0xFF76  65398 %/num
          PassedCharge()     PCHG 0x0000      0 mAh
                  DOD0()     DOD0 0x05A0   1440 HEX#
  SelfDischargeCurrent()     SDSG 0x007A    122 mA
```

### references
inspired by some articles on ripitapart blog:
https://ripitapart.com/2014/09/30/reading-out-hdq-equipped-battery-fuel-gauges-with-a-serial-port/
https://ripitapart.com/2014/09/30/looking-inside-a-fake-iphone-5s-battery-2/

TI's app note about interfacing HDQ protocol with simple UARTs:
http://www.ti.com/lit/an/slua408a/slua408a.pdf

TI's bq27545 battery gas gauge IC datasheet:
http://www.ti.com/lit/ds/symlink/bq27545-g1.pdf

