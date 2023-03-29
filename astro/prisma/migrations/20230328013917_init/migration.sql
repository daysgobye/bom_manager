-- CreateTable
CREATE TABLE "User" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "token" TEXT NOT NULL
);

-- CreateTable
CREATE TABLE "Part" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "userId" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "package" TEXT NOT NULL,
    "value" TEXT NOT NULL,
    "part_number" TEXT NOT NULL,
    "qty" INTEGER NOT NULL,
    "note" TEXT NOT NULL,
    "location" TEXT NOT NULL,
    "dataSheet" TEXT NOT NULL,
    "missing" BOOLEAN NOT NULL DEFAULT false,
    "rollback" BOOLEAN NOT NULL DEFAULT false,
    "incoming" BOOLEAN NOT NULL DEFAULT false,
    "lookup" BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT "Part_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "User_token_key" ON "User"("token");
