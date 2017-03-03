from subprocess import call
import sys

def main():
    UUID = sys.argv[1]
    call(["sudo", "hcitool", "-i", "hci0 cmd 0x08 0x0008 1e 02 01 1a 1a ff 4c 00 02 15 " + UUID + " 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"])


if __name__ == "__main__":
    main()
