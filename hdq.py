#!/usr/bin/python

# hdq over uart implementation
# based on http://www.ti.com/lit/an/slua408a/slua408a.pdf
# (c) 2017 jens jensen

import serial
import argparse
import binascii
import csv

ap = argparse.ArgumentParser()
ap.add_argument("port")
ap.add_argument("-d","--debug", action="store_true")
ap.add_argument("-f","--file", help="csvfile containing reg info")
args = ap.parse_args()

ser = serial.Serial(args.port, 57600, stopbits=2, timeout=1)

HDQ_BIT1 = 0xFE
HDQ_BIT0 = 0xC0
HDQ_BIT_THRESHOLD = 0xF8

def reset():
    #reset
    ser.send_break()
    ser.read()

def write_byte(byte):
    #convert and write 8 data bits
    buf = bytearray()
    for i in range(8):
        if (byte & 1) == 1:
                buf.append(HDQ_BIT1)
        else:
                buf.append(HDQ_BIT0)
        byte = byte >> 1
    if args.debug:
        print "sending:", binascii.hexlify(buf)
    ser.write(buf)
    # chew echoed bytes
    ser.read(8)

def read_byte():
    #read and convert 8 data bits
    buf = ser.read(8)
    buf = bytearray(buf)
    # lsb first, so reverse:
    buf.reverse()
    if args.debug:
        print "recv buf:", binascii.hexlify(buf)
    byte = 0
    for i in range(8):
        byte = byte << 1
        if buf[i] > HDQ_BIT_THRESHOLD:
            byte = byte | 1       
    return byte

def uint16le(bl, bh):
    word = bh << 8 | bl
    return word

def read_reg(reg):
    write_byte(reg)
    return read_byte()

def write_reg(reg, byte):
    write_byte(0x80 | reg)
    write_byte(byte)
 
#main
reset()

if args.file:
    with open(args.file) as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        print "%24s %8s %6s %6s %s" % ("name","short", "hex", "dec", "unit")
        for row in reader:
            regs = row["regaddrs"].split('/')
            byte_low = read_reg(int(regs[0],16))
            byte_high = read_reg(int(regs[1],16))
            value = uint16le(byte_low, byte_high)
            name = row["name"]
            shortname = row["shortname"]
            unit = row["unit"]
            print "%24s %8s 0x%04X %6d %s" % (name, shortname, value, value, unit)
            
else:
    #demo
    print "get DEVICE_TYPE..."
    write_reg(0x00, 0x01)
    write_reg(0x01, 0x00)
    b1 = read_reg(0x00)
    b2 = read_reg(0x01)
    value = uint16le(b1,b2)
    print "value: 0x%04X" % value

