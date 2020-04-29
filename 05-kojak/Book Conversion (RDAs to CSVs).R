require("stringr")


datadir = "Data/Book RDAs/"
writedir = "Data/Book CSVs/"

for (filename in list.files(datadir)) {
  book_title = str_replace(filename, '.rda', '')
  book_name = load(paste(datadir, book_title, ".rda", sep=""))
  book_vec = get(book_name)
  rm(book_name)
  write.(book_vec, file=paste(writedir, book_title, ".csv", sep=""), sep="")
}

