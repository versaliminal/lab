# VERSALIMINAL LAB

## High-Level Diagram
![diagram](diagram.png)

## Compute Node Configurations
```
[
  {
    "Name": "warlock",
    "Cores": 16,
    "StorageGB": 100,
    "MemoryGB": 64
  },
  {
    "Name": "sorcerer",
    "Cores": 20,
    "StorageGB": 100,
    "MemoryGB": 48
  },
  {
    "Name": "wizard",
    "Cores": 22,
    "StorageGB": 100,
    "MemoryGB": 64
  }
]
```

## Storage Group Configurations
```
[
    {
        "Name": "SG1",
        "StorageGB": 10000,
        "Host": "warlock"
    }
]
```