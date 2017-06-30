# hdq_python
python example for reading Texas Instruments battery gas gauge ICs via HDQ protocol via UART

useful for reading data, e.g. voltage, temperature, current, power, state-of-charge, et al., from things like iphone batteries

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
from an old iphone 5S battery, with 1k ohm resistor across +/- terminals:
```
$ ./hdq.py /dev/ttyUSB0 -f bq27545.csv 
                    name    short    hex    dec unit
                AtRate()       AR 0x0000      0 mA
         UnfilteredSOC()    UFSOC 0x7FFF  32767 %
           Temperature()     TEMP 0x0BB8   3000 0.1K
               Voltage()     VOLT 0x1048   4168 mV
                 Flags()    FLAGS 0x0180    384 N/A
  NomAvailableCapacity()      NAC 0x04C7   1223 mAh
 FullAvailableCapacity()      FAC 0x0548   1352 mAh
     RemainingCapacity()       RM 0x045D   1117 mAh
    FullChargeCapacity()      FCC 0x04DE   1246 mAh
        AverageCurrent()       AI 0xFFFD     -3 mA
           TimeToEmpty()      TTE 0x4173  16755 Minutes
           FilteredFCC()     FFCC 0x0000      0 mAh
        StandbyCurrent()       SI 0xFFFC     -4 mA
         UnfilteredFCC()    UFFCC 0x0600   1536 mAh
        MaxLoadCurrent()      MLI 0xFF38   -200 mA
          UnfilteredRM()     UFRM 0x0B99   2969 mAh
            FilteredRM()      FRM 0x0568   1384 mAh
          AveragePower()       AP 0xFFF3    -13 mW/cW
   InternalTemperature()  INTTEMP 0x1048   4168 0.1°K
            CycleCount()       CC 0x01F4    500 Counts
         StateOfCharge()      SOC 0x005A     90 %
         StateOfHealth()      SOH 0xFF76   -138 %/num
          PassedCharge()     PCHG 0x0000      0 mAh
                  DOD0()     DOD0 0x0600   1536 HEX#
  SelfDischargeCurrent()     SDSG 0x0080    128 mA
```
note that in Apple implementation, not all of the outputs seem to correspond to datasheet values.

A few useful datapoints that did seem like they are reporting correctly:
 * temperature
 * voltage
 * flags (for determining charged/discharging status)
 * remaining capacity
 * avg current/avg power
 * state of charge

### references
inspired by some articles on ripitapart blog:
https://ripitapart.com/2014/09/30/reading-out-hdq-equipped-battery-fuel-gauges-with-a-serial-port/
https://ripitapart.com/2014/09/30/looking-inside-a-fake-iphone-5s-battery-2/

TI's app note about interfacing HDQ protocol with simple UARTs:
http://www.ti.com/lit/an/slua408a/slua408a.pdf

TI's bq27545 battery gas gauge IC datasheet:
http://www.ti.com/lit/ds/symlink/bq27545-g1.pdf

