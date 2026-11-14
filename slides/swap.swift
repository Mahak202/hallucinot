import PDFKit
import AppKit
let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
let rep = PDFDocument(url: URL(fileURLWithPath: a[2]))!.page(at: 0)!
doc.removePage(at: 8); doc.insert(rep, at: 8)
doc.write(to: URL(fileURLWithPath: a[3]))
let img = rep.thumbnail(of: NSSize(width: 1280, height: 720), for: .mediaBox)
try! NSBitmapImageRep(data: img.tiffRepresentation!)!.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: a[4]))
print("pages:", doc.pageCount)
