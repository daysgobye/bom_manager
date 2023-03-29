import { PrismaClient, Prisma } from "@prisma/client";
const prisma = new PrismaClient();

export const getUserForToken = async (token: string) => {
  return await prisma.user.findFirstOrThrow({ where: { token: token } });
};

export const addPartsToUser = async (
  id: number,
  parts: Prisma.PartCreateInput[]
) => {
  await Promise.all(
    parts.map((part) => {
      prisma.user.update({
        where: { id },
        data: {
          partLibrary: {
            create: part,
          },
        },
      });
    })
  );
  const user = await prisma.user.findFirstOrThrow({ where: { id } });
  return user;
};
export const createUser = async (token: string) => {
  const newUser: Prisma.UserCreateInput = {
    token,
  };
  return prisma.user.create({
    data: {
      ...newUser,
    },
  });
};
