import PDFKit
import AppKit
let a = CommandLine.arguments
let doc = PDFDocument(url: URL(fileURLWithPath: a[1]))!
for n in a[3...] {
  let i = Int(n)! - 1
  let page = doc.page(at: i)!
  let img = page.thumbnail(of: NSSize(width: 1280, height: 720), for: .mediaBox)
  let rep = NSBitmapImageRep(data: img.tiffRepresentation!)!
  try! rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: "\(a[2])/page\(n).png"))
}
print("ok")
