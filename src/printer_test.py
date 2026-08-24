from escpos.printer import Usb
import settings

printer = Usb(
    settings.PRINTER_VID, 
    settings.PRINTER_PID,
    0,
    out_ep=settings.PRINTER_OUT,
    in_ep=settings.PRINTER_IN)

printer.text("Mem-O-Mart printer test\n")
printer.text("Printer connected!\n")
printer.text("----------------------\n")
printer.cut()