import { getServerSession } from "next-auth/next";
import { options } from "./../api/auth/[...nextauth]/options";

import prisma from "@/app/libs/prismadb";

export async function getSession() {
  return await getServerSession(options);
}

export default async function getCurrentUser() {
  try {
    // Kimlik doğrulama kontrolünü kaldırdık
    // localStorage'dan kullanıcı bilgilerini almak yerine sabit bir kullanıcı döndürüyoruz
    
    // Tarayıcı tarafında çalışmadığı için server-side olarak sabit bir kullanıcı döndürüyoruz
    return {
      id: "1",
      name: "Test Kullanıcı",
      email: "user@example.com",
      role: "user",
      emailVerified: new Date(),
      image: null,
      createdAt: new Date(),
      updatedAt: new Date()
    };
  } catch (error: any) {
    return {
      id: "1",
      name: "Test Kullanıcı",
      email: "user@example.com",
      role: "user",
      emailVerified: new Date(),
      image: null,
      createdAt: new Date(),
      updatedAt: new Date()
    };
  }
}
