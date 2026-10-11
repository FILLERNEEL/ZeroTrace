# ZeroTrace

A simple multithreaded TCP port scanner written in Python.
I built it while learning about networking and cybersecurity.

## Features
- Scans any port range from 1 to 65535
- Uses 100 threads for faster scanning
- Works with an IP address or a hostname
- Shows open ports and the time taken

## How to run
No extra libraries needed, just Python 3.

```
python portScanner.py
```

Then enter a target and a port range:

```
Target IP/host: 127.0.0.1
Port range (e.g. 1-100): 1-1000
```

## Disclaimer
Only scan systems you own or have permission to test.
