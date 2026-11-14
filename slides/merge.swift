import PDFKit
let a = CommandLine.arguments
let out = PDFDocument(url: URL(fileURLWithPath: a[1]))!
let add = PDFDocument(url: URL(fileURLWithPath: a[2]))!
for i in 0..<add.pageCount { out.insert(add.page(at: i)!, at: out.pageCount) }
out.write(to: URL(fileURLWithPath: a[3]))
print("pages:", out.pageCount)
